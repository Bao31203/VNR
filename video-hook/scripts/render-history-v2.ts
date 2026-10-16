import { readFile, writeFile, mkdir, cp, copyFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { spawn } from 'node:child_process';
import { join, resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

const root = resolve(import.meta.dirname, '..');
const output = join(root, 'out/history-1946-v2');
const tool = 'F:/AI-auto-generate-video';
const templateId = 'frame-vnr-history-v2';
const style = JSON.parse(await readFile(join(root, 'style/video-style.json'), 'utf8'));
const audioConfig = JSON.parse(await readFile(join(root, 'production/history-v2-audio.json'), 'utf8'));
const oldSpec = JSON.parse(await readFile(join(root, 'production/history-scenes.json'), 'utf8'));
const { getDurationSec } = await import(pathToFileURL(join(tool, 'src/assets/audio-tools.ts')).href);
const { composeTemplate } = await import(pathToFileURL(join(tool, 'src/render/template-composer.ts')).href);
const { OmniVoiceClient } = await import(pathToFileURL(join(tool, 'src/tts/omnivoice-client.ts')).href);
const args = process.argv.slice(2);
const fps = 30;
const frameTime = (seconds: number) => Math.ceil(seconds * fps - 1e-7) / fps;
await mkdir(join(output, 'voice'), { recursive: true });
await mkdir(join(output, 'qa'), { recursive: true });

function run(cmd: string, args: string[], stderr = false): Promise<string> {
  return new Promise((accept, reject) => {
    const proc = spawn(cmd, args, { cwd: root, windowsHide: true });
    let out = '', err = '';
    proc.stdout.on('data', d => out += d); proc.stderr.on('data', d => err += d);
    proc.on('error', reject); proc.on('close', code => code === 0 ? accept(out + (stderr ? err : '')) : reject(new Error(`${cmd} exit ${code}: ${err.slice(-3000)}`)));
  });
}
function hash(value: string | Buffer) { return createHash('sha256').update(value).digest('hex'); }
async function mixAudio(timeline: any) {
  const quietWindows = [...timeline.quietWindows, timeline.blackouts.at(-1)];
  const silence = quietWindows.map((q: any) => `between(t,${q.start-1/48000},${q.end+1/48000})`).join('+');
  // Apply sample-level silence after loudnorm's resampling so its FIR tail
  // cannot introduce pre-ringing into the deliberately silent intervals.
  const filter = `[0:a][1:a]amix=inputs=2:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=9,aresample=48000,aeval=exprs='if(${silence},0,val(0))'[a]`;
  await run('ffmpeg',['-y','-v','error','-i',join(output,'voice.wav'),'-i',join(output,'soundtrack.wav'),'-filter_complex',filter,'-map','[a]','-ar','48000','-c:a','pcm_s16le',join(output,'mix.wav')]);
}
function seeded(seed: string) {
  let state = parseInt(hash(seed).slice(0, 8), 16) >>> 0;
  return () => { state ^= state << 13; state ^= state >>> 17; state ^= state << 5; return (state >>> 0) / 4294967296; };
}
const assetSources: Record<string,string> = {
  A01: 'assets/history-1946-v2/a01-dong-ho.png', A02: 'assets/history-1946/a02-pho-ha-noi.png',
  A03: 'assets/history-1946/a03-hai-phong.png', A04: 'assets/history-1946-v2/a04-thiet-giap.png',
  A06: 'assets/history-1946/a06-van-phuc.png', A07: 'assets/history-1946/a07-chien-luy.png',
  A08: 'assets/history-1946-v2/a08-nha-may-dien.png', A09: 'assets/history-1946-v2/a09-phao-khai-hoa.png',
  A10: 'assets/history-1946/a10-loi-keu-goi.png', A11a: 'assets/history-1946-v2/a11a-quan-phap.png',
  A11b: 'assets/history-1946/a07-chien-luy.png', A12: 'assets/history-1946-v2/a12-cau-hoi.png',
  A13: 'assets/history-1946/a13-binh-minh.png',
};

async function generateQuestionAudio() {
  const voiceDir = join(tool, '.studio/voices/131af5c2-8d45-4733-8568-9e10166695ee');
  const profile = JSON.parse(await readFile(join(voiceDir, 'profile.json'), 'utf8'));
  if (!profile.consent?.confirmed) throw new Error('Saved narrator profile has no consent');
  const tts = new OmniVoiceClient({ endpoint: 'http://127.0.0.1:8123', refAudio: join(voiceDir, 'reference.wav'), refText: profile.referenceText, speed: 1 });
  for (const [name, text] of [['c10-body','Thiếu vũ khí. Kinh tế kiệt quệ. Không một nước nào công nhận.'], ['c10-question','Vậy, lấy gì để thắng?']]) {
    const path = join(output, 'voice', `${name}.mp3`);
    if (!existsSync(path)) { console.log(`TTS: ${name}`); await tts.generate(text, path); }
  }
}

if (args.includes('--prepare')) {
  await generateQuestionAudio();
  const scenes: any[] = [];
  let cursor = 0;
  const recording = join(root, audioConfig.sourceAudio);
  const originalSha256 = hash(await readFile(recording));
  const quotePath = join(output, 'voice/c08-recording.wav');
  const quoteLength = audioConfig.clipEnd - audioConfig.clipStart;
  await run('ffmpeg', ['-y','-v','error','-ss',String(audioConfig.clipStart),'-i',recording,'-t',String(quoteLength),'-af',`afade=t=in:d=0.008,afade=t=out:st=${quoteLength-.008}:d=0.008`,'-ar','48000','-ac','1',quotePath]);
  const events: any[] = [];
  for (let i = 0; i < style.scenes.length; i++) {
    const scene = JSON.parse(JSON.stringify(style.scenes[i]));
    const old = oldSpec.scenes[i];
    const id = `c${String(i+1).padStart(2,'0')}`;
    const tempo = i === 7 ? 1 : .88;
    let source = i === 7 ? quotePath : join(root, `out/history-1946/voice/${id}.mp3`);
    let voiceDuration = (await getDurationSec(source)) / tempo;
    let duration = frameTime(Math.max(scene.duration, scene.voStart + voiceDuration + .8));
    scene.voiceText = i === 7 ? style.scenes[7].elements.filter((e: any) => e.id !== 'q-attr').map((e: any) => e.text).join(' ') : old.voiceText;
    if (i === 7) {
      for (const cue of audioConfig.quoteCues) {
        const element = scene.elements.find((e: any) => e.id === cue.id);
        element.in.t = scene.voStart + cue.start - audioConfig.clipStart;
        element.speechEnd = scene.voStart + cue.end - audioConfig.clipStart;
        if (element.in.preset === 'type') element.in.charsPerSecond = Array.from(element.text.normalize('NFC')).length / (.8 * (cue.end-cue.start));
      }
      const last = scene.elements.find((e: any) => e.id === 'q9');
      const attribution = scene.elements.find((e: any) => e.id === 'q-attr');
      attribution.in.t = last.in.t + (last.speechEnd-last.in.t)*.8 + .2;
      duration = frameTime(Math.max(duration, attribution.in.t + attribution.text.length/30 + .8));
    }
    if (i === 9) {
      const body = join(output, 'voice/c10-body.mp3');
      const question = join(output, 'voice/c10-question.mp3');
      const bodyDuration = await getDurationSec(body);
      const questionDuration = await getDurationSec(question);
      const bodyTempo = Math.max(.88, bodyDuration / 4.82);
      source = join(output,'voice/c10-composite.wav');
      await run('ffmpeg',['-y','-v','error','-i',body,'-i',question,'-filter_complex',`[0:a]atempo=${bodyTempo},aresample=48000,adelay=400:all=1,apad[a];[1:a]aresample=48000,adelay=5900:all=1,apad[b];[a][b]amix=inputs=2:normalize=0[out]`,'-map','[out]','-t','9','-ar','48000','-ac','1',source]);
      scene.voStart = 0; voiceDuration = 9; duration = 9;
      scene.voiceText = 'Thiếu vũ khí. Kinh tế kiệt quệ. Không một nước nào công nhận. Vậy, lấy gì để thắng?';
      scene.customVoiceWindows = [[.4, .4 + bodyDuration/bodyTempo], [5.9, 5.9+questionDuration]];
    }
    if (i === 4) cursor += .3;
    scene.start = frameTime(cursor); scene.duration = duration; scene.end = frameTime(scene.start+duration);
    scene.voiceDuration = voiceDuration; scene.baseDuration = style.scenes[i].duration; scene.voiceSource = source;
    scene.voiceWindows = scene.customVoiceWindows || [[scene.voStart, scene.voStart+voiceDuration]];
    const padded = join(output, 'voice', `${id}-padded.wav`);
    const rate = i === 9 ? 1 : tempo;
    const speedFilter = rate === 1 ? '' : `atempo=${rate},`;
    await run('ffmpeg',['-y','-v','error','-i',source,'-af',`${speedFilter}aresample=48000,adelay=${Math.round(scene.voStart*1000)}:all=1,apad`,'-t',String(duration),'-ar','48000','-ac','1',padded]);
    if (Math.abs(await getDurationSec(padded)-duration) > 1/48000+.000001) throw new Error(`Audio length mismatch ${id}`);
    scene.paddedAudio = padded;

    function event(type: string, local: number, extra: any = {}) {
      events.push({ type, frame: Math.round((scene.start + local)*fps), scene: scene.id, local, ...extra });
    }
    function compile(element: any, parentStart = 0, inherited: any = undefined) {
      const config = element.in || inherited || { t: parentStart, preset: 'printed' };
      let local = typeof config.t === 'number' ? config.t : config.t === 'fromC2' ? -10 : parentStart;
      if (element.anchor === 'end') local += duration - scene.baseDuration;
      element.runtimeIn = local;
      element.runtimeOut = typeof element.out?.t === 'number' ? element.out.t : duration;
      element.runtimePreset = config.preset || 'printed';
      if (element.kind === 'group') {
        for (const child of element.children) compile(child, local);
        if (element.id === 'c4-cal') event('paper-flip', 6.8);
        if (element.id === 'c4-doc') event('paper-slide', local);
      } else if (element.kind === 'node') {
        const fromPrevious = config.t === 'fromC2';
        element.date.kind = 'text'; element.desc.kind = 'text';
        compile(element.date, local, {t: fromPrevious ? -10 : local+.4, preset: fromPrevious ? 'printed' : 'type',charsPerSecond:config.charsPerSecond||24});
        const next = element.date.charFrames?.length ? (element.date.charFrames.at(-1)/fps)+.2 : local;
        compile(element.desc, next, {t: fromPrevious ? -10 : next,preset:fromPrevious ? 'printed':'type',charsPerSecond:config.charsPerSecond||24});
        if (!fromPrevious) event('node-pop', local);
      } else if (element.kind === 'text' && element.runtimePreset === 'type') {
        const st = style.textStyles[element.style];
        const text = st.case === 'upper' ? element.text.toLocaleUpperCase('vi') : element.text;
        const chars = Array.from(text.normalize('NFC')) as string[];
        const random = seeded(`${scene.id}:${element.id||element.style}:${local}`);
        const cps = typeof config.charsPerSecond === 'number' ? config.charsPerSecond : 26;
        let at = local;
        element.charFrames = chars.map((character, j) => {
          if (j) at += (1+(random()-.5)*.4)/cps;
          const f = Math.round(at*fps);
          event(character === ' ' ? 'type-space' : 'type-key', f/fps, { element: element.id, character, variant: Math.floor(random()*6), pitch: .95+random()*.1 });
          return f;
        });
        element.cursorHold = config.cursorHoldAfter || .5;
        const finish = (element.charFrames.at(-1)||Math.round(local*fps))/fps;
        if (element.returnSound) event('type-return',finish+.08);
        if (element.bell) event('type-bell',finish+.1);
      } else if (element.kind === 'number') {
        event('counter',local,{length:1.2});
      } else if (element.runtimePreset === 'slam' && scene.id === 'C8') event('hit',local);
      else if (element.runtimePreset === 'softScaleIn') event('hit',local,{gain:.6});
      if (element.id === 'c11-rule') event('drum',local);
    }
    for (const element of scene.elements) compile(element);
    if (scene.id === 'C1') for (let t=.3;t<duration;t+=1) event('tick',t,{gain:.6});
    if (scene.id === 'C3') for (const flash of scene.flashes) event('naval',flash.t);
    if (scene.id === 'C6') {for(let t=duration-5;t<duration;t++)event('tick',t,{gain:1+(t-duration+5)*.15});event('buzz',duration-.8,{length:.8});}
    if (scene.id === 'C7') {event('switch',0);event('cannon',1);}
    scene.keyframe = scene.id === 'C8' ? duration-.35 : scene.id === 'C11' ? duration-.3 : Math.min(scene.keyframe,duration-.5);
    scenes.push(scene);cursor = scene.end;
  }
  const duration = frameTime(cursor + 2.5);
  const timeline = { fps,width:1920,height:1080,duration,templateId,sourceCommit:audioConfig.sourceCommit,scenes,recording:{...audioConfig,sha256:originalSha256},blackouts:[{start:0,end:.5},{start:scenes[3].end,end:scenes[4].start},{start:scenes[6].start,end:scenes[6].start+1},{start:cursor+1.5,end:duration}],quietWindows:[{start:scenes[6].start+.04,end:scenes[6].start+1},{start:scenes[9].start+5.4,end:scenes[9].start+5.9}] };
  events.sort((a,b)=>a.frame-b.frame);
  await writeFile(join(output,'timeline.json'),JSON.stringify(timeline,null,2));
  await writeFile(join(output,'sfx-events.json'),JSON.stringify(events,null,2));
  const concatFiles: string[] = [];
  for(let i=0;i<scenes.length;i++){
    if(i===4){const gap=join(output,'voice/dip-black-gap.wav');await run('ffmpeg',['-y','-v','error','-f','lavfi','-i','anullsrc=r=48000:cl=mono','-t',String(scenes[4].start-scenes[3].end),gap]);concatFiles.push(gap);}
    concatFiles.push(scenes[i].paddedAudio);
  }
  const tail=join(output,'voice/end-black.wav');await run('ffmpeg',['-y','-v','error','-f','lavfi','-i','anullsrc=r=48000:cl=mono','-t','2.5',tail]);concatFiles.push(tail);
  await writeFile(join(output,'voice/concat.txt'),concatFiles.map(p=>`file '${p.replaceAll('\\','/')}'`).join('\n'));
  await run('ffmpeg',['-y','-v','error','-f','concat','-safe','0','-i',join(output,'voice/concat.txt'),'-af','loudnorm=I=-18:TP=-2:LRA=9','-ar','48000','-ac','1',join(output,'voice.wav')]);
  if(Math.abs(await getDurationSec(join(output,'voice.wav'))-duration)>.001)throw new Error('Narration / image timeline mismatch');
  const template=join(root,'templates/history-v2');const assetMap:Record<string,string>={};
  for(const [key,relative]of Object.entries(assetSources)){
    const path=join(root,relative);if(!existsSync(path))throw new Error(`Missing illustration: ${path}`);
    const filename=`${key.toLowerCase()}.png`;await copyFile(path,join(template,'assets',filename));assetMap[key]=filename;
  }
  await cp(template,join(tool,'templates',templateId),{recursive:true});
  const variables={timeline_json:JSON.stringify(timeline),style_json:JSON.stringify(style),asset_map_json:JSON.stringify(assetMap)};
  await writeFile(join(output,'variables.json'),JSON.stringify(variables));
  await writeFile(join(output,'script.txt'),scenes.map(s=>s.voiceText).join('\n\n'));
  const html=await readFile(join(template,'index.html'),'utf8');
  const driver='<script>const began=performance.now();function play(now){window.seek(((now-began)/1000)%window.DURATION);requestAnimationFrame(play)}requestAnimationFrame(play);</script>';
  await writeFile(join(output,'preview.html'),html.replace('<script>',`<script>window.VNR_PREVIEW=${JSON.stringify(variables).replaceAll('<','\\u003c')}</script><script>`).replaceAll('./assets/','../../templates/history-v2/assets/').replace('</body>',driver+'</body>'));
  console.log(JSON.stringify({duration,frames:Math.round(duration*fps),quoteDuration:scenes[7].duration,quoteSourceSeconds:[audioConfig.clipStart,audioConfig.clipEnd],typingEvents:events.filter(e=>e.type.startsWith('type')).length}));
} else if(args.includes('--proof')||args.includes('--render')) {
  const timeline=JSON.parse(await readFile(join(output,'timeline.json'),'utf8'));const variables=JSON.parse(await readFile(join(output,'variables.json'),'utf8'));const proof=args.includes('--proof');
  await composeTemplate({templateId,inputs:variables,aspect:'16:9',outputPath:join(output,proof?'qa/proof.mp4':'video-silent.mp4'),fps:proof?1:30,quality:proof?'draft':'high',workers:proof?1:2,durationSec:timeline.duration});
} else if(args.includes('--extract-proof')||args.includes('--extract-final')) {
  const timeline=JSON.parse(await readFile(join(output,'timeline.json'),'utf8'));const final=args.includes('--extract-final');
  for(let i=0;i<timeline.scenes.length;i++){const s=timeline.scenes[i];const t=s.start+s.keyframe;await run('ffmpeg',['-y','-v','error','-ss',String(final?t:Math.floor(t)),'-i',join(output,final?'hook.mp4':'qa/proof.mp4'),'-frames:v','1',join(output,`qa/c${String(i+1).padStart(2,'0')}.png`)]);}
  await run('ffmpeg',['-y','-v','error','-framerate','1','-i',join(output,'qa/c%02d.png'),'-vf','scale=640:360,tile=3x4:padding=4:color=black','-frames:v','1',join(output,'qa/contact-sheet.jpg')]);
} else if(args.includes('--finalize')) {
  const timeline=JSON.parse(await readFile(join(output,'timeline.json'),'utf8'));
  await mixAudio(timeline);
  await run('ffmpeg',['-y','-v','error','-i',join(output,'video-silent.mp4'),'-i',join(output,'mix.wav'),'-map','0:v:0','-map','1:a:0','-c:v','copy','-bsf:v','h264_metadata=colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1','-c:a','aac','-b:a','192k','-t',String(timeline.duration),'-movflags','+faststart',join(output,'hook.mp4')]);
  await run('ffmpeg',['-y','-v','error','-i',join(output,'hook.mp4'),'-vf','scale=1280:720','-c:v','libx264','-crf','23','-preset','fast','-c:a','aac','-b:a','128k','-movflags','+faststart',join(output,'hook-720p.mp4')]);
  console.log(`Updated video: ${output}/hook.mp4`);
} else if(args.includes('--mix-only')) {
  await mixAudio(JSON.parse(await readFile(join(output,'timeline.json'),'utf8')));
  console.log('Mixed audio with sample-accurate quiet windows');
} else if(args.includes('--verify')) {
  const timeline=JSON.parse(await readFile(join(output,'timeline.json'),'utf8'));const video=join(output,'hook.mp4');
  const metadata=JSON.parse(await run('ffprobe',['-v','error','-show_entries','format=duration,size:stream=codec_name,codec_type,width,height,r_frame_rate,nb_frames,pix_fmt,color_space,color_transfer,color_primaries','-of','json',video]));
  const v=metadata.streams.find((s:any)=>s.codec_type==='video');const a=metadata.streams.find((s:any)=>s.codec_type==='audio');
  if(v?.width!==1920||v?.height!==1080||v?.r_frame_rate!=='30/1'||v?.pix_fmt!=='yuv420p'||v?.codec_name!=='h264'||a?.codec_name!=='aac')throw new Error('Incorrect final format');
  if(Math.abs(+metadata.format.duration-timeline.duration)>.034||+v.nb_frames!==Math.round(timeline.duration*fps))throw new Error('Final frame count or duration mismatch');
  if(hash(await readFile(join(root,audioConfig.sourceAudio)))!==timeline.recording.sha256)throw new Error('Source recording changed');
  const loudness=await run('ffmpeg',['-hide_banner','-nostats','-xerror','-i',video,'-vf','blackdetect=d=0.1:pix_th=0.02:pic_th=0.999','-af','loudnorm=I=-16:TP=-1.5:LRA=9:print_format=json','-f','null','NUL'],true);
  await writeFile(join(output,'qa/media-analysis.txt'),loudness);
  const measurement=JSON.parse(loudness.match(/\{\s*"input_i"[\s\S]*?\}/u)![0]);
  if(+measurement.input_tp> -1)throw new Error('Final true peak exceeds -1 dBTP');
  const blackouts=[...loudness.matchAll(/black_start:([\d.]+) black_end:([\d.]+) black_duration:([\d.]+)/gu)].map(m=>({start:+m[1],end:+m[2],duration:+m[3]}));
  if(blackouts.length!==4)throw new Error(`Expected four blackouts; measured ${blackouts.length}`);
  const cannonBlack=blackouts.find(b=>Math.abs(b.start-timeline.scenes[6].start)<.067);
  if(!cannonBlack||Math.abs(cannonBlack.duration-1)>.034)throw new Error('C7 blackout must last exactly 30 frames');
  const report={passed:true,metadata,loudness:measurement,blackouts,recording:timeline.recording,sha256:hash(await readFile(video)),duration:timeline.duration};
  await writeFile(join(output,'qa/verification.json'),JSON.stringify(report,null,2));console.log(JSON.stringify({passed:true,duration:timeline.duration,frames:v.nb_frames,loudness:measurement.input_i,peak:measurement.input_tp}));
} else throw new Error('Choose --prepare, --proof, --render, --extract-proof, --extract-final, --finalize, --verify');
