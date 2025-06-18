import sys
from transformers import pipeline, BartTokenizer
import nltk
from nltk.tokenize import sent_tokenize

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')


class TextSummarizer:
    def __init__(self, text):
        self.text = text
        try:
            self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
            self.tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")
            print("Summarization pipeline and tokenizer loaded successfully.")
        except Exception as e:
            print(f"Error loading model or tokenizer: {e}")
            sys.exit(1)

    def _split_text_into_chunks(self, max_tokens=1024):
        sentences = sent_tokenize(self.text)
        chunks = []
        current_chunk = []
        current_token_count = 0

        for sentence in sentences:
            sentence_tokens = len(self.tokenizer.encode(sentence, add_special_tokens=False))

            if current_token_count + sentence_tokens > max_tokens:
                if current_chunk:
                    chunks.append(" ".join(current_chunk))
                    current_chunk = []
                    current_token_count = 0
                if sentence_tokens > max_tokens:
                    print(f"Warning: Single sentence exceeds {max_tokens} tokens, truncating.")
                    tokens = self.tokenizer.encode(sentence, add_special_tokens=False)[:max_tokens]
                    sentence = self.tokenizer.decode(tokens, skip_special_tokens=True)
                    chunks.append(sentence)
                    continue

            current_chunk.append(sentence)
            current_token_count += sentence_tokens

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks

    def summarize(self, max_new_tokens=256, min_length=100):
        try:
            total_tokens = len(self.tokenizer.encode(self.text, add_special_tokens=False))
            if total_tokens <= 1024:
                summary = self.summarizer(self.text, max_new_tokens=max_new_tokens, min_length=min_length, do_sample=True, num_beams=4, length_penalty=2.0)
                summary_text = summary[0]['summary_text']
                print("Summarization completed successfully")
                return summary_text

            print(f"Text too long ({total_tokens} tokens), splitting into chunks...")
            chunks = self._split_text_into_chunks(max_tokens=1024)
            summaries = []

            for i, chunk in enumerate(chunks):
                chunk_tokens = len(self.tokenizer.encode(chunk, add_special_tokens=False))
                print(f"Processing chunk {i + 1} with {chunk_tokens} tokens")
                summary = self.summarizer(chunk ,max_new_tokens=256, min_length=min_length, do_sample=True, num_beams=4, length_penalty=2.0)
                summaries.append(summary[0]['summary_text'])

            combined_summary = " ".join(summaries)
            print("Summarization of all chunks completed successfully")
            return combined_summary

        except Exception as e:
            print(f"Error during summarization: {e}")
            return None


# Test the class with the provided article when run directly
if __name__ == "__main__":

    with open("cleaned_text.txt", "r", encoding="utf-8") as f:
        actual_input = f.read()

    summarizer = TextSummarizer(actual_input)
    summary = summarizer.summarize()
    with open("summary1%2.txt", 'w') as f:
        f.write(summary)
    if summary:
        print("\nSummary:\n", summary)