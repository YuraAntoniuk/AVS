import logging
from deepeval import evaluate
from deepeval.models import GeminiModel
from deepeval.metrics import SummarizationMetric
from deepeval.test_case import LLMTestCase


class SummaryEvaluator:
    def __init__(self):
        self.model = GeminiModel(model_name="gemini-2.0-flash", api_key="")

    def evaluate_summary(self, transcribe_path, summary_path):
        try:
            with open(transcribe_path, "r", encoding="utf-8") as f:
                input_text = f.read()
            with open(summary_path, "r", encoding="utf-8") as f:
                actual_output = f.read()

            test_case = LLMTestCase(input=input_text, actual_output=actual_output)
            metric = SummarizationMetric(
                threshold=0.5,
                model=self.model,
                include_reason=True
            )

            # Evaluate
            result = evaluate([test_case], [metric])
            first_result = result.test_results[0]
            metric_data = first_result.metrics_data[0]

            score = metric_data.score
            reason = metric_data.reason

            eval_output = f"Score: {score:.2f}\nReason: {reason}"
            return True, eval_output

        except Exception as e:
            return False, f"Evaluation error (measuring file): {str(e)}"

