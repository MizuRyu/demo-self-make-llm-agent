import os
import subprocess

from models import (
    ListFileParams,
    ReadFileParams,
    WriteFileParams,
    AskQuestionParams,
    ExecuteCommandParams,
    CompleteParams,
    ToolResponse,
)

# 6つのツールを定
# ListFile: ディレクトリ内のファイル一覧を取得
def list_file(params: ListFileParams) -> ToolResponse:
    """
    ディレクトリ内のファイル一覧を取得するツール
    """
    path = params.path
    recursive = params.recursive.lower() == "true"

    if not os.path.exists(path):
        return ToolResponse(False, f"パスが存在しません: {path}")
    
    collected_paths = []
    try:
        if recursive:
            for root, dirs, files in os.walk(path):
                for name in files:
                    full_path = os.path.join(root, name)
                    collected_paths.append(full_path)
                for d in dirs:
                    full_path = os.path.join(root, d)
                    collected_paths.append(full_path)
        else:
            with os.scandir(path) as entries:
                for entry in entries:
                    collected_paths.append(os.path.join(path, entry.name))
    except Exception as e:
        return ToolResponse(False, f"ディレクトリの読み取りに失敗しました: {str(e)}")
    
    if not collected_paths:
        return ToolResponse(True, f"ディレクトリ {path} にファイルディレクトリはありません")
    
    result_msg = f"ディレクトリ {path} のファイル一覧:\n"
    for item in collected_paths:
        result_msg += f"{item}\n"

    return ToolResponse(True, result_msg)

# ReadFile: ファイルの内容を読み込む
def read_file(params: ReadFileParams) -> ToolResponse:
    """
    ファイルの内容を読み込むツール
    """
    path = params.path

    if not os.path.exists(path):
        return ToolResponse(False, f"ファイルが存在しません: {path}")
    
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return ToolResponse(False, f"ファイルの読み取りに失敗しました: {str(e)}")
    
    return ToolResponse(True, content)

# WriteFile: ファイルに書き込む
def write_file(params: WriteFileParams) -> ToolResponse:
    """
    ファイルに内容を書き込むツール
    """
    try:
        # ディレクトリが存在しない場合作成
        print(params.path)
        os.makedirs(os.path.dirname(params.path), exist_ok=True)
        with open(params.path, "w", encoding="utf-8") as f:
            f.write(params.content)
    except Exception as e:
        return ToolResponse(False, f"ファイルの書き込みに失敗しました: {str(e)}")
    
    return ToolResponse(True, f"ファイル {params.path} に書き込みました")

# AskQuestion: ユーザーに質問
def ask_question(params: AskQuestionParams) -> ToolResponse:
    """
    ユーザーに質問するツール。ユーザーの回答を返却する。
    """
    print(f"\n質問: {params.question}")
    answer = input("回答: ") # CLIでの入力を想定
    return ToolResponse(True, f"ユーザーの回答: {answer}")

# ExecuteCommand: コマンドを実行
def execute_command(params: ExecuteCommandParams) -> ToolResponse:
    """
    コマンドを実行するツール
    """
    # ユーザーに実行の承認を求めるため
    requires_approval = params.requires_approval.lower() == "true"
    if requires_approval:
        print(f"\nこちらのコマンドを実行しても良いですか？: {params.command}")
        approval = input("[y/n]: ")
        if approval.lower() != "y":
            return ToolResponse(False, "コマンドの実行が拒否（キャンセル）されました")
        
    try:
        completed = subprocess.run(
            params.command,
            shell=True,
            capture_output=True,
            text=True,
        )
        if completed.returncode != 0:
            return ToolResponse(False, f"コマンドの実行に失敗しました: {completed.stderr}")
    
    except Exception as e:
        return ToolResponse(False, f"コマンドの実行に失敗しました: {str(e)}")
    
    return ToolResponse(True, f"コマンドの実行結果: {completed.stdout}")

# Complete: タスク完了の目印
def complete(params: CompleteParams) -> ToolResponse:
    """
    タスクの完了を示すツール
    """
    return ToolResponse(True, f"タスク完了: {params.result}")