class InputAnalyzer:
    def analyze(self, user_input: str) -> dict:
        lowered = user_input.lower()

        if "code" in lowered or "debug" in lowered:
            return {"task": "coding", "complexity": "medium"}

        if len(user_input) > 1000:
            return {"task": "long_doc", "complexity": "high"}

        return {"task": "general", "complexity": "low"}
