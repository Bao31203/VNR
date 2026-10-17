// Tạo variables.json cho V7: lấy timeline V6 dựng lại (dung-lai-timeline-v6.mjs), thay hình nền theo v7/canh-v7.json.
// Đồng thời tách khung hình các đoạn phim tư liệu ra JPG (cao 1080 px) để trang dựng hiển thị từng khung.
//
// Dùng: node v7/dung-v7.mjs                                        (V7, kết quả trong out/history-1946-v7/build/)
//       node v7/dung-v7.mjs v8/canh-v8.json out/history-1946-v8    (bản khác: file cảnh và thư mục ra riêng)
import {readFileSync, writeFileSync, existsSync, mkdirSync, readdirSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
import {join, resolve, relative} from 'node:path';

const root = resolve(import.meta.dirname, '..');
const [specFile = 'v7/canh-v7.json', outDir = 'out/history-1946-v7'] = process.argv.slice(2);
const build = join(resolve(root, outDir), 'build');
const templateDir = join(root, 'templates/history-v7');
execFileSync('node', [join(root, 'v7/dung-lai-timeline-v6.mjs'), build], {stdio: 'inherit'});
const variables = JSON.parse(readFileSync(join(build, 'variables-v6.json'), 'utf8'));
const timeline = JSON.parse(variables.timeline_json);
const spec = JSON.parse(readFileSync(resolve(root, specFile), 'utf8'));
const tag = spec._ma || 'v7';
const url = path => relative(templateDir, path).replaceAll('\\', '/');

function size(path) {
  const out = execFileSync('ffprobe', ['-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of', 'csv=p=0', path]).toString().trim();
  const [w, h] = out.split(',').map(Number);
  return {w, h};
}
function clipFrames(clip) {
  const dir = join(build, 'phim', clip);
  if (!existsSync(dir) || readdirSync(dir).length === 0) {
    mkdirSync(dir, {recursive: true});
    execFileSync('ffmpeg', ['-nostdin', '-v', 'error', '-i', join(root, 'assets/tu-lieu/phim', clip + '.mp4'),
      '-vf', 'scale=-2:1080:flags=lanczos', '-q:v', '2', '-start_number', '0', join(dir, '%04d.jpg')]);
  }
  return dir;
}

for (const scene of timeline.scenes) {
  const layers = spec.scenes[scene.id];
  if (!layers) continue;
  const old = scene.background;
  scene.background = layers.map(layer => {
    if (layer.keepV6 !== undefined) {
      const {keepV6, ...changes} = layer;
      return {...old[keepV6], ...changes};
    }
    const b = {...layer, asset: layer.kind};
    if (layer.kind === 'clip') {
      const dir = clipFrames(layer.clip);
      const first = join(dir, String(layer.frames[0]).padStart(4, '0') + '.jpg');
      b.dir = url(dir);
      b.aspect = (({w, h}) => w / h)(size(first));
    } else if (layer.kind === 'photo') {
      const path = join(root, 'assets/tu-lieu/anh', layer.photo);
      b.src = url(path);
      b.aspect = (({w, h}) => w / h)(size(path));
    }
    return b;
  });
}
timeline.templateId = 'vnr-history-v7';
timeline.visualRevision = spec._phienBan || 'V7: thay tranh AI bằng ảnh và phim tư liệu thật (đen trắng); cảnh chưa có tư liệu giữ tranh AI chuyển đen trắng';
variables.timeline_json = JSON.stringify(timeline);
writeFileSync(join(build, `timeline-${tag}.json`), JSON.stringify(timeline, null, 2));
writeFileSync(join(build, `variables-${tag}.json`), JSON.stringify(variables));
console.log(`Đã tạo ${join(build, `variables-${tag}.json`)}`);
