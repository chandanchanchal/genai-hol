class PromptBuilder:
    def build(self, user_input: str, analysis: dict) -> list:
        task = analysis["task"]

        system_prompt = f"You are an expert assistant specialized in {task}."

        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
