class Router:
    def select_model(self, analysis: dict, max_budget: float) -> dict:
        task = analysis["task"]
        complexity = analysis["complexity"]

        if task == "coding":
            return {"provider": "openai", "model": "gpt-4o"}

        if task == "long_doc":
            return {"provider": "openai", "model": "gpt-4o"}

        if complexity == "low" and max_budget <= 0.05:
            return {"provider": "openai", "model": "gpt-4o-mini"}

        return {"provider": "openai", "model": "gpt-4o-mini"}
