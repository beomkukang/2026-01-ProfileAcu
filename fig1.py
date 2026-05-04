import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import Axes3D, proj3d
from matplotlib import rcParams

rcParams['font.family'] = 'Liberation Serif'

CA = '#5B8EC2'; CB = '#8EC8E0'
CC = '#D46A5F'; CD = '#E8A96A'
AX_C = (0.40, 0.40, 0.45, 0.72)
EDGE = (0.52, 0.52, 0.57, 0.58)

class Arrow3D(FancyArrowPatch):
    def __init__(self, p0, p1, *args, **kwargs):
        super().__init__((0,0),(0,0), *args, **kwargs)
        self._p0 = p0; self._p1 = p1
    def do_3d_projection(self, renderer=None):
        xs, ys, zs = proj3d.proj_transform(
            [self._p0[0], self._p1[0]],
            [self._p0[1], self._p1[1]],
            [self._p0[2], self._p1[2]], self.axes.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        return min(zs)

def sph(el, az):
    el, az = np.radians(el), np.radians(az)
    return np.array([np.cos(el)*np.cos(az),
                     np.cos(el)*np.sin(az),
                     np.sin(el)])

def draw_vec(ax, v, color, s=0.82):
    vn = v / np.linalg.norm(v)
    p1 = vn * s
    ax.add_artist(Arrow3D((0,0,0),(p1[0],p1[1],p1[2]),
                          arrowstyle='-|>', mutation_scale=18,
                          lw=2.2, color=color,
                          shrinkA=0, shrinkB=0, zorder=7))

def draw_arc(ax, v1, v2, r, col, lw=1.8):
    n1 = v1/np.linalg.norm(v1); n2 = v2/np.linalg.norm(v2)
    perp = n2 - np.dot(n2,n1)*n1
    nm = np.linalg.norm(perp)
    if nm < 1e-8: return
    perp /= nm
    ang = np.arccos(np.clip(np.dot(n1,n2),-1,1))
    t   = np.linspace(0, ang, 60)
    pts = r*(np.outer(np.cos(t),n1) + np.outer(np.sin(t),perp))
    ax.plot(pts[:,0], pts[:,1], pts[:,2],
            color=col, lw=lw, linestyle='--', alpha=0.85, zorder=6)

# ── Vectors ───────────────────────────────────────────────────────────
vA = sph(55,  3);  vB = sph(18,  8)   # A-B: ~37°
vC = sph(55, 82);  vD = sph(22, 87)   # C-D: ~35°

# ── Figure ────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(5.5, 5.5), facecolor='white')
ax  = fig.add_axes([0.05, 0.05, 0.90, 0.90], projection='3d')

ax.set_xlim(0,1.25); ax.set_ylim(0,1.25); ax.set_zlim(0,1.25)
ax.set_box_aspect([1,1,1])
ax.axis('off')
ax.view_init(elev=28, azim=45)
for pane in [ax.xaxis.pane, ax.yaxis.pane, ax.zaxis.pane]:
    pane.fill = False; pane.set_edgecolor('none')

# quarter sphere surface
u = np.linspace(0, np.pi/2, 60); v = np.linspace(0, np.pi/2, 60)
ax.plot_surface(np.outer(np.cos(u), np.sin(v)),
                np.outer(np.sin(u), np.sin(v)),
                np.outer(np.ones(len(u)), np.cos(v)),
                color=(0.92,0.92,0.92), alpha=0.05,
                linewidth=0, zorder=0, rcount=60, ccount=60)

# boundary edges
t = np.linspace(0, np.pi/2, 120)
for xs,ys,zs in [(np.cos(t),np.sin(t),np.zeros(120)),
                 (np.sin(t),np.zeros(120),np.cos(t)),
                 (np.zeros(120),np.sin(t),np.cos(t))]:
    ax.plot(xs, ys, zs, color=EDGE, lw=1.0, zorder=2)

# axes (no labels)
lim = 1.22
for d in [([lim,0,0]), ([0,lim,0]), ([0,0,lim])]:
    ax.add_artist(Arrow3D((0,0,0), tuple(d),
                          arrowstyle='-|>', mutation_scale=8,
                          lw=0.9, color=AX_C,
                          shrinkA=0, shrinkB=0, zorder=3))

# vectors
draw_vec(ax, vA, CA); draw_vec(ax, vB, CB)
draw_vec(ax, vC, CC); draw_vec(ax, vD, CD)

# dashed arcs
draw_arc(ax, vA, vB, r=0.24, col=CA)
draw_arc(ax, vC, vD, r=0.34, col=CC)

plt.savefig('fig1_conceptual.png',
            dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
print("Done.")