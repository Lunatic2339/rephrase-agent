# 원곡이 페이드아웃일 때만 거치는 엔딩 생성 루프
from rephrase.state import State, MAX_ENDING_RETRY


def ending_maker(state: State):
    # TODO: gemini-3.5-flash-lite로 Lyria 프롬프트 작성 → lyria-3-clip-preview로 엔딩 클립 생성
    ending = dict(state.get("ending", {}))
    ending["attempts"] = ending.get("attempts", 0) + 1
    return {"ending": ending, "logs": [f"ending_maker: {ending['attempts']}회차"]}


def clip_meter(state: State):
    # TODO: librosa로 생성 클립의 BPM·키를 측정해 원곡과 비교
    ending = dict(state["ending"])
    ending["passed"] = True
    if not ending["passed"] and ending["attempts"] >= MAX_ENDING_RETRY:
        ending["fallback"] = "reverb_tail"  # 대체 경로: 잔향 마무리
    return {"ending": ending, "logs": [f"clip_meter: passed={ending['passed']}"]}
