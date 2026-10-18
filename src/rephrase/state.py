# 그래프 전체가 공유하는 State 정의 (컨텍스트 문서 6절 초안 기준)
import operator
from typing import Annotated, TypedDict

# 재계획·엔딩 재생성 최대 횟수 (문서 6절: 최대 3회)
MAX_PLAN_RETRY = 3
MAX_ENDING_RETRY = 3


class State(TypedDict, total=False):
    # 사용자 입력
    request: str                       # 사용자가 입력한 요청 문장
    song_path: str                     # 재구성할 곡 파일 경로
    guard_ok: bool                     # 입력 가드레일 통과 여부
    mode: str                          # "remix"(재구성) 또는 "medley"(확장 기능)

    # 병렬 분석 노드 4개가 같은 칸에 쓰므로 dict를 합치는 리듀서(or_) 사용
    analysis: Annotated[dict, operator.or_]
    structure: list                    # 구간 목록 [{"label", "start", "end"}, ...]

    # 계획과 검증 루프
    plan: list                         # 남길 구간과 순서
    check_report: dict                 # 렌더링 전 검증 결과 {"passed", "reasons"}
    revision: int                      # 재계획 횟수

    # 엔딩 생성 루프
    ending: dict                       # {"needed", "bpm", "key", "attempts", "passed", "fallback"}

    # 렌더링과 사람 확인
    render_report: dict                # 렌더링 후 검증 결과
    review: str                        # "approve" 또는 "revise"
    feedback: str                      # 사용자가 남긴 수정 요청

    prefs: dict                        # 저장·불러오는 편집 취향
    logs: Annotated[list, operator.add]  # 노드 실행 기록 (여러 노드가 이어 붙임)
