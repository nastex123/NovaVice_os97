"""
Servicio del Bot de Telegram en Python para Nova Idiomas.
Permite recibir consultas de usuarios a través de Telegram, responder vía RAG
y escalar automáticamente a asesores humanos cuando sea necesario.
"""

import asyncio
import logging
from typing import Dict, Any, Optional
import httpx
from src.config import settings
from src.rag.engine import rag_engine

logger = logging.getLogger("telegram_bot")


class TelegramBotService:
    def __init__(self, token: Optional[str] = None):
        self.token = token or settings.telegram_bot_token
        self.base_url = f"https://api.telegram.org/bot{self.token}" if self.token else ""
        self._is_polling = False
        self._polling_task: Optional[asyncio.Task] = None

    @property
    def is_configured(self) -> bool:
        return bool(self.token and len(self.token.strip()) > 10)

    async def send_message(
        self,
        chat_id: int,
        text: str,
        reply_markup: Optional[Dict[str, Any]] = None
    ) -> bool:
        if not self.is_configured:
            return False

        payload: Dict[str, Any] = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "Markdown"
        }
        if reply_markup:
            payload["reply_markup"] = reply_markup

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(f"{self.base_url}/sendMessage", json=payload)
                if resp.status_code != 200:
                    # Fallback without markdown parsing if syntax error occurs
                    payload.pop("parse_mode", None)
                    await client.post(f"{self.base_url}/sendMessage", json=payload)
                return resp.status_code == 200
        except Exception as e:
            logger.error(f"Error enviando mensaje por Telegram: {e}")
            return False

    def build_keyboard(self, buttons: list) -> Dict[str, Any]:
        keyboard = []
        row = []
        for btn in buttons:
            row.append({"text": btn.get("label", btn.get("text", "Opción"))})
            if len(row) == 2:
                keyboard.append(row)
                row = []
        if row:
            keyboard.append(row)

        return {
            "keyboard": keyboard,
            "resize_keyboard": True,
            "one_time_keyboard": False
        }

    async def handle_update(self, update: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Procesa una actualización individual recibida por webhook o polling.
        """
        message = update.get("message") or update.get("edited_message")
        if not message:
            return None

        chat = message.get("chat", {})
        chat_id = chat.get("id")
        user = message.get("from", {})
        user_id = f"telegram_{user.get('id', chat_id)}"
        user_text = message.get("text", "").strip()

        if not chat_id or not user_text:
            return None

        # Handle commands
        if user_text.lower() in ("/start", "/menu", "menu", "inicio", "0"):
            query_to_send = "0"
        else:
            query_to_send = user_text

        # Process through Pure Python RAG Engine
        session_id = f"tg_session_{chat_id}"
        rag_response = await rag_engine.answer_query(
            query=query_to_send,
            user_id=user_id,
            session_id=session_id
        )

        response_text = rag_response.get("response", "Lo siento, no pude procesar tu solicitud.")
        action_buttons = rag_response.get("action_buttons", [])
        reply_markup = self.build_keyboard(action_buttons) if action_buttons else None

        await self.send_message(chat_id, response_text, reply_markup=reply_markup)

        return {
            "chat_id": chat_id,
            "status": "responded",
            "query": user_text,
            "escalated": rag_response.get("escalated_to_human", False)
        }

    async def _polling_loop(self):
        offset = 0
        logger.info("Iniciando servicio de polling de Telegram...")
        async with httpx.AsyncClient(timeout=30.0) as client:
            while self._is_polling:
                try:
                    resp = await client.get(
                        f"{self.base_url}/getUpdates",
                        params={"offset": offset, "timeout": 20}
                    )
                    if resp.status_code == 200:
                        data = resp.json()
                        updates = data.get("result", [])
                        for upd in updates:
                            offset = upd.get("update_id", 0) + 1
                            await self.handle_update(upd)
                except asyncio.CancelledError:
                    break
                except Exception as e:
                    logger.error(f"Error en polling de Telegram: {e}")
                    await asyncio.sleep(5)

    def start_polling(self):
        if not self.is_configured:
            logger.info("Telegram bot no configurado (TELEGRAM_BOT_TOKEN vacío).")
            return
        if not self._is_polling:
            self._is_polling = True
            self._polling_task = asyncio.create_task(self._polling_loop())

    def stop_polling(self):
        if self._is_polling:
            self._is_polling = False
            if self._polling_task:
                self._polling_task.cancel()


telegram_service = TelegramBotService()
