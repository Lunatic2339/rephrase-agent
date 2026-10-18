# RePhrase CLI 진입점: uv run main.py
# 그래프 구조를 출력하고 싶으면: uv run main.py --draw
import sys

from dotenv import load_dotenv

from rephrase.graph import build_graph


def main():
    # 1) .env에서 API 키 읽기 (OPENAI_API_KEY, GOOGLE_API_KEY)
    load_dotenv()

    # 2) 그래프 만들기
    graph = build_graph()

    if "--draw" in sys.argv:
        print(graph.get_graph().draw_ascii())
        return

    # 3) 수업 방식 CLI 루프: exit/quit 입력 시 종료
    print("RePhrase - 곡 파일 경로와 요청을 입력하세요. (종료: exit)")
    while True:
        song_path = input("\n곡 파일 경로 > ").strip()
        if song_path.lower() in ("exit", "quit"):
            break
        request = input("요청 > ").strip()
        if request.lower() in ("exit", "quit"):
            break

        result = graph.invoke({"song_path": song_path, "request": request})

        print("\n[실행 기록]")
        for line in result.get("logs", []):
            print(" -", line)


if __name__ == "__main__":
    main()
