# 사람 개입 2: 결과 청취 후 승인/수정
from rephrase.state import State


def human_review(state: State):
    print("\n[재구성 계획]")
    for s in state["plan"]:
        print(f"  {s['label']:8s} {s['start']:6.1f}s ~ {s['end']:6.1f}s")
    answer = input("승인하면 y, 고칠 점이 있으면 내용을 입력 > ").strip()
    if answer.lower() in ("y", "yes", ""):
        return {"review": "approve", "logs": ["human_review: 승인"]}
    return {"review": "revise", "feedback": answer, "logs": ["human_review: 수정 요청"]}


def feedback_parser(state: State):
    # TODO: gpt-4o-mini로 피드백을 취향 항목(예: keep_solo=True)으로 변환
    # 재계획 횟수를 0으로 되돌려 다시 계획하게 한다
    return {"revision": 0, "logs": [f"feedback_parser: {state.get('feedback', '')}"]}
