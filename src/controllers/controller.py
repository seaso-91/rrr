from abc import ABC, abstractmethod

class BaseController:
    def __init__(self):
        ...



    @abstractmethod
    def handle_request(self, request):
        """Every child controller must implement this entry point"""

    def send_json_response(self, data: dict, status_code: int = 200) -> dict:
        """Shared helper method for uniform responses."""
        return {
            "status": "success" if status_code < 400 else "error",
            "code": status_code,
            "data": data
        }