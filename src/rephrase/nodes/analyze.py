# 병렬 분석 노드 4개. 각자 analysis 딕셔너리의 다른 키에 써서 리듀서(or_)로 합쳐진다.
from rephrase.state import State


def analyze_beat_key(state: State):
    # TODO: librosa로 템포·비트·키·에너지 측정 (다운비트는 캐시 또는 추정)
    return {"analysis": {"beat_key": {"bpm": 120.0, "key": "A minor"}},
            "logs": ["analyze_beat_key"]}


def analyze_vocal(state: State):
    # TODO: Demucs 캐시에서 보컬 있는 구간 읽기
    return {"analysis": {"vocal": [{"start": 15.0, "end": 60.0}]},
            "logs": ["analyze_vocal"]}


def analyze_lyrics(state: State):
    # TODO: Whisper로 가사 단어 시각 얻기
    return {"analysis": {"lyrics": []}, "logs": ["analyze_lyrics"]}


def analyze_structure(state: State):
    # TODO: allin1 캐시에서 구조 라벨 읽기 + 프리코러스 규칙 적용
    sections = [
        {"label": "intro", "start": 0.0, "end": 30.0},
        {"label": "verse", "start": 30.0, "end": 60.0},
        {"label": "chorus", "start": 60.0, "end": 90.0},
        {"label": "verse", "start": 90.0, "end": 120.0},
        {"label": "chorus", "start": 120.0, "end": 150.0},
        {"label": "solo", "start": 150.0, "end": 210.0},
        {"label": "chorus", "start": 210.0, "end": 240.0},
        {"label": "outro", "start": 240.0, "end": 280.0},
    ]
    return {"analysis": {"structure": sections}, "logs": ["analyze_structure"]}
