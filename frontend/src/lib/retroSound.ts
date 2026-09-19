// Procedural Web Audio clicks under 2KB, off by default (TODO-5.10).
let ctx: AudioContext | null = null;
export function retroClick(enabled = false): void {
  if (!enabled) return;
  try {
    ctx = ctx || new AudioContext();
    const o = ctx.createOscillator();
    const g = ctx.createGain();
    o.connect(g);
    g.connect(ctx.destination);
    o.frequency.value = 880;
    g.gain.value = 0.05;
    o.start();
    o.stop(ctx.currentTime + 0.05);
  } catch {
    return;
  }
}
