/** Typing +13 dB; gun bursts +5s/-3dB; wait for gunfire before C8. */
import {readFile,writeFile,mkdir,rename} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {spawn} from 'node:child_process';
import {resolve,join} from 'node:path';
import {pathToFileURL} from 'node:url';
const root=resolve(import.meta.dirname,'..'),output=join(root,'out/history-1946-v6'),previous=join(root,'out/history-1946-v5');
const args=process.argv.slice(2),fps=30;
const tool='F:/AI-auto-generate-video';
await mkdir(join(output,'qa'),{recursive:true});
const hash=(b:Buffer)=>createHash('sha256').update(b).digest('hex');
function run(cmd:string,args:string[],stderr=false):Promise<string>{return new Promise((ok,fail)=>{
 const p=spawn(cmd,args,{cwd:root,windowsHide:true});let out='',err='';
 p.stdout.on('data',d=>out+=d);p.stderr.on('data',d=>err+=d);p.on('error',fail);
 p.on('close',code=>code===0?ok(out+(stderr?err:'')):fail(new Error(`${cmd} ${code}: ${err.slice(-4000)}`)));
});}
const json=async(path:string)=>JSON.parse(await readFile(path,'utf8'));
if(args.includes('--prepare')){
 const timeline=await json(join(previous,'timeline.json'));
 timeline.sourceCommit=(await run('git',['rev-parse','HEAD'])).trim();
 timeline.visualSource='V5, with C7 extended five seconds before C8';
 timeline.audioRevision='Typing +13 dB; only gun bursts +5s and -3dB; cannon unchanged; no gunfire under C8';
 const hold=5,oldC8Start=timeline.scenes[7].start;
 timeline.sfxAdjustments={typingBoostDb:13,gunfireDelaySeconds:hold,gunfireGainDb:-3,cannonUnchanged:true,waitForGunfireBeforeC8:true};
 timeline.scenes[6].duration+=hold;timeline.scenes[6].end+=hold;
 for(const e of timeline.scenes[6].elements)if(e.out?.t==='end')e.runtimeOut=timeline.scenes[6].duration;
 for(const s of timeline.scenes.slice(7)){s.start+=hold;s.end+=hold;}
 timeline.duration+=hold;
 for(const q of [...timeline.blackouts,...timeline.quietWindows]){
  if(q.start>=oldC8Start){q.start+=hold;q.end+=hold;}
 }
 // The cannon file begins 85 ms before its actual transient. Preserve its full
 // original pre-roll instead of gating/cutting it at the visual flash.
 timeline.quietWindows[0].end=timeline.scenes[6].start+.915;
 const events=await json(join(previous,'sfx-events.json'));
 const oldSfx=await json(join(previous,'qa/sfx-provenance.json'));
 for(const e of events){
  if(['C8','C9','C10','C11'].includes(e.scene))e.frame+=hold*fps;
  if(e.scene==='C7'&&['gunfire','machine-gun'].includes(e.type)){
   const source=oldSfx.recordedPlacements.find((p:any)=>p.scene==='C7'&&p.type===e.type&&Math.abs(p.targetOnset-e.frame/fps)<1e-5);
   if(!source)throw new Error('Missing original gunfire gain');
   e.local+=hold;e.frame+=hold*fps;e.gainOverride=source.gain*10**(-3/20);
  }
 }
 events.sort((a:any,b:any)=>a.frame-b.frame);
 await writeFile(join(output,'timeline.json'),JSON.stringify(timeline,null,2));
 await writeFile(join(output,'sfx-events.json'),JSON.stringify(events,null,2));
 // Insert silence only; narration samples on both sides remain unchanged.
 const voiceFilter=`[0:a]asplit[p][s];[p]atrim=end=${oldC8Start},asetpts=PTS-STARTPTS[a];anullsrc=r=48000:cl=mono,atrim=duration=5[b];[s]atrim=start=${oldC8Start},asetpts=PTS-STARTPTS[c];[a][b][c]concat=n=3:v=0:a=1[out]`;
 await run('ffmpeg',['-y','-v','error','-i',join(previous,'voice.wav'),'-filter_complex',voiceFilter,'-map','[out]','-ar','48000','-ac','1','-c:a','pcm_s16le',join(output,'voice.wav')]);
 const variables=await json(join(root,'out/history-1946-v4/variables.json'));
 variables.timeline_json=JSON.stringify(timeline);
 await writeFile(join(output,'variables.json'),JSON.stringify(variables));
 console.log(JSON.stringify({sourceCommit:timeline.sourceCommit,duration:timeline.duration,events:events.length,fortDuration:timeline.scenes[6].duration,quoteStarts:timeline.scenes[7].start}));
}else if(args.includes('--update-typing-metadata')){
 const timeline=await json(join(output,'timeline.json'));
 timeline.sfxAdjustments.typingBoostDb=13;
 timeline.audioRevision=timeline.audioRevision.replace('Typing +10 dB','Typing +13 dB');
 await writeFile(join(output,'timeline.json'),JSON.stringify(timeline,null,2));
 const variables=await json(join(output,'variables.json'));variables.timeline_json=JSON.stringify(timeline);
 await writeFile(join(output,'variables.json'),JSON.stringify(variables));
 console.log('V6 typing level updated to +13 dB over V5; timing unchanged.');
}else if(args.includes('--render-fort')){
 const timeline=await json(join(output,'timeline.json')),variables=await json(join(output,'variables.json'));
 const {composeTemplate}=await import(pathToFileURL(join(tool,'src/render/template-composer.ts')).href);
 variables.render_offset=timeline.scenes[6].start;
 await composeTemplate({templateId:'frame-vnr-history-v4',inputs:variables,aspect:'16:9',outputPath:join(output,'fort-silent.mp4'),fps:30,quality:'high',workers:2,durationSec:timeline.scenes[6].duration+1});
}else if(args.includes('--assemble-fort')){
 const timeline=await json(join(output,'timeline.json')),old=await json(join(previous,'timeline.json'));
 const prefix=Math.round(timeline.scenes[6].start*fps),replace=Math.round((timeline.scenes[6].duration+1)*fps),oldEnd=Math.round((old.scenes[7].start+1)*fps);
 const filter=`[0:v]trim=end_frame=${prefix},setpts=PTS-STARTPTS[a];[1:v]trim=end_frame=${replace},setpts=PTS-STARTPTS[b];[2:v]setpts=PTS-STARTPTS[c];[a][b][c]concat=n=3:v=1:a=0[v]`;
 const input=join(previous,'hook.mp4');
 await run('ffmpeg',['-y','-v','error','-t',String(prefix/fps),'-i',input,'-i',join(output,'fort-silent.mp4'),'-ss',String(oldEnd/fps),'-i',input,'-filter_complex',filter,'-map','[v]','-c:v','libx264','-crf','17','-preset','fast','-pix_fmt','yuv420p','-r','30','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-movflags','+faststart',join(output,'video-silent.mp4')]);
 console.log('Extended C7 by exactly 150 frames; C8 begins after all gunfire finishes.');
}else if(args.includes('--finalize')||args.includes('--mix-only')||args.includes('--remux-existing')){
 const timeline=await json(join(output,'timeline.json'));
 // Static master gain only: no loudnorm dynamics, limiter, saturation, EQ,
 // reverb or time manipulation of the new cannon/gun recordings.
 const analysis=await run('ffmpeg',['-hide_banner','-nostats','-i',join(output,'mix-unmastered.wav'),'-af','loudnorm=I=-16:TP=-1.5:LRA=9:print_format=json','-f','null','NUL'],true);
 const measured=JSON.parse(analysis.match(/\{\s*"input_i"[\s\S]*?\}/u)![0]);
 const gainDb=(await json(join(previous,'qa/mastering.json'))).gainDb;
 if(+measured.input_tp+gainDb> -1.15)throw new Error('Typing boost exceeds peak headroom with unchanged V5 master gain');
 await run('ffmpeg',['-y','-v','error','-i',join(output,'mix-unmastered.wav'),'-af',`volume=${gainDb}dB`,'-ar','48000','-c:a','pcm_s16le',join(output,'mix.wav')]);
 await writeFile(join(output,'qa/mastering.json'),JSON.stringify({method:'static gain only',gainDb,unmastered:measured,noDynamicCompression:true,typingBoostDb:13,masterGainUnchangedFromV5:true},null,2));
 if(args.includes('--mix-only')){console.log('Audio mix ready; V5 master gain unchanged');process.exit(0);}
 if(args.includes('--remux-existing')){
  const candidates=[];
  for(const [name,bitrate]of [['hook.mp4','192k'],['hook-720p.mp4','128k'],['fort-review.mp4','128k']]){
   const original=join(output,name),candidate=join(output,'qa/typing-plus3',name);
   const clip=name==='fort-review.mp4';
   await run('ffmpeg',['-y','-v','error','-i',original,...(clip?['-ss',String(timeline.scenes[6].start)]:[]),'-i',join(output,'mix.wav'),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a',bitrate,'-t',String(clip?timeline.scenes[6].duration+1:timeline.duration),'-movflags','+faststart',candidate]);
   const essence=async(path:string)=>(await run('ffmpeg',['-v','error','-i',path,'-map','0:v:0','-c','copy','-f','hash','-hash','sha256','pipe:1'])).trim();
   if(await essence(original)!==await essence(candidate))throw new Error(`Video changed: ${name}`);
   const m=JSON.parse(await run('ffprobe',['-v','error','-show_entries','format=duration:stream=codec_type,nb_frames','-of','json',candidate]));
   const expectedFrames=clip?445:4116;
   if(+m.streams.find((s:any)=>s.codec_type==='video').nb_frames!==expectedFrames)throw new Error(`Frame count changed: ${name}`);
   candidates.push({original,candidate,name});
  }
  const decoded=await run('ffmpeg',['-hide_banner','-nostats','-xerror','-i',candidates[0].candidate,'-af','loudnorm=I=-16:TP=-1.5:LRA=9:print_format=json','-f','null','NUL'],true);
  const loudness=JSON.parse(decoded.match(/\{\s*"input_i"[\s\S]*?\}/u)![0]);
  if(+loudness.input_tp> -1)throw new Error('Updated audio exceeds true-peak ceiling');
  for(const c of candidates)await rename(c.candidate,c.original);
  console.log('Updated all V6 MP4s in place; visual streams unchanged.');process.exit(0);
 }
 await run('ffmpeg',['-y','-v','error','-i',join(output,'video-silent.mp4'),'-i',join(output,'mix.wav'),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k','-t',String(timeline.duration),'-movflags','+faststart',join(output,'hook.mp4')]);
 await run('ffmpeg',['-y','-v','error','-i',join(output,'hook.mp4'),'-vf','scale=1280:720','-c:v','libx264','-crf','23','-preset','fast','-c:a','aac','-b:a','128k','-movflags','+faststart',join(output,'hook-720p.mp4')]);
 console.log(`Updated SFX: ${output}`);
}else if(args.includes('--verify')){
 const timeline=await json(join(output,'timeline.json'));
 const reports=[];
 for(const [name,width,height]of [['hook.mp4',1920,1080],['hook-720p.mp4',1280,720]] as const){
  const video=join(output,name);
  const metadata=JSON.parse(await run('ffprobe',['-v','error','-show_entries','format=duration,size:stream=codec_name,codec_type,width,height,r_frame_rate,nb_frames,pix_fmt,color_space,color_transfer,color_primaries','-of','json',video]));
  const v=metadata.streams.find((s:any)=>s.codec_type==='video'),a=metadata.streams.find((s:any)=>s.codec_type==='audio');
  if(v.width!==width||v.height!==height||+v.nb_frames!==Math.round(timeline.duration*fps)||v.r_frame_rate!=='30/1'||v.codec_name!=='h264'||a.codec_name!=='aac'||Math.abs(+metadata.format.duration-timeline.duration)>.034)throw new Error(`Invalid format: ${name}`);
  const packetHash=async(path:string)=>(await run('ffmpeg',['-v','error','-i',path,'-map','0:v:0','-c','copy','-f','hash','-hash','sha256','pipe:1'])).trim();
  const current=await packetHash(video);
  reports.push({file:name,metadata,videoStreamSha256:current});
 }
 const analysis=await run('ffmpeg',['-hide_banner','-nostats','-xerror','-i',join(output,'hook.mp4'),'-vf','blackdetect=d=0.1:pix_th=0.02:pic_th=0.999','-af','loudnorm=I=-16:TP=-1.5:LRA=9:print_format=json','-f','null','NUL'],true);
 const loudness=JSON.parse(analysis.match(/\{\s*"input_i"[\s\S]*?\}/u)![0]);
 if(+loudness.input_tp> -1)throw new Error(`True peak too high: ${loudness.input_tp}`);
 const blackouts=[...analysis.matchAll(/black_start:([\d.]+) black_end:([\d.]+) black_duration:([\d.]+)/gu)].map(m=>({start:+m[1],end:+m[2],duration:+m[3]}));
 if(blackouts.length!==4)throw new Error('Unexpected blackouts');
 if(hash(await readFile(join(root,timeline.recording.sourceAudio)))!==timeline.recording.sha256)throw new Error('Original recording changed');
 await writeFile(join(output,'qa/verification.json'),JSON.stringify({passed:true,sourceCommit:timeline.sourceCommit,reports,loudness,blackouts,adjustments:timeline.sfxAdjustments,recording:timeline.recording},null,2));
 console.log(JSON.stringify({passed:true,duration:timeline.duration,frames:Math.round(timeline.duration*fps),loudness:loudness.input_i,peak:loudness.input_tp}));
}else throw new Error('Use --prepare, --finalize, or --verify');
