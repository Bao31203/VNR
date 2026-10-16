// Xuất từng khung hình của trang dựng (templates/history-v4 hoặc history-v7) bằng Chromium.
//
//   node v7/xuat-hinh.cjs --template <index.html> --vars <variables.json> --png <thư mục> --frames 100,250,900
//   node v7/xuat-hinh.cjs --template <index.html> --vars <variables.json> --video <ra.mp4> [--workers 4] [--crf 18]
//
// Trang dựng phải có window.seek(giây); nếu có window.__ready() thì chờ nó (ảnh phim tư liệu đã giải mã) trước khi chụp.
const {chromium} = require(process.env.PLAYWRIGHT_MODULE || '/opt/node-tools/node_modules/playwright');
const {spawn} = require('node:child_process');
const fs = require('node:fs');
const path = require('node:path');
const {pathToFileURL} = require('node:url');

const argv = process.argv.slice(2);
const opt = name => { const i = argv.indexOf('--' + name); return i < 0 ? undefined : argv[i + 1]; };
const template = path.resolve(opt('template'));
const variables = JSON.parse(fs.readFileSync(path.resolve(opt('vars')), 'utf8'));
const fps = 30;
const total = Math.round(JSON.parse(variables.timeline_json).duration * fps);
const workers = Number(opt('workers') || 4);
const crf = opt('crf') || '18';

async function openPage(browser) {
  const page = await browser.newPage({viewport: {width: 1920, height: 1080}, deviceScaleFactor: 1});
  await page.addInitScript(v => { window.VNR_PREVIEW = v; }, variables);
  await page.goto(pathToFileURL(template).href, {waitUntil: 'load'});
  await page.evaluate(async () => { await document.fonts.ready; await Promise.all([...document.images].map(i => i.decode().catch(() => {}))); });
  return page;
}
async function shoot(page, frame, type = 'jpeg') {
  await page.evaluate(async t => { window.seek(t); if (window.__ready) await window.__ready(); }, frame / fps);
  return page.screenshot(type === 'png' ? {type: 'png'} : {type: 'jpeg', quality: 95});
}

(async () => {
  const browser = await chromium.launch({executablePath: process.env.CHROMIUM_PATH || undefined, args: ['--allow-file-access-from-files', '--disable-web-security']});
  if (opt('png')) {
    const dir = path.resolve(opt('png')); fs.mkdirSync(dir, {recursive: true});
    const frames = opt('frames').split(',').map(Number);
    const page = await openPage(browser);
    for (const f of frames) fs.writeFileSync(path.join(dir, `f${String(f).padStart(5, '0')}.png`), await shoot(page, f, 'png'));
    console.log(`Đã xuất ${frames.length} khung vào ${dir}`);
  } else {
    const out = path.resolve(opt('video'));
    const parts = [];
    const chunk = Math.ceil(total / workers);
    const started = Date.now();
    let done = 0;
    await Promise.all(Array.from({length: workers}, async (_, w) => {
      const from = w * chunk, to = Math.min(total, from + chunk);
      if (from >= to) return;
      const part = `${out}.part${w}.mp4`; parts[w] = part;
      const page = await openPage(browser);
      const ff = spawn('ffmpeg', ['-y', '-v', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-',
        '-c:v', 'libx264', '-preset', 'medium', '-crf', crf, '-pix_fmt', 'yuv420p', '-r', String(fps),
        '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709', part], {stdio: ['pipe', 'inherit', 'inherit']});
      const finished = new Promise((ok, fail) => ff.on('close', c => c === 0 ? ok() : fail(new Error('ffmpeg ' + c))));
      for (let f = from; f < to; f++) {
        const jpg = await shoot(page, f);
        if (!ff.stdin.write(jpg)) await new Promise(r => ff.stdin.once('drain', r));
        if (++done % 300 === 0) console.log(`${done}/${total} khung, ${((Date.now() - started) / 1000).toFixed(0)} s`);
      }
      ff.stdin.end(); await finished; await page.close();
    }));
    const list = `${out}.parts.txt`;
    fs.writeFileSync(list, parts.filter(Boolean).map(p => `file '${p.replaceAll("'", "'\\''")}'`).join('\n'));
    await new Promise((ok, fail) => spawn('ffmpeg', ['-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', list, '-c', 'copy', '-movflags', '+faststart', out], {stdio: 'inherit'})
      .on('close', c => c === 0 ? ok() : fail(new Error('concat ' + c))));
    for (const p of parts.filter(Boolean)) fs.unlinkSync(p);
    fs.unlinkSync(list);
    console.log(`Xong ${total} khung → ${out} (${((Date.now() - started) / 1000).toFixed(0)} s)`);
  }
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
