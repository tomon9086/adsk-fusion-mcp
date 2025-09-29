from typing import Union


class RpcResponse:
    def __init__(self, success: bool, message: Union[str, list[str]]):
        self.success = success
        self.message = message if isinstance(message, str) else "; ".join(message)

    def to_dict(self):
        return {"success": self.success, "message": self.message}

    def to_text(self) -> str:
        return "{}: {}".format("OK" if self.success else "ERROR", self.message)

    @staticmethod
    def of(dict: dict):
        return RpcResponse(
            success=dict.get("success", False),
            message=dict.get("message", ""),
        )
