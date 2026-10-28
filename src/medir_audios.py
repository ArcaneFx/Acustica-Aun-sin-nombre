"""Mide duración, tono (F0 aproximado por autocorrelación) y nivel (RMS) de una misma oración con cada preset emocional.

Uso: python src/medir_audios.py results/audios/demo_emociones
"""
import sys, wave
import numpy as np
sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
import fase2_narracion as f
voz = f.cargar_voz("es_MX-claude-high")
texto = "De pronto, la puerta se abrió con violencia y un viajero empapado cayó de rodillas."
def f0(x, sr):
    x = x.astype(float); out = []
    for i in range(0, len(x) - 2048, 512):
        v = x[i:i+2048]; v = v - v.mean()
        if np.sqrt((v**2).mean()) < 0.02 * 32768: continue
        a = np.correlate(v, v, "full")[2047:]
        lo, hi = int(sr/400), int(sr/70)
        k = lo + np.argmax(a[lo:hi])
        if a[k] > 0.4 * a[0]: out.append(sr / k)
    return np.median(out)
print(f"{'emoción':<9}{'dur(s)':>7}{'F0(Hz)':>8}{'RMS(dB)':>9}")
for emo, p in f.PARAMETROS.items():
    pcm, sr = f.sintetizar(voz, texto, p)
    ruta = f"{sys.argv[1]}/{emo}.wav"
    f.modular(pcm, sr, p, ruta)
    w = wave.open(ruta); x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
    voz_x = x[: len(x) - int(p["pausa"] * sr)]
    rms = 20*np.log10(np.sqrt((voz_x.astype(float)**2).mean())/32768)
    print(f"{emo:<9}{len(voz_x)/sr:>7.2f}{f0(voz_x, sr):>8.0f}{rms:>9.1f}")
