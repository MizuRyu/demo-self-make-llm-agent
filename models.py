class ListFileParams:
    def __init__(self, path: str, recursive: str):
        self.path = path
        self.recursive = recursive

class ReadFileParams:
    def __init__(self, path: str):
        self.path = path

class WriteFileParams:
    def __init__(self, path: str, content: str):
        self.path = path
        self.content = content

class AskQuestionParams:
    def __init__(self, question: str):
        self.question = question

class ExecuteCommandParams:
    def __init__(self, command: str, requires_approval: str):
        self.command = command
        self.requires_approval = requires_approval

class CompleteParams:
    def __init__(self, result: str):
        self.result = result

class ToolResponse:
    def __init__(self, success: bool, msg: str):
        self.success = success
        self.msg = msg

class AgentResponse:
    def __init__(self, tool_response: ToolResponse, tool_type: str, is_complete: bool):
        self.tool_response = tool_response
        self.tool_type = tool_type
        self.is_complete = is_complete