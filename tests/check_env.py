# 환경 검증 스크립트: uv run tests/check_env.py
# 음원 파일 없이 합성한 테스트 신호로 핵심 라이브러리가 Python 3.13에서 동작하는지 확인한다.
import sys
import shutil
import tempfile
from importlib.metadata import version, PackageNotFoundError

import numpy as np

# 1) 버전 출력: 설치 여부와 버전을 한눈에 확인
PACKAGES = [
    "langgraph", "langgraph-checkpoint-sqlite", "openai", "google-genai",
    "python-dotenv", "librosa", "pydub", "audioop-lts", "pyloudnorm",
]

print(f"Python {sys.version.split()[0]}")
for name in PACKAGES:
    try:
        print(f"  {name:28s} {version(name)}")
    except PackageNotFoundError:
        print(f"  {name:28s} 설치 안 됨")

print(f"  {'ffmpeg':28s} {'있음' if shutil.which('ffmpeg') else '없음 (별도 설치 필요)'}")

# 2) 테스트 신호 만들기: 120 BPM 클릭 + A음(440Hz) 사인파, 10초
SR = 22050
DURATION = 10.0
t = np.arange(int(SR * DURATION)) / SR
signal = 0.3 * np.sin(2 * np.pi * 440 * t)
beat_interval = int(SR * 60 / 120)
for start in range(0, len(signal), beat_interval):
    signal[start:start + 400] += 0.8 * np.hanning(800)[400:]
signal = signal.astype(np.float32)

results = {}


def check(name, fn):
    # 각 검사를 try/except로 감싸 하나가 실패해도 나머지는 계속 진행
    try:
        results[name] = ("OK", fn())
    except Exception as e:
        results[name] = ("FAIL", f"{type(e).__name__}: {e}")


# 3) librosa: 템포·비트·크로마(키 추정용) 계산
def librosa_check():
    import librosa
    tempo, beats = librosa.beat.beat_track(y=signal, sr=SR)
    chroma = librosa.feature.chroma_stft(y=signal, sr=SR)
    top_pitch = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"][
        int(chroma.mean(axis=1).argmax())]
    return f"tempo={float(np.atleast_1d(tempo)[0]):.1f} BPM, beats={len(beats)}, 가장 강한 음={top_pitch}"


# 4) pydub + audioop-lts: 자르기·이어붙이기·크로스페이드
def pydub_check():
    from pydub import AudioSegment
    pcm = (signal * 32767).astype(np.int16).tobytes()
    seg = AudioSegment(data=pcm, sample_width=2, frame_rate=SR, channels=1)
    joined = seg[:4000].append(seg[6000:], crossfade=200)
    return f"원본 {len(seg)}ms → 편집 {len(joined)}ms, dBFS={joined.dBFS:.1f}"


# 5) pydub + ffmpeg: wav로 내보낸 뒤 다시 읽기
def pydub_ffmpeg_check():
    from pydub import AudioSegment
    pcm = (signal * 32767).astype(np.int16).tobytes()
    seg = AudioSegment(data=pcm, sample_width=2, frame_rate=SR, channels=1)
    with tempfile.NamedTemporaryFile(suffix=".mp3") as f:
        seg.export(f.name, format="mp3")
        back = AudioSegment.from_file(f.name)
    return f"mp3 왕복 {len(back)}ms"


# 6) pyloudnorm: LUFS 측정 (연결부 음량 차 검증용)
def loudness_check():
    import pyloudnorm as pyln
    meter = pyln.Meter(SR)
    return f"{meter.integrated_loudness(signal):.1f} LUFS"


check("librosa", librosa_check)
check("pydub+audioop-lts", pydub_check)
check("pydub+ffmpeg", pydub_ffmpeg_check)
check("pyloudnorm", loudness_check)

print()
for name, (status, detail) in results.items():
    print(f"[{status}] {name}: {detail}")

sys.exit(0 if all(s == "OK" for s, _ in results.values()) else 1)
