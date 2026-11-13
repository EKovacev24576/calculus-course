import json, sys, os, subprocess, math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import Arc, Polygon, FancyBboxPatch

for f in ("Poppins-Regular", "Poppins-Medium", "Poppins-Bold", "Poppins-SemiBold"):
    p = f"/usr/share/fonts/truetype/google-fonts/{f}.ttf"
    if os.path.exists(p): fm.fontManager.addfont(p)
plt.rcParams.update({"font.family": "Poppins", "mathtext.fontset": "dejavusans", "axes.unicode_minus": False})

W, H, FPS, PAD = 1920, 1080, 24, 0.8
BG, INK, MUTE = "#0E1525", "#F4F7FB", "#8A97B0"
TURQ, CORAL, YEL, GRID = "#24C8C6", "#FF746A", "#FFD166", "#243049"
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Cues:
    def __init__(s, name):
        r = json.load(open(f"{HERE}/vo/{name}.json"))
        s.ch, s.t = [], []
        for c in r["timestamps"]:
            s.ch += c["characters"]; s.t += c["character_start_times_seconds"]
        s.text = "".join(s.ch).lower()
        s.dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                      f"{HERE}/vo/{name}.mp3"], capture_output=True, text=True).stdout)
    def __call__(s, phrase, at=None, nth=1):
        i = -1
        for _ in range(nth):
            i = s.text.find(phrase.lower(), i + 1)
            if i < 0: raise KeyError(phrase)
        if at: i += phrase.lower().find(at.lower())
        return s.t[i]

def clamp(v, a=0.0, b=1.0): return max(a, min(b, v))
def ease(v): v = clamp(v); return v * v * (3 - 2 * v)
def fade(t, t0, d=0.5): return ease((t - t0) / d)
def lerp(a, b, k): return a + (b - a) * k

def header(fig):
    fig.text(0.04, 0.945, "WHAT IS A DERIVATIVE?", color=MUTE, fontsize=17, fontweight="bold")
    fig.text(0.225, 0.945, "LEVEL 1  ·  THE IDEA", color=TURQ, fontsize=17, fontweight="bold")

def axes(fig, a=1.0, rect=(0.07, 0.13, 0.55, 0.72), xl=True, yl=True, ymax=10.8, ylabel="distance (meters)"):
    ax = fig.add_axes(rect); ax.set_facecolor(BG)
    ax.set_xlim(0, 3.35); ax.set_ylim(0, ymax)
    for sp in ("top", "right"): ax.spines[sp].set_visible(False)
    for sp in ("left", "bottom"): ax.spines[sp].set_color(MUTE); ax.spines[sp].set_linewidth(2.5); ax.spines[sp].set_alpha(a)
    ax.set_xticks([0, 1, 2, 3]); ax.set_yticks(range(0, int(ymax) + 1, 2))
    ax.tick_params(colors=MUTE, labelsize=20, length=7, width=2)
    for l in ax.get_xticklabels() + ax.get_yticklabels(): l.set_alpha(a)
    ax.grid(True, color=GRID, lw=1.5, alpha=a); ax.set_axisbelow(True)
    if xl is not False: ax.set_xlabel("time (seconds)", color=INK, fontsize=24, labelpad=12, alpha=a if xl is True else xl)
    if yl is not False: ax.set_ylabel(ylabel, color=INK, fontsize=24, labelpad=12, alpha=a if yl is True else yl)
    return ax

def curve(ax, upto=3.25, a=1.0, lw=6):
    t = np.linspace(0, max(upto, 0.001), 240)
    ax.plot(t, t ** 2, color=TURQ, lw=lw, solid_capstyle="round", alpha=a, zorder=3)

def dot(ax, x, y, c=INK, s=260, a=1.0, z=6):
    ax.scatter([x], [y], s=s, color=c, edgecolors=BG, linewidths=3, zorder=z, alpha=a)

def line(ax, x0, y0, m, c, lw=4.5, a=1.0, x1=-0.3, x2=3.6, z=4):
    xs = np.array([x1, x2]); ax.plot(xs, y0 + m * (xs - x0), color=c, lw=lw, alpha=a, zorder=z, solid_capstyle="round")

def T(fig, x, y, s, a=1.0, size=34, c=INK, w="medium", ha="left", va="center"):
    if a > 0.01: fig.text(x, y, s, color=c, fontsize=size, fontweight=w, alpha=clamp(a), ha=ha, va=va)

# ---------------- segments ----------------
def seg_a(fig, t, q):
    k0 = 1 - fade(t, q("speedometer") - 0.3, 0.6)
    T(fig, 0.5, 0.56, "What is a derivative?", k0, 76, INK, "bold", "center")
    T(fig, 0.5, 0.44, "Level 1  ·  The idea", k0, 36, TURQ, "medium", "center")
    a = fade(t, q("speedometer"), 0.6)
    if a > 0.01:
        ax = fig.add_axes([0.05, 0.10, 0.46, 0.74]); ax.set_xlim(-1.25, 1.25); ax.set_ylim(-0.35, 1.3); ax.set_aspect("equal"); ax.axis("off")
        ax.add_patch(Arc((0, 0), 2, 2, theta1=0, theta2=180, color=MUTE, lw=10, alpha=a))
        for v in range(0, 121, 20):
            th = math.radians(180 - v / 120 * 180)
            ax.plot([0.88 * math.cos(th), 1.0 * math.cos(th)], [0.88 * math.sin(th), 1.0 * math.sin(th)], color=INK, lw=4, alpha=a)
            ax.text(0.74 * math.cos(th), 0.74 * math.sin(th), str(v), color=MUTE, fontsize=22, ha="center", va="center", alpha=a)
        v = 60 * ease((t - q("speedometer")) / max(0.5, q("sixty") - q("speedometer") + 0.4))
        th = math.radians(180 - v / 120 * 180)
        ax.plot([0, 0.82 * math.cos(th)], [0, 0.82 * math.sin(th)], color=CORAL, lw=9, solid_capstyle="round", alpha=a)
        ax.scatter([0], [0], s=700, color=CORAL, alpha=a, zorder=5)
        ax.text(0, -0.25, f"{v:.0f} mph", color=INK, fontsize=54, fontweight="bold", ha="center", va="center", alpha=a)
    b = fade(t, q("a distance divided"))
    T(fig, 0.58, 0.72, "speed  =", b, 44)
    T(fig, 0.76, 0.72, r"$\frac{\mathrm{distance}}{\mathrm{time}}$", b, 66, TURQ)
    c = fade(t, q("at a single instant"))
    T(fig, 0.58, 0.50, "at one instant:", c, 34, MUTE)
    d = fade(t, q("no time passes"))
    T(fig, 0.58, 0.38, "speed  =", d, 44)
    T(fig, 0.76, 0.38, r"$\frac{0}{0}$", d, 66, CORAL)
    T(fig, 0.83, 0.38, "= ?", fade(t, q("So how can")), 50, CORAL, "bold")
    e = fade(t, q("That puzzle"))
    T(fig, 0.58, 0.20, "The answer:", e, 30, MUTE)
    T(fig, 0.715, 0.20, "the derivative", e, 40, YEL, "bold")

def seg_b(fig, t, q):
    a = fade(t, 0.2, 0.8)
    ax = axes(fig, a, xl=fade(t, q("Time goes across")), yl=fade(t, q("distance goes up")))
    t0 = q("This curve"); k = ease((t - t0) / 3.2)
    if t > t0:
        curve(ax, 3.25 * k); x = 3.25 * k; dot(ax, x, x * x, YEL)
    f = fade(t, q("flatter"))
    if f > 0.01:
        ax.axvspan(0.0, 0.95, color=YEL, alpha=0.10 * f, zorder=1)
        ax.text(0.48, 2.4, "flat\nslow", color=YEL, fontsize=30, ha="center", va="center", alpha=f, fontweight="bold", linespacing=1.3)
    s = fade(t, q("steep,"))
    if s > 0.01:
        ax.axvspan(2.2, 3.25, color=CORAL, alpha=0.12 * s, zorder=1)
        ax.text(2.55, 9.4, "steep\nfast", color=CORAL, fontsize=30, ha="center", va="center", alpha=s, fontweight="bold", linespacing=1.3)
    T(fig, 0.66, 0.74, "How far the car", fade(t, t0), 32, MUTE); T(fig, 0.66, 0.685, "has gone", fade(t, t0), 32, MUTE)
    h = fade(t, q("Speed is hiding"))
    T(fig, 0.66, 0.48, "speed", h, 52, INK, "bold"); T(fig, 0.66, 0.40, "= steepness", h, 52, YEL, "bold"); T(fig, 0.66, 0.325, "of the curve", h, 36, MUTE)

def tri(ax, x1, x2, a_run=1.0, a_rise=1.0, run_txt="run", rise_txt="rise"):
    y1, y2 = x1 * x1, x2 * x2
    ax.plot([x1, x2], [y1, y1], color=YEL, lw=4, ls=(0, (4, 3)), alpha=a_run, zorder=4)
    ax.plot([x2, x2], [y1, y2], color=CORAL, lw=4, ls=(0, (4, 3)), alpha=a_rise, zorder=4)
    ax.text((x1 + x2) / 2, y1 - 0.62, run_txt, color=YEL, fontsize=26, ha="center", va="center", alpha=a_run, fontweight="bold")
    ax.text(x2 + 0.06, (y1 + y2) / 2, rise_txt, color=CORAL, fontsize=26, ha="left", va="center", alpha=a_rise, fontweight="bold")

def seg_c(fig, t, q):
    ax = axes(fig); curve(ax)
    p = fade(t, q("Pick two points"), 0.4)
    s = ease((t - q("connect them")) / 1.2)
    if s > 0: ax.plot([1, lerp(1, 3, s)], [1, lerp(1, 9, s)], color=INK, lw=5, zorder=5, solid_capstyle="round")
    r = fade(t, q("rise over run"))
    run_txt = "run = 2 s" if t > q("From one second") else "run"
    rise_txt = "rise = 8 m" if t > q("nine meters") else "rise"
    if r > 0.01: tri(ax, 1, 3, r, r, run_txt, rise_txt)
    dot(ax, 1, 1, INK, a=p); dot(ax, 3, 9, INK, a=fade(t, q("Pick two points") + 0.5, 0.4))
    T(fig, 0.66, 0.76, "average speed", fade(t, q("average speed")), 36, MUTE)
    T(fig, 0.66, 0.60, r"$=\ \frac{\mathrm{rise}}{\mathrm{run}}$", fade(t, q("average speed")), 62, INK)
    e = fade(t, q("eight meters in two"))
    T(fig, 0.66, 0.42, r"$=\ \frac{8\ \mathrm{m}}{2\ \mathrm{s}}$", e, 62, INK)
    T(fig, 0.66, 0.24, "= 4 m/s", fade(t, q("four meters per second")), 62, YEL, "bold")

def seg_d(fig, t, q):
    ax = axes(fig); curve(ax)
    k1, k2, k3 = q("Three seconds"), q("Two seconds"), q("One and a half")
    g0, g1 = q("As the gap"), q("It settles")
    if t < k2: x2 = 3.0
    elif t < k3: x2 = lerp(3.0, 2.0, ease((t - k2) / 0.9))
    elif t < g0: x2 = lerp(2.0, 1.5, ease((t - k3) / 0.9))
    else: x2 = lerp(1.5, 1.02, ease((t - g0) / (g1 - g0 + 1.2)))
    m = x2 + 1
    line(ax, 1, 1, m, INK, 4.5)
    tri(ax, 1, x2, 0.9, 0.9, "", "")
    dot(ax, 1, 1, YEL, 320); dot(ax, x2, x2 * x2, INK)
    ax.text(1.0, 1.0 + 1.25, "t = 1", color=YEL, fontsize=24, ha="right", va="center", fontweight="bold")
    T(fig, 0.66, 0.80, "second point at", fade(t, q("slide")), 28, MUTE); T(fig, 0.84, 0.80, "slope", fade(t, q("slide")), 28, MUTE)
    rows = [("3 s", "4", k1, q("Four.")), ("2 s", "3", k2 + 0.5, q("Three.")), ("1.5 s", "2.5", k3 + 0.5, q("Two and a half."))]
    for i, (a_, b_, ta, tb) in enumerate(rows):
        y = 0.70 - i * 0.09
        T(fig, 0.66, y, a_, fade(t, ta), 40, INK); T(fig, 0.84, y, b_, fade(t, tb), 40, YEL, "bold")
    if t > g0:
        T(fig, 0.66, 0.40, f"{x2:.2f} s", fade(t, g0), 40, INK); T(fig, 0.84, 0.40, f"{m:.2f}", fade(t, g0), 40, YEL, "bold")
    z = fade(t, q("number: two", at="two"))
    T(fig, 0.66, 0.22, "slope", z, 44, MUTE); T(fig, 0.755, 0.22, r"$\rightarrow$", z, 54, INK); T(fig, 0.82, 0.22, "2", z, 84, YEL, "bold")

def seg_e(fig, t, q):
    ax = axes(fig); curve(ax)
    k = ease((t - 0.3) / 1.4)
    line(ax, 1, 1, 2, YEL, 5.5, x1=lerp(1, -0.3, k), x2=lerp(1, 3.6, k))
    dot(ax, 1, 1, YEL, 340)
    a = fade(t, q("tangent line"))
    if a > 0.01: ax.text(2.42, 3.2, "tangent line", color=YEL, fontsize=30, alpha=a, fontweight="bold", ha="left", va="center")
    T(fig, 0.66, 0.74, "slope of the tangent", fade(t, q("Its slope")), 32, MUTE)
    T(fig, 0.66, 0.64, "2 m/s", fade(t, q("two meters per second")), 70, YEL, "bold")
    T(fig, 0.66, 0.48, "= the car's speed", fade(t, q("is the car")), 36, INK); T(fig, 0.66, 0.42, "at exactly t = 1 s", fade(t, q("is the car")), 36, INK)
    d = fade(t, q("That number"))
    T(fig, 0.66, 0.27, "This number is", d, 30, MUTE); T(fig, 0.66, 0.20, "the derivative at t = 1", d, 38, TURQ, "bold")

def seg_f(fig, t, q):
    ax = axes(fig, rect=(0.06, 0.13, 0.42, 0.72)); curve(ax)
    s0, s1 = q("Slide along"), q("Collect")
    x = lerp(1.0, 0.15, ease(t / max(s0, 0.5))) if t < s0 else lerp(0.15, 3.0, ease((t - s0) / (s1 - s0 + 1.5)))
    m = 2 * x
    half = 0.55 / math.sqrt(1 + (m / 3.2) ** 2) + 0.25
    line(ax, x, x * x, m, YEL, 5.5, x1=x - half, x2=x + half)
    dot(ax, x, x * x, YEL, 320)
    ax2 = axes(fig, rect=(0.56, 0.13, 0.40, 0.72), ymax=6.6, ylabel="slope (meters per second)")
    if t > s0:
        xs = np.linspace(0.15, x, 80); ax2.plot(xs, 2 * xs, color=YEL, lw=6, solid_capstyle="round", zorder=3); dot(ax2, x, m, YEL, 320)
    ax2.text(0.15, 6.1, f"slope = {m:.1f}", color=YEL, fontsize=32, fontweight="bold", va="center")
    f = fade(t, q("it's flat")) * (1 - fade(t, q("it's steep")))
    if f > 0.01: ax.text(0.9, 8.6, "flat: small slope", color=INK, fontsize=28, alpha=f, fontweight="bold")
    g = fade(t, q("it's steep")) * (1 - fade(t, s1))
    if g > 0.01: ax.text(0.9, 8.6, "steep: large slope", color=INK, fontsize=28, alpha=g, fontweight="bold")
    fig.text(0.27, 0.885, "distance", color=TURQ, fontsize=28, fontweight="bold", ha="center")
    fig.text(0.76, 0.885, "the derivative", color=YEL, fontsize=28, fontweight="bold", ha="center", alpha=clamp(0.25 + 0.75 * fade(t, q("brand new function"))))

def seg_g(fig, t, q):
    a = fade(t, q("The derivative is"))
    T(fig, 0.5, 0.80, "The derivative", a, 64, YEL, "bold", "center")
    T(fig, 0.5, 0.69, "=  the slope of a curve at a single point", a, 44, INK, "medium", "center")
    T(fig, 0.5, 0.60, "=  how fast something is changing right now", fade(t, q("how fast something")), 44, TURQ, "medium", "center")
    items = [("Speed is", "speed", "derivative of distance"), ("population", "population growth", "derivative of population"),
             ("price changes", "price change", "derivative of price"), ("rocket", "a rocket's climb", "derivative of height")]
    for i, (cue, l, r) in enumerate(items):
        b = fade(t, q(cue)); y = 0.45 - i * 0.075
        T(fig, 0.47, y, l, b, 32, INK, "medium", "right"); T(fig, 0.50, y, "=", b, 32, MUTE, "medium", "center"); T(fig, 0.53, y, r, b, 32, MUTE)
    n = fade(t, q("In level two"))
    if n > 0.01:
        ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off"); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
        ax.add_patch(FancyBboxPatch((0.30, 0.055), 0.40, 0.085, boxstyle="round,pad=0.0,rounding_size=0.03", fc="#16223A", ec=TURQ, lw=2.5, alpha=n))
    T(fig, 0.5, 0.097, "Next  ·  Level 2: the formula", n, 32, TURQ, "bold", "center")

SEGS = {"a": seg_a, "b": seg_b, "c": seg_c, "d": seg_d, "e": seg_e, "f": seg_f, "g": seg_g}

def frame(fig, name, t, q):
    fig.clf(); fig.patch.set_facecolor(BG)
    if not (name == "a" and t < q("speedometer")): header(fig)
    SEGS[name](fig, t, q)
    fig.canvas.draw()
    return np.asarray(fig.canvas.buffer_rgba())[:, :, :3]

def render(name, out):
    q = Cues(name); dur = q.dur + PAD; fig = plt.figure(figsize=(W / 100, H / 100), dpi=100)
    tmp = f"{out}/{name}.tmp.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                          "-i", "-", "-i", f"{HERE}/vo/{name}.mp3", "-af", f"apad=whole_dur={dur}", "-c:v", "libx264", "-crf", "18", "-preset", "veryfast",
                          "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2", "-t", f"{dur:.3f}", tmp], stdin=subprocess.PIPE)
    n = int(round(dur * FPS))
    for i in range(n): p.stdin.write(frame(fig, name, i / FPS, q).tobytes())
    p.stdin.close()
    if p.wait() != 0: sys.exit("ffmpeg failed " + name)
    os.replace(tmp, f"{out}/{name}.mp4"); print(name, "done", n, "frames", flush=True)

if __name__ == "__main__":
    mode, out = sys.argv[1], sys.argv[2]
    if mode == "stills":
        from PIL import Image
        fig = plt.figure(figsize=(W / 100, H / 100), dpi=100)
        for name in "abcdefg":
            q = Cues(name)
            for j, fr in enumerate((0.45, 0.97)):
                Image.fromarray(frame(fig, name, q.dur * fr, q)).resize((960, 540)).save(f"{out}/st_{name}{j}.jpg", quality=85)
    else:
        for name in sys.argv[3:]: render(name, out)
