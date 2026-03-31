class CostTracker:
    MODEL_COSTS = {
        "gpt-4o-mini": 0.001,
        "gpt-4o": 0.01
    }

    def estimate_cost(self, model: str) -> float:
        return self.MODEL_COSTS.get(model, 0.005)
