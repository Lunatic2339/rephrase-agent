# 렌더링과 렌더링 후 검증
from rephrase.state import State


def renderer(state: State):
    # TODO: pydub로 계획대로 구간을 잇고 크로스페이드, data/output/에 저장
    return {"logs": [f"renderer: 구간 {len(state['plan'])}개"]}


def render_checker(state: State):
    # TODO: pyloudnorm으로 연결부 음량 차(2dB 이내)·에너지 확인
    report = {"passed": True, "lufs_gaps": []}
    return {"render_report": report, "logs": [f"render_checker: {report}"]}
