
import streamlit as st
import streamlit.components.v1 as components
import math
import json

st.set_page_config(
    page_title="For Rava ❤️",
    page_icon="❤️",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: #100713;
}
header, footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

def heart_points(name="rava", layers=7, n=420):
    points = []
    chars = [c for c in name.lower() if c != " "]

    for li in range(layers):
        z = (li - (layers - 1) / 2) * 0.55 / (layers - 1)
        shrink = 1.0 - 0.06 * abs(li - (layers - 1) / 2)

        for i in range(n):
            t = 2 * math.pi * i / n

            hx = 16 * math.sin(t) ** 3
            hy = (
                13 * math.cos(t)
                - 5 * math.cos(2*t)
                - 2 * math.cos(3*t)
                - math.cos(4*t)
            )

            x = hx * 0.07 * shrink
            y = -hy * 0.07 * shrink
            ch = chars[i % len(chars)]

            points.append([x, y, z, ch])

    return points


points = json.dumps(heart_points())

html = """
<!DOCTYPE html>
<html>
<head>
<style>
body {
    margin: 0;
    background: #100713;
    overflow: hidden;
}
canvas {
    display: block;
    width: 100%;
    height: 560px;
}
</style>
</head>
<body>

<canvas id="heart"></canvas>

<script>
const canvas = document.getElementById("heart");
const ctx = canvas.getContext("2d");

const points = POINTS_DATA;

function resize() {
    const dpr = window.devicePixelRatio || 1;
    canvas.width = canvas.clientWidth * dpr;
    canvas.height = canvas.clientHeight * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
}

window.addEventListener("resize", resize);
resize();

let angle = 0;

function animate() {
    const w = canvas.clientWidth;
    const h = canvas.clientHeight;

    ctx.clearRect(0, 0, w, h);

    const ca = Math.cos(angle);
    const sa = Math.sin(angle);
    const ct = Math.cos(0.35);
    const st = Math.sin(0.35);

    let projected = [];

    for (const [x, y, z, ch] of points) {
        const rx = x * ca + z * sa;
        const rz = -x * sa + z * ca;

        const ry = y * ct - rz * st;
        const rz2 = y * st + rz * ct;

        const perspective = 1 / (1 - rz2 * 0.12);

        projected.push({
            x: rx,
            y: ry,
            z: rz2,
            ch: ch,
            scale: perspective
        });
    }

    projected.sort((a, b) => a.z - b.z);

    for (const p of projected) {
        const px = w/2 + p.x * 25 * p.scale;
        const py = h/2 + p.y * 25 * p.scale;

        if (p.z > 0.15) {
            ctx.fillStyle = "#ffffff";
        } else if (p.z > -0.15) {
            ctx.fillStyle = "#ff8bd5";
        } else {
            ctx.fillStyle = "#ff1744";
        }

        ctx.font = "bold 12px monospace";
        ctx.fillText(p.ch, px, py);
    }

    angle += 0.025;
    requestAnimationFrame(animate);
}

animate();
</script>
</body>
</html>
"""

html = html.replace("POINTS_DATA", points)

components.html(html, height=580, scrolling=False)

st.markdown(
    "<h3 style='text-align:center;color:#ff8bd5;'>"
    "Made with love ❤️</h3>",
    unsafe_allow_html=True
)
