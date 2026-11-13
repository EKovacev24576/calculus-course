import sys, os, math, subprocess
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
from render import (Cues, T, fade, ease, lerp, clamp, dot, W, H, FPS, PAD, BG, INK, MUTE, TURQ, CORAL, YEL, GRID, HERE)

PANEL = "#16223A"
def F(x): return x * x + 1

def header(fig):
    fig.text(0.04, 0.945, "1.1  REVIEW OF FUNCTIONS", color=MUTE, fontsize=17, fontweight="bold")
    fig.text(0.245, 0.945, "LEVEL 1  ·  THE IDEA", color=TURQ, fontsize=17, fontweight="bold")

def canvas(fig):
    ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off"); ax.set_xlim(0, 16); ax.set_ylim(0, 9); return ax

def box(ax, x, y, w, h, fc=PANEL, ec=TURQ, a=1.0, lw=3, r=0.35):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec, lw=lw, alpha=clamp(a)))

def txt(ax, x, y, s, a=1.0, size=34, c=INK, w="medium", ha="center"):
    if a > 0.01: ax.text(x, y, s, color=c, fontsize=size, fontweight=w, alpha=clamp(a), ha=ha, va="center")

def arrow(ax, x0, x1, y, a=1.0, c=MUTE):
    if a > 0.01: ax.annotate("", xy=(x1, y), xytext=(x0, y), arrowprops=dict(arrowstyle="-|>", color=c, lw=4, alpha=clamp(a), mutation_scale=34))

def axes(fig, rect=(0.07, 0.13, 0.55, 0.72), a=1.0, xlim=(-3.2, 3.2), ylim=(-0.6, 10.6), yt=None):
    ax = fig.add_axes(rect); ax.set_facecolor(BG); ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    for sp in ("top", "right", "left", "bottom"): ax.spines[sp].set_visible(False)
    ax.axhline(0, color=MUTE, lw=2.5, alpha=a, zorder=2); ax.axvline(0, color=MUTE, lw=2.5, alpha=a, zorder=2)
    ax.set_xticks(range(int(math.ceil(xlim[0])), int(xlim[1]) + 1)); ax.set_yticks(yt if yt is not None else range(0, 11, 2))
    ax.tick_params(colors=MUTE, labelsize=20, length=0)
    for l in ax.get_xticklabels() + ax.get_yticklabels(): l.set_alpha(a)
    ax.grid(True, color=GRID, lw=1.5, alpha=a); ax.set_axisbelow(True)
    return ax

def parab(ax, upto=1.0, a=1.0):
    x = np.linspace(-3.0, lerp(-3.0, 3.0, upto), 240)
    ax.plot(x, F(x), color=TURQ, lw=6, solid_capstyle="round", alpha=a, zorder=3)

def seg_a(fig, t, q):
    k0 = 1 - fade(t, 1.4, 0.5)
    T(fig, 0.5, 0.58, "What is a function?", k0, 76, INK, "bold", "center")
    T(fig, 0.5, 0.46, "Calculus 1  ·  Chapter 1  ·  Level 1", k0, 34, TURQ, "medium", "center")
    a = fade(t, 1.7, 0.6)
    if a < 0.01: return
    ax = canvas(fig)
    box(ax, 1.4, 1.3, 4.6, 6.2, a=a, ec=MUTE)
    lit = t > q("Press B4")
    for r in range(3):
        for c in range(3):
            on = lit and (r, c) == (1, 1)
            box(ax, 1.9 + c * 1.25, 5.6 - r * 1.25, 1.0, 1.0, fc=YEL if on else BG, ec=YEL if on else MUTE, a=a, lw=2, r=0.15)
            txt(ax, 2.4 + c * 1.25, 6.1 - r * 1.25, ("A", "B", "C")[r] + str(c + 3), a, 22, BG if on else MUTE, "bold")
    box(ax, 1.9, 1.75, 3.6, 0.9, fc=BG, ec=MUTE, a=a, lw=2, r=0.15)
    p = fade(t, q("you get pretzels"))
    arrow(ax, 6.3, 7.7, 4.4, p)
    box(ax, 8.0, 3.6, 3.2, 1.6, ec=CORAL, a=p); txt(ax, 9.6, 4.4, "pretzels", p, 36, CORAL, "bold")
    txt(ax, 3.7, 2.2, "B4", fade(t, q("Press B4")), 28, YEL, "bold")
    T(fig, 0.725, 0.66, "one input", fade(t, q("one input")), 36, YEL, "bold")
    T(fig, 0.725, 0.58, "exactly one output", fade(t, q("exactly one output")), 36, CORAL, "bold")
    T(fig, 0.725, 0.45, "= a function", fade(t, q("is a function")), 46, INK, "bold")

def machine(ax, a=1.0, rule=0.0):
    box(ax, 6.0, 3.2, 4.0, 3.0, a=a)
    txt(ax, 8.0, 5.15, "f", a, 80, TURQ, "bold")
    txt(ax, 8.0, 3.85, "square it, then add 1", rule, 24, INK)

def seg_b(fig, t, q):
    ax = canvas(fig); machine(ax, fade(t, 0.3), fade(t, q("This machine's rule")))
    txt(ax, 3.4, 6.6, "input", fade(t, q("A number goes in")), 28, MUTE); txt(ax, 12.6, 6.6, "output", fade(t, q("a number comes out")), 28, MUTE)
    rounds = [("2", "5", q("Put in two"), q("plus one is five", at="five")),
              ("3", "10", q("Put in three"), q("you get ten", at="ten")),
              ("−1", "2", q("Put in negative one"), q("you get two", at="two"))]
    for i, (xin, xout, ti, to) in enumerate(rounds):
        nxt = rounds[i + 1][2] if i + 1 < len(rounds) else 1e9
        if ti <= t < nxt:
            k = ease((t - ti) / 0.9); ko = ease((t - to) / 0.9)
            if t < to + 0.2: txt(ax, lerp(1.6, 5.2, k), 4.7, xin, 1 - fade(t, to - 0.1, 0.3) * 0.0, 76, YEL, "bold")
            arrow(ax, 4.0, 5.8, 4.7, 0.5 * (1 - k) if False else 0)
            if t > to: txt(ax, lerp(10.8, 13.4, ko), 4.7, xout, 1, 76, CORAL, "bold")
        y = 2.2 - i * 0.0
        r = fade(t, to + 0.4)
        txt(ax, 4.6 + i * 3.4, 1.5, f"{xin}", r, 34, YEL, "bold", "right"); txt(ax, 5.1 + i * 3.4, 1.5, r"$\rightarrow$", r, 38, MUTE); txt(ax, 5.6 + i * 3.4, 1.5, xout, r, 34, CORAL, "bold", "left")

def seg_c(fig, t, q):
    a = fade(t, q("f of x equals") - 0.2)
    T(fig, 0.5, 0.74, r"$f(x) = x^2 + 1$", a, 110, INK, "medium", "center")
    rows = [("f", "the machine's name", TURQ, q("f is the machine")), ("x", "whatever goes in", YEL, q("x is whatever")),
            ("f(x)", "what comes out", CORAL, q("And f of x is"))]
    for i, (s, d, c, tt) in enumerate(rows):
        b = fade(t, tt); y = 0.52 - i * 0.085
        T(fig, 0.40, y, s, b, 44, c, "bold", "right"); T(fig, 0.44, y, d, b, 36, INK)
    T(fig, 0.5, 0.17, r"$f(2) = 2^2 + 1 = 5$", fade(t, q("So f of two")), 76, YEL, "medium", "center")

PTS = [(-2, 5), (-1, 2), (0, 1), (1, 2), (2, 5)]
def seg_d(fig, t, q):
    t0 = q("a table") - 0.6
    T(fig, 0.10, 0.80, "x", fade(t, t0), 40, YEL, "bold", "center"); T(fig, 0.21, 0.80, "f(x)", fade(t, t0), 40, CORAL, "bold", "center")
    for i, (x, y) in enumerate(PTS):
        b = fade(t, t0 + 0.4 + i * 0.4, 0.3); yy = 0.70 - i * 0.095
        T(fig, 0.10, yy, str(x).replace("-", "−"), b, 40, INK, "medium", "center"); T(fig, 0.21, yy, str(y), b, 40, INK, "medium", "center")
    ax = axes(fig, rect=(0.36, 0.13, 0.58, 0.72), a=fade(t, q("Each pair") - 0.5))
    tp = q("Plot them all")
    ex = fade(t, q("Each pair"))
    if ex > 0.01: dot(ax, 2, 5, YEL, 320, ex, 7)
    ac = ease((t - q("how far across")) / 0.8); up = ease((t - q("how far up")) / 0.8)
    if ac > 0: ax.plot([0, 2 * ac], [0, 0], color=YEL, lw=7, zorder=5, solid_capstyle="round")
    if up > 0: ax.plot([2, 2], [0, 5 * up], color=CORAL, lw=5, ls=(0, (3, 2)), zorder=5)
    if ex > 0.01: ax.text(2.18, 5.5, "(2, 5)", color=YEL, fontsize=28, fontweight="bold", alpha=ex)
    for i, (x, y) in enumerate(PTS):
        if (x, y) != (2, 5): dot(ax, x, y, INK, 260, fade(t, tp + i * 0.22, 0.25))
    c = ease((t - q("fill in every input")) / 2.4)
    if c > 0: parab(ax, c)
    g = fade(t, q("the graph of the function"))
    if g > 0.01: ax.text(0.25, 9.9, "the graph of f", color=TURQ, fontsize=30, fontweight="bold", alpha=g, ha="left", va="center")

def seg_e(fig, t, q):
    sw = q("But a circle"); k = fade(t, sw - 0.2, 0.6)
    rect = (0.07, 0.13, 0.55, 0.72)
    if k < 0.99:
        ax = axes(fig, rect, a=1 - k); parab(ax, 1.0, 1 - k)
        v0, v1 = q("any vertical line"), q("This curve passes")
        if t > v0:
            x = lerp(-2.6, 2.6, ease((t - v0) / (v1 - v0 + 0.8)))
            ax.axvline(x, color=YEL, lw=4, alpha=1 - k, zorder=4); dot(ax, x, F(x), YEL, 320, 1 - k)
        T(fig, 0.66, 0.60, "crosses once", fade(t, v0 + 1.2) * (1 - k), 40, INK)
        T(fig, 0.66, 0.50, "a function", fade(t, v1) * (1 - k), 52, TURQ, "bold")
    if k > 0.01:
        ax = axes(fig, rect, a=k, xlim=(-3.2, 3.2), ylim=(-2.358, 2.358), yt=range(-2, 3))
        th = np.linspace(0, 2 * math.pi, 240); ax.plot(2 * np.cos(th), 2 * np.sin(th), color=TURQ, lw=6, alpha=k, zorder=3)
        v = fade(t, q("One input"))
        if v > 0.01:
            ax.axvline(1, color=YEL, lw=4, alpha=v, zorder=4)
            tw = fade(t, q("two outputs"))
            dot(ax, 1, math.sqrt(3), CORAL, 340, tw); dot(ax, 1, -math.sqrt(3), CORAL, 340, tw)
        T(fig, 0.66, 0.66, "one input", fade(t, q("One input")), 40, YEL, "bold")
        T(fig, 0.66, 0.57, "two outputs", fade(t, q("two outputs")), 40, CORAL, "bold")
        T(fig, 0.66, 0.42, "not a function", fade(t, q("is not a function")), 52, CORAL, "bold")
    T(fig, 0.66, 0.80, "Vertical line test", fade(t, q("any vertical line")), 34, MUTE)

def seg_f(fig, t, q):
    ax = axes(fig); parab(ax)
    d = ease((t - q("The domain")) / 1.0)
    if d > 0: ax.plot([-3.15 * d, 3.15 * d], [0, 0], color=YEL, lw=9, zorder=5, solid_capstyle="round")
    r = ease((t - q("The range")) / 1.0)
    if r > 0:
        ax.plot([0, 0], [1, lerp(1, 10.5, r)], color=CORAL, lw=9, zorder=5, solid_capstyle="round"); dot(ax, 0, 1, CORAL, 300, 1, 7)
    T(fig, 0.66, 0.78, "domain", fade(t, q("The domain")), 50, YEL, "bold")
    T(fig, 0.66, 0.705, "every input it accepts", fade(t, q("every input")), 30, INK)
    T(fig, 0.66, 0.60, "range", fade(t, q("The range")), 50, CORAL, "bold")
    T(fig, 0.66, 0.525, "every output it can produce", fade(t, q("every output")), 30, INK)
    T(fig, 0.66, 0.36, "domain:  all real numbers", fade(t, q("so the domain")), 34, YEL, "medium")
    T(fig, 0.66, 0.27, "range:  1 and up", fade(t, q("so the range")), 34, CORAL, "medium")
    T(fig, 0.735, 0.19, r"$[1, \infty)$", fade(t, q("so the range") + 0.8), 40, CORAL)

def seg_g(fig, t, q):
    a = fade(t, q("a function is"))
    T(fig, 0.5, 0.80, "A function", a, 68, YEL, "bold", "center")
    T(fig, 0.5, 0.69, "a rule that gives each input exactly one output", fade(t, q("a rule")), 42, INK, "medium", "center")
    ax = canvas(fig)
    for i, (w, cue) in enumerate([("machine", "a machine"), ("formula", "a formula"), ("table", "a table"), ("graph", "or a graph")]):
        b = fade(t, q(cue)); x = 2.6 + i * 2.8
        box(ax, x, 4.0, 2.4, 1.0, ec=TURQ, a=b, lw=2.5, r=0.3); txt(ax, x + 1.2, 4.5, w, b, 30, INK)
    T(fig, 0.5, 0.33, "Calculus  =  how functions change", fade(t, q("Calculus is")), 44, TURQ, "medium", "center")
    n = fade(t, q("In level two"))
    box(ax, 3.4, 0.5, 9.2, 0.8, ec=TURQ, a=n, lw=2.5, r=0.3)
    T(fig, 0.5, 0.10, "Next  ·  Level 2: domain, range, combining, symmetry", n, 28, TURQ, "bold", "center")

SEGS = {"a": seg_a, "b": seg_b, "c": seg_c, "d": seg_d, "e": seg_e, "f": seg_f, "g": seg_g}

def frame(fig, name, t, q):
    fig.clf(); fig.patch.set_facecolor(BG)
    if not (name == "a" and t < 1.7): header(fig)
    SEGS[name](fig, t, q); fig.canvas.draw()
    return np.asarray(fig.canvas.buffer_rgba())[:, :, :3]

def render(name, out):
    q = Cues("s11" + name); dur = q.dur + PAD; fig = plt.figure(figsize=(W / 100, H / 100), dpi=100)
    tmp = f"{out}/s11{name}.tmp.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                          "-i", "-", "-i", f"{HERE}/vo/s11{name}.mp3", "-af", f"apad=whole_dur={dur}", "-c:v", "libx264", "-crf", "18", "-preset", "veryfast",
                          "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2", "-t", f"{dur:.3f}", tmp], stdin=subprocess.PIPE)
    n = int(round(dur * FPS))
    for i in range(n): p.stdin.write(frame(fig, name, i / FPS, q).tobytes())
    p.stdin.close()
    if p.wait() != 0: sys.exit("ffmpeg failed " + name)
    os.replace(tmp, f"{out}/s11{name}.mp4"); print(name, "done", n, flush=True)

if __name__ == "__main__":
    mode, out = sys.argv[1], sys.argv[2]
    if mode == "stills":
        from PIL import Image
        fig = plt.figure(figsize=(W / 100, H / 100), dpi=100)
        for name in "abcdefg":
            q = Cues("s11" + name)
            for j, fr in enumerate((0.5, 0.98)):
                Image.fromarray(frame(fig, name, q.dur * fr, q)).resize((960, 540)).save(f"{out}/t_{name}{j}.jpg", quality=85)
    else:
        for name in sys.argv[3:]: render(name, out)
