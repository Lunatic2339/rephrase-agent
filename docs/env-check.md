# 환경 검증 결과 (2026-10-18)

`uv run tests/check_env.py` 로 다시 돌릴 수 있다. 음원 파일 없이 코드로 만든 테스트 신호(120 BPM 클릭 + 440Hz 사인파, 10초)를 쓴다.

검증 환경: Linux x86_64 (Claude 클라우드 컨테이너), uv 0.11.32, Python 3.13.16, ffmpeg 6.1.1.
팀원 PC(Windows/macOS)에서는 아직 확인 안 함.

## 설치된 버전 (uv.lock 기준)

| 패키지 | 버전 | 설치 |
|---|---|---|
| langgraph | 1.2.16 | OK |
| langgraph-checkpoint-sqlite | 3.1.2 | OK |
| openai | 3.35.1 | OK |
| google-genai | 2.31.0 | OK |
| python-dotenv | 1.2.4 | OK |
| librosa | 1.0.0 | OK |
| pydub | 0.25.1 | OK |
| audioop-lts | 0.2.2 | OK |
| pyloudnorm | 0.2.0 | OK |
| grandalf | 0.8 | OK, `draw_ascii()`에 필요 |

## 동작 확인

| 항목 | 결과 |
|---|---|
| librosa 템포·비트·크로마 | OK. 120 BPM 신호 → 117.5 BPM 측정, 가장 강한 음 A (정답 A) |
| pydub + audioop-lts 자르기·크로스페이드 | OK. 10000ms → 7800ms |
| pydub + ffmpeg mp3 내보내기·읽기 | OK |
| pyloudnorm LUFS 측정 | OK. -14.0 LUFS |

## 알아둘 점

- pydub 0.25.1을 처음 import할 때 `SyntaxWarning: invalid escape sequence` 경고가 나온다. Python 3.12부터 생긴 경고이고 동작에는 영향 없다.
- pydub는 내부에서 `audioop`을 쓰는데 Python 3.13에서 제거됐다. `audioop-lts`가 같이 설치돼 있어야 한다 (pyproject.toml에 포함).
- mp3 읽기·쓰기는 ffmpeg가 시스템에 설치돼 있어야 한다. uv로는 설치되지 않는다.
- librosa 템포 추정이 정확히 120이 아니라 117.5로 나왔다. 합성 신호 기준이고 실제 곡 정확도는 10절 검증 계획에서 따로 확인해야 한다.
- Demucs, allin1, Whisper, Lyria는 이번 검증 범위가 아니다.
