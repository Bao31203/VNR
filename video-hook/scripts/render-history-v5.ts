/** Audio-only revision: original recorded SFX from repo, unchanged V4 video. */
import {readFile,writeFile,mkdir,copyFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {spawn} from 'node:child_process';
import {resolve,join} from 'node:path';
const root=resolve(import.meta.dirname,'..'),output=join(root,'out/history-1946-v5'),previous=join(root,'out/history-1946-v4');
const args=process.argv.slice(2),fps=30;
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
 timeline.visualSource='out/history-1946-v4/hook.mp4';
 timeline.audioRevision='Original recorded SFX; no return/bell/paper/end-title accents';
 // The cannon file begins 85 ms before its actual transient. Preserve its full
 // original pre-roll instead of gating/cutting it at the visual flash.
 timeline.quietWindows[0].end=timeline.scenes[6].start+.915;
 const events=await json(join(previous,'sfx-events.json'));
 for(const [local,type]of [[1.8,'gunfire'],[4.1,'machine-gun'],[5.9,'gunfire']] as const)
  events.push({type,scene:'C7',local,frame:Math.round((timeline.scenes[6].start+local)*fps)});
 events.sort((a:any,b:any)=>a.frame-b.frame);
 await writeFile(join(output,'timeline.json'),JSON.stringify(timeline,null,2));
 await writeFile(join(output,'sfx-events.json'),JSON.stringify(events,null,2));
 await copyFile(join(previous,'voice.wav'),join(output,'voice.wav'));
 console.log(JSON.stringify({sourceCommit:timeline.sourceCommit,duration:timeline.duration,events:events.length,visuals:'unchanged V4'}));
}else if(args.includes('--finalize')){
 const timeline=await json(join(output,'timeline.json'));
 // Static master gain only: no loudnorm dynamics, limiter, saturation, EQ,
 // reverb or time manipulation of the new cannon/gun recordings.
 const analysis=await run('ffmpeg',['-hide_banner','-nostats','-i',join(output,'mix-unmastered.wav'),'-af','loudnorm=I=-16:TP=-1.5:LRA=9:print_format=json','-f','null','NUL'],true);
 const measured=JSON.parse(analysis.match(/\{\s*"input_i"[\s\S]*?\}/u)![0]);
 const gainDb=Math.min(-16-(+measured.input_i),-1.8-(+measured.input_tp));
 await run('ffmpeg',['-y','-v','error','-i',join(output,'mix-unmastered.wav'),'-af',`volume=${gainDb}dB`,'-ar','48000','-c:a','pcm_s16le',join(output,'mix.wav')]);
 await writeFile(join(output,'qa/mastering.json'),JSON.stringify({method:'static gain only',gainDb,unmastered:measured,noDynamicCompression:true},null,2));
 for(const [name,bitrate]of [['hook.mp4','192k'],['hook-720p.mp4','128k']]){
  await run('ffmpeg',['-y','-v','error','-i',join(previous,name),'-i',join(output,'mix.wav'),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a',bitrate,'-t',String(timeline.duration),'-movflags','+faststart',join(output,name)]);
 }
 console.log(`Updated SFX: ${output}`);
}else if(args.includes('--verify')){
 const timeline=await json(join(output,'timeline.json'));
 const reports=[];
 for(const [name,width,height]of [['hook.mp4',1920,1080],['hook-720p.mp4',1280,720]] as const){
  const video=join(output,name);
  const metadata=JSON.parse(await run('ffprobe',['-v','error','-show_entries','format=duration,size:stream=codec_name,codec_type,width,height,r_frame_rate,nb_frames,pix_fmt,color_space,color_transfer,color_primaries','-of','json',video]));
  const v=metadata.streams.find((s:any)=>s.codec_type==='video'),a=metadata.streams.find((s:any)=>s.codec_type==='audio');
  if(v.width!==width||v.height!==height||v.nb_frames!=='3966'||v.r_frame_rate!=='30/1'||v.codec_name!=='h264'||a.codec_name!=='aac'||Math.abs(+metadata.format.duration-timeline.duration)>.034)throw new Error(`Invalid format: ${name}`);
  const packetHash=async(path:string)=>(await run('ffmpeg',['-v','error','-i',path,'-map','0:v:0','-c','copy','-f','hash','-hash','sha256','pipe:1'])).trim();
  const current=await packetHash(video),old=await packetHash(join(previous,name));
  if(current!==old)throw new Error(`Visual stream changed: ${name}`);
  reports.push({file:name,metadata,videoStreamSha256:current,visualStreamIdenticalToV4:true});
 }
 const analysis=await run('ffmpeg',['-hide_banner','-nostats','-xerror','-i',join(output,'hook.mp4'),'-vf','blackdetect=d=0.1:pix_th=0.02:pic_th=0.999','-af','loudnorm=I=-16:TP=-1.5:LRA=9:print_format=json','-f','null','NUL'],true);
 const loudness=JSON.parse(analysis.match(/\{\s*"input_i"[\s\S]*?\}/u)![0]);
 if(+loudness.input_tp> -1)throw new Error(`True peak too high: ${loudness.input_tp}`);
 const blackouts=[...analysis.matchAll(/black_start:([\d.]+) black_end:([\d.]+) black_duration:([\d.]+)/gu)].map(m=>({start:+m[1],end:+m[2],duration:+m[3]}));
 if(blackouts.length!==4)throw new Error('Unexpected blackouts');
 if(hash(await readFile(join(output,'voice.wav')))!==hash(await readFile(join(previous,'voice.wav'))))throw new Error('Narration changed');
 if(hash(await readFile(join(root,timeline.recording.sourceAudio)))!==timeline.recording.sha256)throw new Error('Original recording changed');
 await writeFile(join(output,'qa/verification.json'),JSON.stringify({passed:true,sourceCommit:timeline.sourceCommit,reports,loudness,blackouts,narrationIdenticalToV4:true,recording:timeline.recording},null,2));
 console.log(JSON.stringify({passed:true,duration:timeline.duration,visualStreamsIdenticalToV4:true,loudness:loudness.input_i,peak:loudness.input_tp}));
}else throw new Error('Use --prepare, --finalize, or --verify');
