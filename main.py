import os
import sys
import openai

from models import AgentResponse
from parser import parse_and_execute_tool

def main():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("APIキーが設定されていません")
        sys.exit(1)
    openai.api_key = api_key

    # システムプロンプト読み込み
    with open("instruction.md", "r") as f:
        system_prompt = f.read()

    print("エージェントに与えるタスクを入力してください...")
    user_task = input("> ")

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_task}
    ]

    is_complete = False
    while not is_complete:
        try:
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )
        except Exception as e:
            print(f"OpenAI API呼び出しに失敗しました: {str(e)}")
            break

        assistant_response = response.choices[0].message.content
        usage_token = response. usage.total_tokens
        print(f"消費総トークン数: {usage_token}")

        agent_response: AgentResponse = parse_and_execute_tool(assistant_response)

        # agent(assistant)のレスポンス(XML)を履歴に追加
        messages.append({"role": "assistant", "content": assistant_response})

        # ツールの実行結果を表示
        # NOTE: 表示したい実行結果があればここに追加
        if agent_response.tool_type not in ("ask_question", "execute_command"):
            print(f"\n[{agent_response.tool_type}] {agent_response.tool_response.msg}")
        
        # ツール実行結果をagent(assistant)に渡す
        messages.append({"role": "user", "content": agent_response.tool_response.msg})

        if agent_response.is_complete:
            is_complete = True
            print("タスクDONE!!!!!!")

if __name__ == "__main__":
    main()