import xml.etree.ElementTree as ET
import re
from models import (
    ListFileParams,
    ReadFileParams,
    WriteFileParams,
    AskQuestionParams,
    ExecuteCommandParams,
    CompleteParams,
    ToolResponse,
    AgentResponse,
)

from tool import (
    list_file,
    read_file,
    write_file,
    ask_question,
    execute_command,
    complete,
)

TOOL_LIST_FILE = "list_file"
TOOL_READ_FILE = "read_file"
TOOL_WRITE_FILE = "write_file"
TOOL_ASK_QUESTION = "ask_question"
TOOL_EXECUTE_COMMAND = "execute_command"
TOOL_COMPLETE = "complete"


def parse_and_execute_tool(response: str) -> AgentResponse:
    """
    LLMのレスポンスをXMLパースし、適切なツールを呼び出す
    return: (ToolRespons, tool_type, is_complete)
    """
    # <tag>...</tag>の部分を正規表現でgrep
    pattern = r"<([a-z_]+)>([\s\S]*?)</\1>"
    match = re.search(pattern, response)
    if not match:
        return ToolResponse(False, "該当するツールが見つかりません"), None, False
    
    tool_type = match.group(1)
    tool_body = match.group(2)

    # XMLとしてパースするため、再構成
    xml_str = f"<tool_type>{tool_body}</tool_type>"

    try:
        root = ET.fromstring(xml_str)
    except Exception as e:
        return AgentResponse(
            ToolResponse(False, f"XMLパースエラー: {e}"),
            tool_type,
            False
        )
    if tool_type == TOOL_LIST_FILE:
        path = root.find("path").text if root.find("path") is not None else ""
        recursive = root.find("recursive").text if root.find("recursive") is not None else "false"
        params = ListFileParams(path, recursive)
        return AgentResponse(
            list_file(params),
            tool_type,
            False
        )
    elif tool_type == TOOL_READ_FILE:
        path = root.find("path").text if root.find("path") is not None else ""
        params = ReadFileParams(path)
        return AgentResponse(
            read_file(params),
            tool_type,
            False
        )
    elif tool_type == TOOL_WRITE_FILE:
        path = root.find("path").text if root.find("path") is not None else ""
        content = root.find("content").text if root.find("content") is not None else ""
        params = WriteFileParams(path, content)
        return AgentResponse(
            write_file(params),
            tool_type,
            False
        )
    elif tool_type == TOOL_ASK_QUESTION:
        question = root.find("question").text if root.find("question") is not None else ""
        params = AskQuestionParams(question)
        return AgentResponse(
            ask_question(params),
            tool_type,
            False
        )
    elif tool_type == TOOL_EXECUTE_COMMAND:
        command = root.find("command").text if root.find("command") is not None else ""
        requires_approval = root.find("requires_approval").text if root.find("requires_approval") is not None else "false"
        params = ExecuteCommandParams(command, requires_approval)
        return AgentResponse(
            execute_command(params),
            tool_type,
            False
        )
    elif tool_type == TOOL_COMPLETE:
        result = root.find("result").text if root.find("result") is not None else ""
        params = CompleteParams(result)
        return AgentResponse(
            complete(params),
            tool_type,
            True
        )
    else:
        return AgentResponse(
            ToolResponse(False, f"未知のツール: {tool_type}"),
            tool_type,
            False
        )