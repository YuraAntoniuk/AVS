import argparse
import os
from audio_extractor import AudioExtractor
from audio_transcriber import AudioTranscriber
from text_summarizer import TextSummarizer

def main():
    parser = argparse.ArgumentParser(description="Video to Summary Converter")
    parser.add_argument("--video", required=True, help="Path to input video file")
    parser.add_argument("--audio", default="output_audio.wav", help="Path for output audio file")
    parser.add_argument("--transcribe", default="transcribe.txt", help="Path for output transcription file")
    parser.add_argument("--summary", default="summary.txt", help="Path for output summary file")
    args = parser.parse_args()

    if not os.path.exists(args.video):
        print(f"Error: Video file {args.video} does not exist")
        return

    # Step 1: Extract audio
    extractor = AudioExtractor(args.video, args.audio)
    extracted_audio = extractor.extract_audio()
    if not extracted_audio:
        print("Audio extraction failed")
        return

    # Step 2: Transcribe audio
    transcriber = AudioTranscriber(extracted_audio, args.transcribe)
    transcribed_text = transcriber.transcribe_audio()
    if not transcribed_text:
        print("Transcription failed")
        return

    # Step 3: Summarize text
    summarizer = TextSummarizer(transcribed_text)
    summary = summarizer.summarize()
    if not summary:
        print("Summarization failed")
        return

    # Save and display summary
    with open(args.summary, 'w') as f:
        f.write(summary)
    print(f"Summary saved to {args.summary}")
    print("\nSummary:\n", summary)

if __name__ == "__main__":
    main()