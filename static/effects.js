/* =====================================
   Animated Background (Dark Mode Only)
   File: effects.js
===================================== */

const canvas = document.createElement("canvas");
canvas.id = "bg-effects";
document.body.prepend(canvas);

const ctx = canvas.getContext("2d");

let width, height;
function resizeCanvas() {
  width = canvas.width = window.innerWidth;
  height = canvas.height = window.innerHeight;
}
resizeCanvas();
window.addEventListener("resize", resizeCanvas);

/* =====================================
   PARTICLES CONFIG
===================================== */
const PARTICLE_COUNT = 90;
const particles = [];

function initParticles() {
  particles.length = 0;
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    particles.push({
      x: Math.random() * width,
      y: Math.random() * height,
      vx: (Math.random() - 0.5) * 0.6,
      vy: (Math.random() - 0.5) * 0.6,
      r: Math.random() * 2 + 1,
    });
  }
}

initParticles();

/* =====================================
   ANIMATION LOOP
===================================== */
function animate() {
  const isLight = document.body.classList.contains("light");

  ctx.clearRect(0, 0, width, height);

  // ❌ Disable particles in LIGHT MODE
  if (!isLight) {
    ctx.fillStyle = "#38bdf8";

    particles.forEach((p) => {
      p.x += p.vx;
      p.y += p.vy;

      if (p.x < 0 || p.x > width) p.vx *= -1;
      if (p.y < 0 || p.y > height) p.vy *= -1;

      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fill();
    });
  }

  requestAnimationFrame(animate);
}

animate();

/* =====================================
   CANVAS STYLE
===================================== */
canvas.style.position = "fixed";
canvas.style.top = "0";
canvas.style.left = "0";
canvas.style.zIndex = "-1";
canvas.style.pointerEvents = "none";
canvas.style.background = "transparent";

/* =====================================
   THEME TOGGLE (NO CHANGE)
===================================== */
window.toggleTheme = function () {
  document.body.classList.toggle("light");
};
