from jiwer import wer, Compose, RemovePunctuation, ToLowerCase, RemoveMultipleSpaces, Strip


class ASREvaluator:
    def __init__(self):
        self.transform = Compose([
            ToLowerCase(),
            RemovePunctuation(),
            RemoveMultipleSpaces(),
            Strip()
        ])

    def evaluate_asr(self, reference_path, transcription_path):
        try:
            with open(reference_path, "r", encoding="utf-8") as f:
                reference = f.read().replace("\n", " ")
                transformed_reference = self.transform(reference)
                if not transformed_reference.strip():
                    return False, "Error: Transformed reference is empty or contains only whitespace."
                reference_words = transformed_reference.split()
                reference_word_count = len(reference_words)

            with open(transcription_path, "r", encoding="utf-8") as f:
                hypothesis = f.read().replace("\n", " ")
                transformed_hypothesis = self.transform(hypothesis)
                if not transformed_hypothesis.strip():
                    return False, "Error: Transformed hypothesis is empty or contains only whitespace."
                hypothesis_words = transformed_hypothesis.split()
                hypothesis_word_count = len(hypothesis_words)

            # Compute WER
            error = wer(transformed_reference, transformed_hypothesis)
            result = (
                f"WER: {error:.2%}\n"
            )
            return True, result

        except FileNotFoundError as e:
            return False, f"Error: File not found - {e}"
        except ValueError as e:
            return False, f"Error: {e}"
        except Exception as e:
            return False, f"Unexpected error: {e}"