"""Procedural sound effects and mixing tools (numpy/scipy). Every function returns mono float32 @ SR."""
import numpy as np
from scipy.signal import butter, sosfilt

SR = 48000
_rng = np.random.default_rng(7)


def t_(d): return np.arange(int(round(d * SR))) / SR   # rounds the same way as noise(), so multiplying them doesn't fail on an off-by-one length
def env_exp(d, tau): return np.exp(-t_(d) / tau)
def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], 'band', fs=SR, output='sos'), x)
def lp(x, f, o=2): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x)
def noise(d): return _rng.standard_normal(int(round(d * SR)))
def norm(x, p=1.0): m = np.abs(x).max(); return x * (p / m) if m > 0 else x


def brown(d):
    w = np.cumsum(noise(d)); w -= np.linspace(w[0], w[-1], len(w)); return norm(hp(w, 20))


# —— Bricks / toys ——
def click(pitch=1.0, v=1.0):
    """Plastic bricks snapping together: very short noise transient + two high resonances + a little low end"""
    d = .06; tt = t_(d)
    tr = hp(noise(d), 2500) * env_exp(d, .0015)
    res = sum(a * np.sin(2 * np.pi * f * pitch * tt + _rng.random() * 6) * env_exp(d, tau)
              for f, a, tau in [(2900, .6, .012), (4600, .4, .008), (1500, .35, .018)])
    body = np.sin(2 * np.pi * 190 * pitch * tt) * env_exp(d, .01) * .5
    return norm(tr * .8 + res + body) * v


def clack(pitch=1.0, v=1.0):
    """Brick dropped on a tabletop: the wood's mids + the plastic's highs"""
    d = .09; tt = t_(d); p = pitch * (.85 + _rng.random() * .3)
    x = hp(noise(d), 1200) * env_exp(d, .004) + sum(a * np.sin(2 * np.pi * f * p * tt) * env_exp(d, tau)
        for f, a, tau in [(1200, .6, .02), (2300, .5, .012), (380, .5, .03)])
    return norm(x) * v


def crash(v=1.0):
    d = .9; out = np.zeros(int(d * SR))
    for k in range(18):
        s = int((k / 18) ** 1.4 * .6 * SR); c = clack(.8 + _rng.random() * .6, .4 + _rng.random() * .6); out[s:s + len(c)] += c[:len(out) - s]
    out[:int(.2 * SR)] += lp(noise(.2), 400) * env_exp(.2, .05) * .8
    return norm(out) * v


def whoosh(d=.35, v=1.0):
    n = noise(d); tt = t_(d); out = np.zeros_like(n)
    for i in range(0, len(n), 480):   # swept bandpass
        hi = min(len(n), i + 480)     # when the last block is shorter than 480 samples, take its actual length (so it doesn't crash when d isn't a multiple of 0.01 s)
        f = 600 + 2600 * np.sin(np.pi * i / len(n)); seg = bp(n[max(0, i - 2000):hi], f * .7, f * 1.3)[-(hi - i):]; out[i:hi] = seg
    return norm(out * np.sin(np.pi * tt / d) ** 2) * v


def creak(v=1.0):
    d = .22; tt = t_(d); f0 = 70 + _rng.random() * 40
    saw = 2 * ((tt * f0 * (1 + .3 * np.sin(2 * np.pi * 9 * tt))) % 1) - 1
    return norm(bp(saw, 400, 3000) * (np.abs(np.sin(2 * np.pi * 23 * tt)) ** 3) * np.sin(np.pi * tt / d)) * v


def thump(v=1.0, f=70):
    d = .35; tt = t_(d)
    return norm(np.sin(2 * np.pi * f * tt * (1 - .3 * tt)) * env_exp(d, .07) + lp(noise(d), 300) * env_exp(d, .02) * .5) * v


def step(v=1.0):
    d = .05; tt = t_(d)
    return norm(hp(noise(d), 1800) * env_exp(d, .004) + np.sin(2 * np.pi * 2200 * tt) * env_exp(d, .006) * .5) * v


def ding(v=1.0):
    d = 1.6; tt = t_(d)
    x = sum(a * np.sin(2 * np.pi * f * tt) * env_exp(d, tau) for f, a, tau in [(1318, 1, .6), (2637, .5, .35), (3951, .3, .2), (1976, .25, .5), (5274, .15, .1)])
    return norm(x) * v


def pop(v=1.0):
    d = .18; tt = t_(d); f = 500 + 1400 * tt / d
    return norm(np.sin(2 * np.pi * np.cumsum(f) / SR) * env_exp(d, .05)) * v


def quindar(v=1.0, f=2525):
    d = .25; tt = t_(d); x = np.sin(2 * np.pi * f * tt); x[:240] *= np.linspace(0, 1, 240); x[-240:] *= np.linspace(1, 0, 240)
    return x * .5 * v


def rumble(d=1.5, v=1.0):
    return norm(lp(brown(d), 200)) * np.sin(np.pi * t_(d) / d / 2) ** 2 * v


def ignite(v=1.0):
    d = 1.8; tt = t_(d)
    sub = np.sin(2 * np.pi * 45 * tt * (1 - .25 * tt)) * env_exp(d, .5)
    burst = lp(noise(d), 1200) * env_exp(d, .35)
    return norm(sub * .9 + burst) * v


def roar(d, v=1.0):
    tt = t_(d); b = lp(brown(d), 700); crack = hp(noise(d), 3000) * (_rng.random(len(tt)) > .995) * 3
    e = np.minimum(1, tt / .4) * np.minimum(1, (d - tt) / .6)
    return norm(b + lp(crack, 6000) * .3) * e * v


def heartbeat(v=1.0):
    return (thump(1, 55) + np.pad(thump(.7, 50), (int(.22 * SR), 0))[:len(thump(1, 55))]) * v


# —— Voice ——
def radio(x):
    """Walkie-talkie: bandpass + light distortion + noise floor"""
    y = bp(x, 380, 2800, 3); y = np.tanh(y * 3) / np.tanh(3)
    return norm(y + bp(_rng.standard_normal(len(y)), 1000, 4000) * .02) * .9


def compress(x, thr=.25, ratio=3.5, att=.004, rel=.08):
    env = np.zeros_like(x); a, r = np.exp(-1 / (att * SR)), np.exp(-1 / (rel * SR)); e = 0.0
    ax = np.abs(x)
    for i in range(len(x)):
        c = ax[i]; e = a * e + (1 - a) * c if c > e else r * e + (1 - r) * c; env[i] = e
    g = np.where(env > thr, (thr + (env - thr) / ratio) / np.maximum(env, 1e-9), 1.0)
    return x * g


def limit(x, ceil=.9, look=.005):
    """1D look-ahead limiter (for multichannel, call it per channel)"""
    n = int(look * SR); pk = np.abs(x)
    from scipy.ndimage import maximum_filter1d, uniform_filter1d
    m = maximum_filter1d(pk, size=2 * n + 1); g = np.minimum(1, ceil / np.maximum(m, 1e-9)); g = uniform_filter1d(g, size=n)
    return x * g


def add(buf, x, at, gain=1.0, pan=0.0):
    s = int(at * SR)
    if s >= len(buf) or s + len(x) <= 0: return
    if s < 0: x = x[-s:]; s = 0
    e = min(len(buf), s + len(x)); l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    buf[s:e, 0] += x[:e - s] * gain * l * 1.414; buf[s:e, 1] += x[:e - s] * gain * r * 1.414


def _st_rms(x, win=0.05):
    from scipy.ndimage import uniform_filter1d
    return np.sqrt(uniform_filter1d(np.square(x), size=max(1, int(win * SR))) + 1e-12)


def under_voice(foley, voice, mask=None, speak_db=24.0, pause_db=10.0, carve_db=8.0, air_hz=7000.0,
                lead=0.12, tail=0.3):
    """Sit a foley layer (pen scratch, burin hiss, paper…) under the narration so it never covers the voice.

    foley, voice: (N,) or (N, 2), with the voice already at the gain it will have in the mix.
    mask: (N,) 1 while someone is speaking (None → found from the voice's own envelope).
    speak_db: the foley's loud moments (95th pct of 50 ms RMS) stay at least this many dB under the voice's average
              level while she speaks. pause_db: the same, between sentences (the foley may be heard, never louder
              than the voice). carve_db: extra cut of 1–4 kHz (where the consonants live) while she speaks.
    air_hz: low-pass on the foley; hiss above it (burin, fineliner) is what tires the ear and fights sibilance.
    It only ever turns the foley down, never up. Returns (foley, report) with the measured gaps in dB.
    """
    from scipy.ndimage import uniform_filter1d
    st = foley.ndim == 2; F = foley if st else foley[:, None]
    V = voice.mean(1) if voice.ndim == 2 else voice
    N = len(V)
    if mask is None:
        e = _st_rms(V, 0.03); mask = (e > e.max() * 10 ** (-35 / 20)).astype(float)
    mask = np.asarray(mask, float)[:N]
    if mask.max() <= 0:
        return foley, dict(speech_gap_db=None, pause_gap_db=None)
    # widen the speaking zone (the pen steps back just before she starts and comes back after), with eased edges
    from scipy.ndimage import maximum_filter1d
    w = maximum_filter1d(mask, size=int((lead + tail) * SR) + 1, origin=int((tail - lead) / 2 * SR))
    w = np.clip(uniform_filter1d(w, size=int(0.1 * SR)), 0, 1)
    F = np.stack([lp(F[:, c], air_hz, 4) for c in range(F.shape[1])], 1)
    if carve_db > 0:
        k = 1 - 10 ** (-carve_db / 20)
        F = F - k * w[:, None] * np.stack([bp(F[:, c], 1000, 4000, 2) for c in range(F.shape[1])], 1)
    v_lvl = float(np.sqrt(np.mean(np.square(V[mask > 0.5])) + 1e-12))
    env = _st_rms(F.mean(1)); act = env > env.max() * 10 ** (-45 / 20)

    def loud(sel):
        s = sel & act
        return float(np.percentile(env[s], 95)) if s.sum() > int(0.05 * SR) else None
    sp, pa = loud(w > 0.5), loud(w <= 0.5)
    gp = min(1.0, v_lvl * 10 ** (-pause_db / 20) / pa) if pa else 1.0
    gs = min(gp, v_lvl * 10 ** (-speak_db / 20) / sp) if sp else gp
    g = gp + (gs - gp) * w
    F = F * g[:, None]
    env2 = _st_rms(F.mean(1)); db = lambda a: 20 * np.log10(a + 1e-12)
    rep = dict(speech_gap_db=round(float(db(v_lvl) - db(np.percentile(env2[(w > 0.5) & act], 95))), 1) if sp else None,
               pause_gap_db=round(float(db(v_lvl) - db(np.percentile(env2[(w <= 0.5) & act], 95))), 1) if pa else None,
               turned_down_db=round(float(-db(gs)), 1))
    return (F if st else F[:, 0]), rep
