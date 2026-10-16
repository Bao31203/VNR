// Dựng lại timeline.json và variables.json của V6 (repo không có hai file này vì nằm trong out/ bị bỏ qua).
//
// Cách làm: chạy lại đúng logic `--prepare` của scripts/render-history-v4.ts (biên dịch chữ đánh máy,
// mốc xuất hiện, hạt ngẫu nhiên), cộng thêm bước của render-history-v6.ts (C7 dài thêm 5 giây).
// Phần duy nhất cần file giọng đọc gốc là thời lượng từng cảnh; thời lượng đó đã đo lại từ
// out/history-1946-v6/hook.mp4 theo từng khung hình (xem MEASURED_FRAMES).
//
// Dùng: node v7/dung-lai-timeline-v6.mjs <thư mục ra>
import {readFileSync, writeFileSync, mkdirSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {join, resolve} from 'node:path';

const root = resolve(import.meta.dirname, '..');
const outDir = resolve(process.argv[2] || join(root, 'out/history-1946-v7/build'));
const style = JSON.parse(readFileSync(join(root, 'style/video-style.json'), 'utf8'));
style.textStyles.comparisonForce = {font:'sans',weight:700,size:36,color:'cream',shadow:'0 2px 12px rgba(0,0,0,.95)'};
const audioConfig = JSON.parse(readFileSync(join(root, 'production/history-v2-audio.json'), 'utf8'));
const fps = 30;
const frameTime = seconds => Math.ceil(seconds * fps - 1e-7) / fps;

// Thời lượng cảnh của V4/V5 (trước khi V6 kéo dài C7), tính bằng khung hình, đo từ hook.mp4 của V6:
// nền cảnh trước biến mất đúng khung đầu của cảnh sau, chớp sáng C3, màn đen C4/C5 và C7, đỉnh màu đỏ C8.
const MEASURED_FRAMES = {C1:176, C2:300, C3:360, C4:420, C5:270, C6:360, C7:265, C8:891, C9:390, C10:270, C11:180};
// Khung hình bắt đầu từng cảnh trong V6, dùng để tự kiểm tra kết quả.
const V6_START_FRAMES = {C1:0, C2:176, C3:476, C4:836, C5:1265, C6:1535, C7:1895, C8:2310, C9:3201, C10:3591, C11:3861};
const V6_TOTAL_FRAMES = 4116;

const assetMap = {A01:'a01.png',A02:'a02.png',A03:'a03.png',A04:'a04.png',A06:'a06.png',A07:'a07.png',A08:'a08.png',
  A09:'a09.png',A10:'a10.webp',A11a:'a11a.png',A11b:'a11b.png',A12:'a12.png',A13:'a13.png'};

function hash(value) { return createHash('sha256').update(value).digest('hex'); }
function seeded(seed) {
  let state = parseInt(hash(seed).slice(0, 8), 16) >>> 0;
  return () => { state ^= state << 13; state ^= state >>> 17; state ^= state << 5; return (state >>> 0) / 4294967296; };
}

const scenes = [];
let cursor = 0;
for (let i = 0; i < style.scenes.length; i++) {
  const scene = JSON.parse(JSON.stringify(style.scenes[i]));
  let duration = MEASURED_FRAMES[scene.id] / fps;
  if (scene.id === 'C10') duration = 9;
  if (scene.id === 'C8') {
    scene.background[0].title = 'Bản thảo Lời kêu gọi do người dùng cung cấp';
    scene.background[0].camera = 'static';
    delete scene.background[0].focus;
  }
  if (scene.id === 'C9') {
    scene.elements.push(
      {id:'c9-viet-quoc-quan',kind:'text',text:'2.500 vệ quốc quân',style:'comparisonForce',x:1014,y:666,w:856,align:'center',in:{t:5.6,preset:'type',charsPerSecond:70}},
      {id:'c9-tu-ve',kind:'text',text:'8.000 tự vệ',style:'comparisonForce',x:1014,y:718,w:856,align:'center',in:{t:8.1,preset:'type',charsPerSecond:55}}
    );
  }
  if (i === 7) {
    for (const cue of audioConfig.quoteCues) {
      const element = scene.elements.find(e => e.id === cue.id);
      element.in.t = scene.voStart + cue.start - audioConfig.clipStart;
      element.speechEnd = scene.voStart + cue.end - audioConfig.clipStart;
      if (element.in.preset === 'type') element.in.charsPerSecond = Array.from(element.text.normalize('NFC')).length / (.8 * (cue.end - cue.start));
    }
    const last = scene.elements.find(e => e.id === 'q9');
    const attribution = scene.elements.find(e => e.id === 'q-attr');
    attribution.in.t = last.in.t + (last.speechEnd - last.in.t) * .8 + .2;
    const computed = frameTime(Math.max(frameTime(scene.voStart + (audioConfig.clipEnd - audioConfig.clipStart) + .8), attribution.in.t + attribution.text.length / 30 + .8));
    if (computed !== duration) throw new Error(`C8: thời lượng tính được ${computed} khác thời lượng đo ${duration}`);
  }
  if (i === 4) cursor += .3;
  scene.start = frameTime(cursor); scene.duration = duration; scene.end = frameTime(scene.start + duration);
  scene.baseDuration = style.scenes[i].duration;

  // Giữ đúng thứ tự gọi random() như bản gốc (mỗi ký tự lấy thêm 2 số cho biến thể tiếng gõ).
  function event() {}
  function compile(element, parentStart = 0, inherited = undefined) {
    const config = element.in || inherited || {t: parentStart, preset: 'printed'};
    let local = typeof config.t === 'number' ? config.t : config.t === 'fromC2' ? -10 : parentStart;
    if (element.anchor === 'end') local += duration - scene.baseDuration;
    element.runtimeIn = local;
    element.runtimeOut = typeof element.out?.t === 'number' ? element.out.t : duration;
    element.runtimePreset = config.preset || 'printed';
    if (element.kind === 'group') {
      for (const child of element.children) compile(child, local);
    } else if (element.kind === 'node') {
      const fromPrevious = config.t === 'fromC2';
      element.date.kind = 'text'; element.desc.kind = 'text';
      compile(element.date, local, {t: fromPrevious ? -10 : local + .4, preset: fromPrevious ? 'printed' : 'type', charsPerSecond: config.charsPerSecond || 24});
      const next = element.date.charFrames?.length ? (element.date.charFrames.at(-1) / fps) + .2 : local;
      compile(element.desc, next, {t: fromPrevious ? -10 : next, preset: fromPrevious ? 'printed' : 'type', charsPerSecond: config.charsPerSecond || 24});
    } else if (element.kind === 'text' && element.runtimePreset === 'type') {
      const st = style.textStyles[element.style];
      const text = st.case === 'upper' ? element.text.toLocaleUpperCase('vi') : element.text;
      const chars = Array.from(text.normalize('NFC'));
      const random = seeded(`${scene.id}:${element.id || element.style}:${local}`);
      const cps = typeof config.charsPerSecond === 'number' ? config.charsPerSecond : 26;
      let at = local;
      element.charFrames = chars.map((character, j) => {
        if (j) at += (1 + (random() - .5) * .4) / cps;
        const f = Math.round(at * fps);
        event(character === ' ' ? 'type-space' : 'type-key', f / fps, {element: element.id, character, variant: Math.floor(random() * 6), pitch: .95 + random() * .1});
        return f;
      });
      element.cursorHold = config.cursorHoldAfter || .5;
    }
  }
  for (const element of scene.elements) compile(element);
  scenes.push(scene); cursor = scene.end;
}
const v4Duration = frameTime(cursor + 2.5);
const timeline = {fps, width:1920, height:1080, duration:v4Duration, templateId:'frame-vnr-history-v4', scenes,
  blackouts:[{start:0,end:.5},{start:scenes[3].end,end:scenes[4].start},{start:scenes[6].start,end:scenes[6].start+1},{start:cursor+1.5,end:v4Duration}],
  quietWindows:[{start:scenes[6].start+.04,end:scenes[6].start+1},{start:scenes[9].start+5.4,end:scenes[9].start+5.9}]};

// Bước của V6: C7 dài thêm 5 giây, các cảnh sau lùi lại 5 giây.
const hold = 5, oldC8Start = timeline.scenes[7].start;
timeline.scenes[6].duration += hold; timeline.scenes[6].end += hold;
for (const e of timeline.scenes[6].elements) if (e.out?.t === 'end') e.runtimeOut = timeline.scenes[6].duration;
for (const s of timeline.scenes.slice(7)) { s.start += hold; s.end += hold; }
timeline.duration += hold;
for (const q of [...timeline.blackouts, ...timeline.quietWindows]) if (q.start >= oldC8Start) { q.start += hold; q.end += hold; }
timeline.quietWindows[0].end = timeline.scenes[6].start + .915;

for (const s of timeline.scenes) {
  const frame = Math.round(s.start * fps);
  if (frame !== V6_START_FRAMES[s.id]) throw new Error(`${s.id} bắt đầu ở khung ${frame}, V6 là ${V6_START_FRAMES[s.id]}`);
}
if (Math.round(timeline.duration * fps) !== V6_TOTAL_FRAMES) throw new Error('Tổng số khung khác V6');
timeline.reconstructedFrom = 'out/history-1946-v6/hook.mp4 (đo khung hình) + scripts/render-history-v4.ts + render-history-v6.ts';

mkdirSync(outDir, {recursive: true});
const variables = {timeline_json: JSON.stringify(timeline), style_json: JSON.stringify(style), asset_map_json: JSON.stringify(assetMap)};
writeFileSync(join(outDir, 'timeline-v6.json'), JSON.stringify(timeline, null, 2));
writeFileSync(join(outDir, 'variables-v6.json'), JSON.stringify(variables));
console.log(JSON.stringify({duration: timeline.duration, frames: Math.round(timeline.duration * fps),
  starts: Object.fromEntries(timeline.scenes.map(s => [s.id, +s.start.toFixed(4)]))}));
