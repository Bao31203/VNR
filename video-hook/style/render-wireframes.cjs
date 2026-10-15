// Vẽ wireframe cho từng cảnh từ video-style.json -> wireframes/C01.jpg ... và tong-quan.jpg
// Chạy: node render-wireframes.cjs
const path = require('path');
const fs = require('fs');
const { execSync } = require('child_process');
const { createRequire } = require('module');

let chromium;
try { ({ chromium } = require('playwright')); }
catch { ({ chromium } = createRequire(path.join(execSync('npm root -g').toString().trim(), 'x'))('playwright')); }

const style = JSON.parse(fs.readFileSync(path.join(__dirname, 'video-style.json'), 'utf8'));
const OUT = path.join(__dirname, 'wireframes');
fs.mkdirSync(OUT, { recursive: true });

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1180 } });
  await page.addInitScript(s => { window.STYLE = s; }, style);
  const files = [];
  for (const sc of style.scenes) {
    await page.goto('file://' + path.join(__dirname, 'wireframe.html') + '?scene=' + sc.id);
    await page.waitForFunction(() => window.READY === true);
    await page.evaluate(() => document.fonts.ready);
    const file = path.join(OUT, sc.id.replace(/^C(\d)$/, 'C0$1') + '.jpg');
    await page.screenshot({ path: file, type: 'jpeg', quality: 88 });
    files.push(file);
  }
  await browser.close();

  // Ảnh tổng quan: lưới 3 cột
  const inputs = files.map(f => `-i "${f}"`).join(' ');
  const cols = 3, w = 640, h = Math.round(1180 * w / 1920);
  const scaled = files.map((_, i) => `[${i}]scale=${w}:${h}[s${i}]`).join(';');
  const pad = files.length % cols ? cols - (files.length % cols) : 0;
  let layout = [], labels = '';
  files.forEach((_, i) => { layout.push(`${(i % cols) * w}_${Math.floor(i / cols) * h}`); labels += `[s${i}]`; });
  let filter = `${scaled};${labels}xstack=inputs=${files.length}:layout=${layout.join('|')}:fill=black`;
  if (pad) filter += `[x];[x]pad=${cols * w}:${Math.ceil(files.length / cols) * h}:0:0:black`;
  execSync(`ffmpeg -loglevel error -y ${inputs} -filter_complex "${filter}" "${path.join(OUT, 'tong-quan.jpg')}"`);
  console.log('Xong:', files.length, 'cảnh + tong-quan.jpg');
})();
