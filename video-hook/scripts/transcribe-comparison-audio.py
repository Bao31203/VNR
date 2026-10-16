"""Local word timings for the comparison narrator; no remote speech API."""
import json
import sys
import subprocess
import numpy as np
from pathlib import Path
from faster_whisper import WhisperModel
sys.stdout.reconfigure(encoding='utf-8')

source = Path(sys.argv[1])
destination = Path(sys.argv[2])
model_path = Path('C:/Users/pgb31/.cache/huggingface/hub/models--Systran--faster-whisper-small/snapshots/536b0662742c02347bc0e980a01041f333bce120')
model = WhisperModel(str(model_path), device='cpu', compute_type='int8', cpu_threads=6)
decoded = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(source), '-f', 'f32le', '-ac', '1', '-ar', '16000', 'pipe:1'], check=True, capture_output=True).stdout
samples = np.frombuffer(decoded, dtype=np.float32).copy()
segments, info = model.transcribe(samples, language='vi', beam_size=5, word_timestamps=True, vad_filter=False, condition_on_previous_text=False,
    initial_prompt='Trong thành phố, hơn sáu nghìn quân Pháp, có xe tăng, xe bọc thép yểm trợ. Phía ta, khoảng hai nghìn rưỡi vệ quốc quân, tám nghìn tự vệ, và chỉ chừng hai nghìn khẩu súng.')
result = {'source': str(source), 'duration': info.duration, 'language': info.language, 'segments': []}
destination.parent.mkdir(parents=True, exist_ok=True)
for segment in segments:
    item = {'start': segment.start, 'end': segment.end, 'text': segment.text,
            'words': [{'start': word.start, 'end': word.end, 'word': word.word, 'probability': word.probability} for word in (segment.words or [])]}
    result['segments'].append(item)
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'{segment.start:6.2f} - {segment.end:6.2f}: {segment.text}', flush=True)
destination.parent.mkdir(parents=True, exist_ok=True)
destination.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
