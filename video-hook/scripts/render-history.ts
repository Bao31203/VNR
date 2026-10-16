import { readFile, writeFile, mkdir, copyFile, cp } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { spawn } from 'node:child_process';
import { createHash } from 'node:crypto';
import { resolve, join } from 'node:path';
import { pathToFileURL } from 'node:url';

const root = resolve(import.meta.dirname, '..');
const tool = 'F:/AI-auto-generate-video';
const output = join(root, 'out/history-1946');
const spec = JSON.parse(await readFile(join(root, 'production/history-scenes.json'), 'utf8'));
const { OmniVoiceClient } = await import(pathToFileURL(join(tool, 'src/tts/omnivoice-client.ts')).href);
const { getDurationSec } = await import(pathToFileURL(join(tool, 'src/assets/audio-tools.ts')).href);
const { composeTemplate } = await import(pathToFileURL(join(tool, 'src/render/template-composer.ts')).href);

function run(command: string, args: string[], includeStderr = false): Promise<string> {
  return new Promise((accept, reject) => {
    const child = spawn(command, args, { cwd: root, windowsHide: true });
    let stdout = '', stderr = '';
    child.stdout.on('data', (data) => stdout += data);
    child.stderr.on('data', (data) => stderr += data);
    child.on('error', reject);
    child.on('close', (code) => code === 0 ? accept(stdout + (includeStderr ? stderr : '')) : reject(new Error(`${command} exited ${code}: ${stderr.slice(-3000)}`)));
  });
}
await mkdir(join(output, 'voice'), { recursive: true });
await mkdir(join(output, 'qa'), { recursive: true });

async function renderSubtitles() {
  // Keep both subtitle lines above the source/citation footer.
  await run('ffmpeg', ['-y', '-v', 'error', '-i', join(output, 'hook.mp4'), '-vf', "subtitles=filename=out/history-1946/hook.srt:fontsdir=templates/history/assets:force_style='FontName=Be Vietnam Pro,Fontsize=16,Alignment=2,MarginV=54,Outline=1.5,Shadow=0'", '-c:v', 'libx264', '-preset', 'fast', '-crf', '19', '-c:a', 'copy', '-movflags', '+faststart', join(output, 'hook-phude.mp4')]);
}

const args = process.argv.slice(2);
if (args.includes('--tts-only')) {
  for (const scene of spec.scenes) {
    const voiceId = scene.voice === 'quote' ? '6847be10-c45a-473a-b831-97167182997d' : '131af5c2-8d45-4733-8568-9e10166695ee';
    const voiceDir = join(tool, '.studio/voices', voiceId);
    const profile = JSON.parse(await readFile(join(voiceDir, 'profile.json'), 'utf8'));
    if (!profile.consent?.confirmed) throw new Error(`Voice has no saved consent: ${voiceId}`);
    const config = { endpoint: 'http://127.0.0.1:8123', refAudio: join(voiceDir, 'reference.wav'), refText: profile.referenceText, speed: scene.voice === 'quote' ? 0.94 : 1.0 };
    const identity = createHash('sha256').update(JSON.stringify({ config, text: scene.voiceText })).digest('hex');
    const audio = join(output, 'voice', `${scene.id}.mp3`);
    const manifest = `${audio}.json`;
    if (existsSync(audio) && existsSync(manifest) && JSON.parse(await readFile(manifest, 'utf8')).identity === identity) {
      console.log(`${scene.id}: reuse voice`); continue;
    }
    console.log(`${scene.id}: generating ${scene.voice === 'quote' ? 'quotation' : 'narration'} (${scene.voiceText.length} characters)`);
    await new OmniVoiceClient(config).generate(scene.voiceText, audio);
    const duration = await getDurationSec(audio);
    if (duration < 1 || duration > 90) throw new Error(`Unexpected voice duration: ${scene.id} ${duration}`);
    await writeFile(manifest, JSON.stringify({ identity, duration, voiceId }, null, 2));
    console.log(`${scene.id}: ${duration.toFixed(2)}s`);
  }
  console.log(`Voice generation complete: ${output}`);
} else if (args.includes('--prepare')) {
  let cursorFrames = 0;
  const scenes = [];
  for (const scene of spec.scenes) {
    const tempo = scene.voice === 'quote' ? 0.97 : 0.88;
    const voiceDuration = (await getDurationSec(join(output, 'voice', `${scene.id}.mp3`))) / tempo;
    const frames = Math.ceil((scene.lead + voiceDuration + scene.hold) * 30);
    const duration = frames / 30;
    scenes.push({ ...scene, start: cursorFrames / 30, end: (cursorFrames + frames) / 30, duration, voiceDuration });
    cursorFrames += frames;
    const paddedAudio = join(output, 'voice', `${scene.id}-padded.wav`);
    // Bound output samples after padding: atrim's timestamp-based duration can
    // exclude the adelay prefix in FFmpeg 8.1, shortening every scene's WAV.
    await run('ffmpeg', ['-y', '-v', 'error', '-i', join(output, 'voice', `${scene.id}.mp3`), '-af', `atempo=${tempo},aresample=48000,adelay=${Math.round(scene.lead * 1000)}:all=1,apad`, '-t', String(duration), '-ar', '48000', '-ac', '1', paddedAudio]);
    const paddedDuration = await getDurationSec(paddedAudio);
    if (Math.abs(paddedDuration - duration) > 1/48000 + .000001) throw new Error(`Audio padding mismatch: ${scene.id}`);
  }
  const timeline = { ...spec, duration: cursorFrames / 30, fps: 30, width: 1920, height: 1080, scenes };
  await writeFile(join(output, 'timeline.json'), JSON.stringify(timeline, null, 2));
  await writeFile(join(output, 'script.txt'), spec.scenes.map((s: any) => s.voiceText).join('\n\n'));
  const concat = scenes.map((s: any) => `file '${join(output, 'voice', `${s.id}-padded.wav`).replaceAll('\\', '/')}'`).join('\n');
  await writeFile(join(output, 'voice/concat.txt'), concat);
  await run('ffmpeg', ['-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', join(output, 'voice/concat.txt'), '-af', 'loudnorm=I=-18:TP=-2:LRA=9', '-ar', '48000', '-ac', '1', join(output, 'voice.wav')]);
  if (Math.abs(await getDurationSec(join(output, 'voice.wav')) - timeline.duration) > 1/48000 + .000001) throw new Error('Concatenated narration duration does not match visual timeline');
  const stamp = (t: number) => { const ms = Math.round(t * 1000); return `${String(Math.floor(ms / 3600000)).padStart(2, '0')}:${String(Math.floor(ms / 60000) % 60).padStart(2, '0')}:${String(Math.floor(ms / 1000) % 60).padStart(2, '0')},${String(ms % 1000).padStart(3, '0')}`; };
  let srt = '', n = 0;
  for (const scene of scenes) {
    const rawSentences = scene.voiceText.match(/[^.!?]+[.!?]+|[^.!?]+$/gu) || [scene.voiceText];
    const sentences: string[] = [];
    for (const rawSentence of rawSentences) {
      let part = '';
      for (const word of rawSentence.trim().split(/\s+/u)) {
        if (part.length + word.length + 1 > 84 && part) { sentences.push(part.trim()); part = ''; }
        part += word + ' ';
      }
      if (part.trim()) sentences.push(part.trim());
    }
    const total = sentences.reduce((sum: number, sentence: string) => sum + sentence.trim().length, 0);
    let position = scene.start + scene.lead;
    for (const sentence of sentences) {
      const end = position + scene.voiceDuration * sentence.trim().length / total;
      const words = sentence.trim().split(/\s+/u);
      let lines = '', line = '';
      for (const word of words) { if (line.length + word.length > 46) { lines += line.trim() + '\n'; line = ''; } line += word + ' '; }
      lines += line.trim();
      srt += `${++n}\n${stamp(position)} --> ${stamp(end)}\n${lines}\n\n`;
      position = end;
    }
  }
  await writeFile(join(output, 'hook.srt'), srt);
  const templateSource = join(root, 'templates/history');
  const toolTemplate = join(tool, 'templates', spec.templateId);
  for (const scene of spec.scenes) {
    if (!existsSync(join(root, 'assets/history-1946', scene.image))) throw new Error(`Missing historical illustration: ${scene.image}`);
  }
  await mkdir(join(templateSource, 'assets'), { recursive: true });
  await cp(join(root, 'assets/history-1946'), join(templateSource, 'assets'), { recursive: true });
  await cp(templateSource, toolTemplate, { recursive: true });
  const variables = { scenes_json: JSON.stringify(scenes), total_duration: timeline.duration };
  await writeFile(join(output, 'variables.json'), JSON.stringify(variables));
  const templateHtml = await readFile(join(templateSource, 'index.html'), 'utf8');
  const previewDriver = '<script>const began=performance.now();function preview(now){window.seek(((now-began)/1000)%window.DURATION);requestAnimationFrame(preview)}requestAnimationFrame(preview);</script>';
  const previewHtml = templateHtml.replace('<script>', `<script>window.VNR_PREVIEW=${JSON.stringify(variables).replaceAll('<', '\\u003c')};</script><script>`).replaceAll('./assets/', '../../templates/history/assets/').replace('</body>', `${previewDriver}</body>`);
  await writeFile(join(output, 'preview.html'), previewHtml);
  console.log(`Prepared ${scenes.length} scenes, ${timeline.duration.toFixed(2)}s, new template: ${spec.templateId}`);
} else if (args.includes('--render') || args.includes('--proof')) {
  const timeline = JSON.parse(await readFile(join(output, 'timeline.json'), 'utf8'));
  const variables = JSON.parse(await readFile(join(output, 'variables.json'), 'utf8'));
  const proof = args.includes('--proof');
  await composeTemplate({ templateId: spec.templateId, inputs: variables, aspect: '16:9', outputPath: join(output, proof ? 'qa/proof.mp4' : 'video-silent.mp4'), fps: proof ? 1 : 30, quality: proof ? 'draft' : 'high', workers: proof ? 1 : 2, durationSec: timeline.duration });
  console.log(`Rendered: ${output}/${proof ? 'qa/proof.mp4' : 'video-silent.mp4'}`);
} else if (args.includes('--extract-proof') || args.includes('--extract-final')) {
  const timeline = JSON.parse(await readFile(join(output, 'timeline.json'), 'utf8'));
  const final = args.includes('--extract-final');
  for (const scene of timeline.scenes) {
    const sampleTime = final ? scene.start + scene.duration * .78 : Math.floor(scene.start + scene.duration * .78);
    await run('ffmpeg', ['-y', '-v', 'error', '-ss', String(sampleTime), '-i', join(output, final ? 'hook.mp4' : 'qa/proof.mp4'), '-frames:v', '1', join(output, `qa/${scene.id}.png`)]);
  }
  await run('ffmpeg', ['-y', '-v', 'error', '-framerate', '1', '-i', join(output, 'qa/c%02d.png'), '-vf', 'scale=640:360,tile=3x4:padding=4:color=black', '-frames:v', '1', join(output, 'qa/contact-sheet.jpg')]);
  console.log(`Proof contact sheet: ${output}/qa/contact-sheet.jpg`);
} else if (args.includes('--finalize')) {
  const timeline = JSON.parse(await readFile(join(output, 'timeline.json'), 'utf8'));
  await run('ffmpeg', ['-y', '-v', 'error', '-i', join(output, 'voice.wav'), '-i', join(output, 'soundtrack.wav'), '-filter_complex', '[0:a][1:a]amix=inputs=2:normalize=0,loudnorm=I=-16:TP=-1.2:LRA=9[a]', '-map', '[a]', '-ar', '48000', '-c:a', 'pcm_s16le', join(output, 'mix.wav')]);
  await run('ffmpeg', ['-y', '-v', 'error', '-i', join(output, 'video-silent.mp4'), '-i', join(output, 'mix.wav'), '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-t', String(timeline.duration), '-movflags', '+faststart', join(output, 'hook.mp4')]);
  await run('ffmpeg', ['-y', '-v', 'error', '-i', join(output, 'hook.mp4'), '-vf', 'scale=1280:720', '-c:v', 'libx264', '-preset', 'fast', '-crf', '23', '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', join(output, 'hook-720p.mp4')]);
  await renderSubtitles();
  await run('ffmpeg', ['-y', '-v', 'error', '-i', join(output, 'voice.wav'), '-c:a', 'libmp3lame', '-b:a', '192k', join(output, 'voice.mp3')]);
  console.log(`Final video: ${output}/hook.mp4 (${timeline.duration.toFixed(2)}s)`);
} else if (args.includes('--subtitles-only')) {
  await renderSubtitles();
  console.log(`Subtitled video: ${output}/hook-phude.mp4`);
} else if (args.includes('--verify')) {
  const timeline = JSON.parse(await readFile(join(output, 'timeline.json'), 'utf8'));
  const video = join(output, 'hook.mp4');
  const metadata = JSON.parse(await run('ffprobe', ['-v', 'error', '-show_entries', 'stream=codec_name,codec_type,width,height,r_frame_rate,pix_fmt,duration,nb_frames,sample_rate,channels:format=duration,size', '-of', 'json', video]));
  const picture = metadata.streams.find((stream: any) => stream.codec_type === 'video');
  const sound = metadata.streams.find((stream: any) => stream.codec_type === 'audio');
  if (picture?.width !== 1920 || picture?.height !== 1080 || picture?.r_frame_rate !== '30/1' || picture?.pix_fmt !== 'yuv420p') throw new Error('Unexpected master video format');
  if (picture.codec_name !== 'h264' || sound?.codec_name !== 'aac') throw new Error('Expected H.264 + AAC');
  if (Math.abs(Number(metadata.format.duration) - timeline.duration) > 1/30+.001) throw new Error('Final duration does not match timeline');
  if (Number(picture.nb_frames) !== Math.round(timeline.duration * 30)) throw new Error('Frame count does not match timeline');
  await run('ffmpeg', ['-v', 'error', '-i', video, '-f', 'null', 'NUL']);
  const measured = await run('ffmpeg', ['-hide_banner', '-nostats', '-i', video, '-af', 'loudnorm=I=-16:TP=-1.2:LRA=9:print_format=json', '-f', 'null', 'NUL'], true);
  await writeFile(join(output, 'qa/final-audio-loudness.txt'), measured);
  const match = measured.match(/\{\s*"input_i"[\s\S]*?\}/u);
  const loudness = match ? JSON.parse(match[0]) : undefined;
  if (!loudness || Number(loudness.input_tp) > -.8) throw new Error('Audio true peak exceeds delivery target');
  const report = { passed: true, newTemplate: spec.templateId, scenes: timeline.scenes.length, expectedDuration: timeline.duration, expectedFrames: Math.round(timeline.duration*30), decode: 'complete decode passed', metadata, loudness, sha256: createHash('sha256').update(await readFile(video)).digest('hex') };
  await writeFile(join(output, 'qa/verification.json'), JSON.stringify(report, null, 2));
  console.log(JSON.stringify({ passed: true, duration: metadata.format.duration, frames: picture.nb_frames, integratedLUFS: loudness.input_i, truePeakDbTP: loudness.input_tp, sizeMB: (Number(metadata.format.size)/1e6).toFixed(1) }));
} else {
  throw new Error('Use --tts-only, --prepare, --proof, --render, --finalize, --extract-final, or --verify.');
}
