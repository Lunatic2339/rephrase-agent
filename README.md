# Re:Phrase (rephrase-agent)

옛 명곡의 프레이즈를 지금의 귀에 맞게 다시 짜는 LangGraph 음악 재구성 에이전트.

곡을 정확히 n분으로 자르는 대신 인트로·벌스·프리코러스·코러스·브릿지·솔로 같은 구조 단위로 분석해, 반복과 늘어지는 구간을 줄이고 훅을 앞으로 당긴 짧은 버전을 만든다.
중앙대 Interactive Intelligent System Design 수업 팀 텀프로젝트.

> 현재 상태: 골격만 있다. 그래프는 연결돼 있지만 노드는 모두 가짜 값을 돌려주는 빈 함수다.

## 실행

준비물: [uv](https://docs.astral.sh/uv/), ffmpeg (mp3 읽기·쓰기에 필요, 별도 설치)

```bash
uv sync                      # 의존성 설치 (Python 3.13)
cp .env.example .env         # API 키 입력
uv run tests/check_env.py    # 환경 검증
uv run main.py --draw        # 그래프 구조 출력
uv run main.py               # CLI 실행 (exit로 종료)
```

## 구조

```
main.py               # CLI 진입점
src/rephrase/
  state.py            # 그래프 State
  graph.py            # 노드 연결, 라우터
  nodes/              # 노드 함수
  tools/              # 오디오 분석·편집 도구 (예정)
  prompts/            # LLM 프롬프트 (예정)
cache_builder/        # Demucs·allin1용 별도 환경 (예정)
data/songs/           # 원본 음원 (커밋 금지)
data/cache/           # 분석 캐시 JSON (커밋 가능)
data/output/          # 결과 음원 (커밋 금지)
tests/                # 환경 검증 등
docs/                 # 그래프 설명, 환경 검증 결과
```

자세한 그래프 설명은 [docs/graph.md](docs/graph.md), 환경 검증 결과는 [docs/env-check.md](docs/env-check.md).

## 음원과 저작권

음원 파일(`*.mp3`, `*.wav`, `*.flac` 등)은 레포에 커밋하지 않는다. 데모는 무료 라이선스 음원이나 자작곡을 쓴다.

## 라이선스

미정 (팀 동의 후 결정, 권장안은 MIT).
