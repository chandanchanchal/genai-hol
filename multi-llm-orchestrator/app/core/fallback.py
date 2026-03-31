class FallbackManager:
    def get_fallback(self, selected_model: dict) -> dict:
        if selected_model["model"] == "gpt-4o":
            return {"provider": "openai", "model": "gpt-4o-mini"}

        return {"provider": "openai", "model": "gpt-4o-mini"}
