from app.core.analyzer import InputAnalyzer
from app.core.router import Router
from app.core.prompt_builder import PromptBuilder
from app.core.validator import ResponseValidator
from app.core.fallback import FallbackManager
from app.core.cost_tracker import CostTracker
from app.providers.openai_provider import OpenAIProvider

class Orchestrator:
    def __init__(self):
        self.analyzer = InputAnalyzer()
        self.router = Router()
        self.prompt_builder = PromptBuilder()
        self.validator = ResponseValidator()
        self.fallback = FallbackManager()
        self.cost_tracker = CostTracker()
        self.openai_provider = OpenAIProvider()

    def handle_request(self, request):
        analysis = self.analyzer.analyze(request.user_input)
        selected = self.router.select_model(analysis, request.max_budget)
        messages = self.prompt_builder.build(request.user_input, analysis)

        fallback_used = False

        try:
            result = self.openai_provider.generate(messages, selected["model"])
            response_text = result["text"]

            if not self.validator.validate(response_text):
                raise ValueError("Invalid response")

        except Exception:
            fallback_used = True
            fallback_model = self.fallback.get_fallback(selected)
            result = self.openai_provider.generate(messages, fallback_model["model"])
            response_text = result["text"]
            selected = fallback_model

        return {
            "selected_model": selected["model"],
            "provider": selected["provider"],
            "response": response_text,
            "fallback_used": fallback_used,
            "estimated_cost": self.cost_tracker.estimate_cost(selected["model"])
        }
