# 입력 단계: 가드레일과 모드 결정
from rephrase.state import State


def input_guard(state: State):
    # TODO: gpt-4o-mini로 요청이 음악 재구성 요청인지 판단 (JSON 강제, 실패 시 거부 = fail-closed)
    ok = bool(state.get("request", "").strip())
    return {"guard_ok": ok, "logs": [f"input_guard: ok={ok}"]}


def mode_router(state: State):
    # TODO: 요청을 해석해 재구성/메들리 결정. 메들리는 확장 기능이라 지금은 항상 remix
    return {"mode": "remix", "logs": ["mode_router: remix"]}
