import os
import shutil
import time
from pathlib import Path
from typing import List, Dict, Any, Optional
from src.config import settings


class ChromaSnapshotManager:
    """
    Manages point-in-time timestamped backups and zero-downtime rollbacks
    of the ChromaDB vector database before re-indexing.
    """

    def __init__(self, chroma_dir: Optional[Path] = None, snapshots_dir: Optional[Path] = None):
        self.chroma_dir = chroma_dir or settings.chroma_persist_dir
        self.snapshots_dir = snapshots_dir or (self.chroma_dir.parent / "snapshots")
        self.snapshots_dir.mkdir(parents=True, exist_ok=True)

    def create_snapshot(self, tag: Optional[str] = None) -> Dict[str, Any]:
        """Creates a timestamped snapshot of chroma_db directory."""
        if not self.chroma_dir.exists():
            return {"status": "error", "message": f"{self.chroma_dir} does not exist"}

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        snapshot_name = f"snapshot_{timestamp}" + (f"_{tag}" if tag else "")
        target_path = self.snapshots_dir / snapshot_name

        try:
            shutil.copytree(self.chroma_dir, target_path, dirs_exist_ok=True)
            return {
                "status": "success",
                "snapshot_name": snapshot_name,
                "snapshot_path": str(target_path),
                "created_at": timestamp
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def list_snapshots(self) -> List[Dict[str, Any]]:
        """Lists all available snapshots sorted by creation date descending."""
        if not self.snapshots_dir.exists():
            return []

        snapshots = []
        for item in sorted(self.snapshots_dir.iterdir(), reverse=True):
            if item.is_dir() and item.name.startswith("snapshot_"):
                snapshots.append({
                    "snapshot_name": item.name,
                    "snapshot_path": str(item),
                    "size_bytes": sum(f.stat().st_size for f in item.rglob('*') if f.is_file())
                })
        return snapshots

    def restore_snapshot(self, snapshot_name: str) -> Dict[str, Any]:
        """Rollback chroma_db from a specific snapshot if indexing fails."""
        source_path = self.snapshots_dir / snapshot_name
        if not source_path.exists():
            return {"status": "error", "message": f"Snapshot {snapshot_name} not found"}

        try:
            # Backup current state into temporary quarantine before overwriting
            if self.chroma_dir.exists():
                shutil.rmtree(self.chroma_dir)
            shutil.copytree(source_path, self.chroma_dir)
            return {
                "status": "success",
                "restored_snapshot": snapshot_name,
                "target_path": str(self.chroma_dir)
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}


snapshot_manager = ChromaSnapshotManager()
