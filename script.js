const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const laneWidth = canvas.width / 4;
const hitZoneY = canvas.height - 100;
let arrows = [];
let lastSpawn = 0;
let score = 0;

function spawnArrow() {
  const dirIndex = Math.floor(Math.random() * 4);
  arrows.push({ x: dirIndex * laneWidth + laneWidth / 2, y: 0, dir: ['left','down','up','right'][dirIndex] });
}

function drawArrow(arrow) {
  ctx.fillStyle = 'white';
  ctx.beginPath();
  ctx.moveTo(arrow.x, arrow.y);
  ctx.lineTo(arrow.x - 20, arrow.y - 30);
  ctx.lineTo(arrow.x + 20, arrow.y - 30);
  ctx.closePath();
  ctx.fill();
}

function update(dt) {
  if (Date.now() - lastSpawn > 800) {
    spawnArrow();
    lastSpawn = Date.now();
  }
  arrows.forEach(a => a.y += dt * 0.3);
  arrows = arrows.filter(a => a.y < canvas.height + 40);
}

function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.strokeStyle = '#555';
  for (let i=1;i<4;i++) {
    ctx.beginPath();
    ctx.moveTo(i*laneWidth, 0);
    ctx.lineTo(i*laneWidth, canvas.height);
    ctx.stroke();
  }
  ctx.fillStyle = '#444';
  ctx.fillRect(0, hitZoneY-10, canvas.width, 20);
  arrows.forEach(drawArrow);
  ctx.fillStyle = 'white';
  ctx.fillText('Score: '+score, 10, 20);
}

function gameLoop() {
  const now = Date.now();
  const dt = now - (gameLoop.last || now);
  gameLoop.last = now;
  update(dt);
  draw();
  requestAnimationFrame(gameLoop);
}

document.addEventListener('keydown', e => {
  const dirMap = {
    ArrowLeft: 'left',
    ArrowDown: 'down',
    ArrowUp: 'up',
    ArrowRight: 'right'
  };
  const dir = dirMap[e.code];
  if (!dir) return;
  let hit = false;
  arrows.forEach((a, idx) => {
    if (a.dir === dir && Math.abs(a.y - hitZoneY) < 40) {
      arrows.splice(idx,1);
      score++;
      hit = true;
      const utter = new SpeechSynthesisUtterance(dir);
      speechSynthesis.speak(utter);
    }
  });
  if (!hit) {
    score = Math.max(0, score-1);
  }
});

gameLoop();
