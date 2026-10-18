# 구조 확인(사람) → 재구성 계획(LLM) → 렌더링 전 검증
from rephrase.state import State, MAX_PLAN_RETRY


def structure_review(state: State):
    # 사람 개입 1: 분석된 구조를 보여 주고 수정 기회를 준다 (수업 방식대로 input() 사용)
    sections = state["analysis"].get("structure", [])
    print("\n[분석된 곡 구조]")
    for i, s in enumerate(sections):
        print(f"  {i}: {s['label']:8s} {s['start']:6.1f}s ~ {s['end']:6.1f}s")
    input("구조가 맞으면 Enter (수정 기능은 TODO) > ")
    return {"structure": sections, "logs": ["structure_review"]}


def planner(state: State):
    # TODO: gpt-4o에 구조·취향·검증 실패 이유를 주고 남길 구간 순서를 JSON으로 받기
    revision = state.get("revision", 0)
    if revision >= MAX_PLAN_RETRY:
        # 대체 경로: 재계획이 계속 실패하면 코러스 중심 단순안
        plan = [s for s in state["structure"] if s["label"] == "chorus"][:2]
        note = "planner: 코러스 중심 단순안"
    else:
        keep = {"verse", "chorus"}
        plan = [s for s in state["structure"] if s["label"] in keep]
        note = f"planner: 계획 {revision + 1}회차"
    return {"plan": plan, "revision": revision + 1, "logs": [note]}


def plan_checker(state: State):
    # TODO: 재구성 규칙(문서 5절) 코드 검증 - 인트로 길이, 첫 훅 위치, 코러스 반복 횟수 등
    reasons = []
    chorus_count = sum(1 for s in state["plan"] if s["label"] == "chorus")
    if chorus_count > state["prefs"].get("max_chorus_repeat", 2):
        reasons.append(f"코러스가 {chorus_count}회 반복됨")
    report = {"passed": not reasons, "reasons": reasons}
    return {"check_report": report, "logs": [f"plan_checker: {report}"]}
