#!/usr/bin/env python3
"""뒷면 로고를 '음각(블라인드 디보싱)'으로 바꾸고, 종이 질감 타일을 만든다.
사용: python3 tools/deboss.py   (assets/card-logo.png → assets/card-back-deboss.png, assets/paper.png)"""
import pathlib, numpy as np
from PIL import Image, ImageFilter
A = pathlib.Path(__file__).resolve().parent.parent / "assets"
src = Image.open(A / "card-logo.png").convert("RGBA")
rgb = np.asarray(src, dtype=np.float32)
alpha = rgb[..., 3]
lum = rgb[..., :3].mean(-1)
logo = ((lum < 70) & (alpha > 0)).astype(np.float32)          # 검은 로고 영역 = 눌릴 영역
paper = np.median(rgb[(logo == 0) & (alpha > 200)][:, :3], axis=0)  # 명함 바탕색

def blur(a, r):
    return np.asarray(Image.fromarray((a * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(r)), dtype=np.float32) / 255

h = -blur(logo, 8)                     # 눌린 높이맵
gy, gx = np.gradient(h)
L = np.array([-0.6, -0.8])             # 빛: 왼쪽 위
shade = -(gx * L[0] + gy * L[1]) * 14   # 벽면 명암
floor = blur(logo, 2)
inner = np.clip(blur(logo, 3) - blur(logo, 10), 0, 1)       # 가장자리 안쪽 그림자
f = 1 + np.clip(shade, -0.4, 0.4) - 0.07 * floor - 0.08 * inner
out = np.empty_like(rgb)
out[..., :3] = np.clip(paper[None, None, :] * f[..., None], 0, 255)
out[..., 3] = alpha
Image.fromarray(out.astype(np.uint8), "RGBA").save(A / "card-back-deboss.png", optimize=True)

# 종이 질감 타일 (펠트/코튼지 느낌의 미세 결 + 섬유) — 흰/검 점의 투명도로만 표현
rng = np.random.default_rng(7); N = 512
n = rng.normal(0, 1, (N, N)).astype(np.float32)
def tblur(a, r):  # 타일 이음새 없는 블러
    big = np.tile(a, (3, 3)); im = Image.fromarray(((big - big.min()) / (np.ptp(big)) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(r))
    b = np.asarray(im, dtype=np.float32)[N:2*N, N:2*N] / 255; return (b - b.mean()) / (b.std() + 1e-6)
g = 0.55 * tblur(n, 0.6) + 0.35 * tblur(rng.normal(0, 1, (N, N)), 1.6) + 0.25 * tblur(rng.normal(0, 1, (N, N)), 5)
for _ in range(900):  # 짧은 섬유
    x, y = rng.integers(0, N, 2); ang = rng.uniform(0, np.pi); ln = rng.integers(6, 22); s = rng.choice([-1, 1]) * rng.uniform(0.6, 1.4)
    for t in range(ln):
        g[int(y + t * np.sin(ang)) % N, int(x + t * np.cos(ang)) % N] += s
tex = np.zeros((N, N, 4), np.float32)
light = np.clip(g, 0, None); dark = np.clip(-g, 0, None)
tex[..., :3] = np.where(g[..., None] > 0, 255, 0)
tex[..., 3] = np.clip(np.where(g > 0, light * 9, dark * 12), 0, 40)
Image.fromarray(tex.astype(np.uint8), "RGBA").save(A / "paper.png", optimize=True)
print("ok", paper)
