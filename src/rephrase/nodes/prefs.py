# 메모리: 편집 취향 불러오기·저장
from rephrase.state import State


def load_prefs(state: State):
    # TODO: sqlite 테이블에서 저장된 취향을 읽기
    prefs = {"keep_solo": False, "max_chorus_repeat": 2}
    return {"prefs": prefs, "logs": ["load_prefs: 기본 취향"]}


def save_prefs(state: State):
    # TODO: "다음에도 이렇게 할까요?" 확인 후 sqlite에 저장
    return {"logs": ["save_prefs: (저장 생략)"]}
