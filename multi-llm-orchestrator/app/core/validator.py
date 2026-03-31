class ResponseValidator:
    def validate(self, response_text: str) -> bool:
        return bool(response_text and len(response_text.strip()) > 0)
