# 노드를 연결해 LangGraph 그래프를 만든다.
from typing import Literal

from langgraph.graph import StateGraph, START, END

from rephrase.state import State, MAX_PLAN_RETRY, MAX_ENDING_RETRY
from rephrase.nodes import (
    input_guard, mode_router, load_prefs, save_prefs,
    analyze_beat_key, analyze_vocal, analyze_lyrics, analyze_structure,
    structure_review, planner, plan_checker,
    ending_maker, clip_meter, renderer, render_checker,
    human_review, feedback_parser,
)

ANALYZERS = ["analyze_beat_key", "analyze_vocal", "analyze_lyrics", "analyze_structure"]


# ----- 라우터: State를 보고 다음 갈 곳의 라벨(Literal)을 돌려준다 -----
def route_guard(state: State) -> Literal["ok", "reject"]:
    return "ok" if state.get("guard_ok") else "reject"


def route_mode(state: State) -> list[str]:
    # 재구성 모드면 분석 노드 4개 이름을 리스트로 돌려줘 병렬 실행(fan-out)
    # 메들리는 확장 기능이라 지금은 바로 종료
    if state.get("mode") == "medley":
        return [END]
    return ANALYZERS


def route_plan(state: State) -> Literal["retry", "fade", "clean"]:
    # 검증 실패면 재계획. 단, 한도를 넘겨 이미 단순안을 냈으면 그대로 진행
    passed = state["check_report"].get("passed")
    if not passed and state.get("revision", 0) <= MAX_PLAN_RETRY:
        return "retry"
    # 통과 후: 원곡이 페이드아웃이면 엔딩 생성, 아니면 바로 렌더링
    # TODO: 원곡 끝부분 음량이 서서히 줄면 페이드아웃으로 판단
    return "fade" if state["analysis"].get("fade_out") else "clean"


def route_clip(state: State) -> Literal["pass", "retry"]:
    ending = state["ending"]
    if ending.get("passed") or ending.get("attempts", 0) >= MAX_ENDING_RETRY:
        return "pass"
    return "retry"


def route_review(state: State) -> Literal["approve", "revise"]:
    return "approve" if state.get("review") == "approve" else "revise"


def build_graph():
    builder = StateGraph(State)

    # 노드 등록
    builder.add_node("input_guard", input_guard)
    builder.add_node("load_prefs", load_prefs)
    builder.add_node("mode_router", mode_router)
    builder.add_node("analyze_beat_key", analyze_beat_key)
    builder.add_node("analyze_vocal", analyze_vocal)
    builder.add_node("analyze_lyrics", analyze_lyrics)
    builder.add_node("analyze_structure", analyze_structure)
    builder.add_node("structure_review", structure_review)
    builder.add_node("planner", planner)
    builder.add_node("plan_checker", plan_checker)
    builder.add_node("ending_maker", ending_maker)
    builder.add_node("clip_meter", clip_meter)
    builder.add_node("renderer", renderer)
    builder.add_node("render_checker", render_checker)
    builder.add_node("human_review", human_review)
    builder.add_node("feedback_parser", feedback_parser)
    builder.add_node("save_prefs", save_prefs)

    # 입력 → 가드레일 → 취향 → 모드
    builder.add_edge(START, "input_guard")
    builder.add_conditional_edges("input_guard", route_guard,
                                  {"ok": "load_prefs", "reject": END})
    builder.add_edge("load_prefs", "mode_router")

    # 재구성 모드면 분석 4개를 병렬로 실행 (Parallelization)
    builder.add_conditional_edges("mode_router", route_mode, ANALYZERS + [END])
    # 4개가 모두 끝나야 구조 확인으로 (join)
    builder.add_edge(ANALYZERS, "structure_review")

    # 계획 ↔ 검증 루프 (Reflection)
    builder.add_edge("structure_review", "planner")
    builder.add_edge("planner", "plan_checker")
    # 통과하면 페이드아웃 여부에 따라 엔딩 생성 루프를 거치거나 바로 렌더링
    builder.add_conditional_edges("plan_checker", route_plan,
                                  {"retry": "planner", "fade": "ending_maker",
                                   "clean": "renderer"})
    builder.add_edge("ending_maker", "clip_meter")
    builder.add_conditional_edges("clip_meter", route_clip,
                                  {"retry": "ending_maker", "pass": "renderer"})

    # 렌더링 → 검증 → 사람 청취 → 승인이면 취향 저장, 수정이면 재계획
    builder.add_edge("renderer", "render_checker")
    builder.add_edge("render_checker", "human_review")
    builder.add_conditional_edges("human_review", route_review,
                                  {"approve": "save_prefs", "revise": "feedback_parser"})
    builder.add_edge("feedback_parser", "planner")
    builder.add_edge("save_prefs", END)

    return builder.compile()
