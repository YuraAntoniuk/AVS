import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk  # For displaying images in Tkinter
import cv2  # For frame extraction
import os
from audio_extractor import AudioExtractor
from audio_transcriber import AudioTranscriber
from text_summarizer import TextSummarizer
from measuring_llm_quality import SummaryEvaluator
from asr_evaluator import ASREvaluator  # Import the new ASR evaluator

class VideoProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video to Summary Converter")
        self.root.geometry("1000x600")  # Increased size to accommodate WER results

        # Variables
        self.video_path = tk.StringVar(value="")
        self.audio_path = tk.StringVar(value="output_audio.wav")
        self.transcribe_path = tk.StringVar(value="transcribe.txt")
        self.reference_path = tk.StringVar(value="reference.txt")  # New: Reference subtitle path
        self.summary_path = tk.StringVar(value="summary.txt")
        self.frame_path = tk.StringVar(value="frame.jpg")
        self.frame_time = tk.DoubleVar(value=1.0)  # Time to extract frame (seconds)

        # Initialize evaluators
        self.summary_evaluator = SummaryEvaluator()  # Replace with your API key
        self.asr_evaluator = ASREvaluator()

        # GUI Elements
        left_frame = tk.Frame(root)
        left_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nw")

        right_frame = tk.Frame(root)
        right_frame.grid(row=0, column=1, padx=20, pady=20, sticky="ne")

        # --- Left frame: Input fields, Transcription, and Summary ---
        row = 0
        tk.Label(left_frame, text="Select Video File:").grid(row=row, column=0, sticky='e', pady=5)  # Right-align label
        tk.Entry(left_frame, textvariable=self.video_path, width=50).grid(row=row, column=1, pady=5,
                                                                          sticky='w')  # Left-align entry
        tk.Button(left_frame, text="Browse", command=self.browse_video).grid(row=row, column=2, padx=5)

        row += 1
        tk.Label(left_frame, text="Reference Subtitle File:").grid(row=row, column=0, sticky='e',
                                                                   pady=5)  # Right-align label
        tk.Entry(left_frame, textvariable=self.reference_path, width=50).grid(row=row, column=1, pady=5,
                                                                              sticky='w')  # Left-align entry
        tk.Button(left_frame, text="Browse Reference", command=self.browse_reference).grid(row=row, column=2, padx=5)

        row += 1
        tk.Label(left_frame, text="Audio Output Path:").grid(row=row, column=0, sticky='e', pady=5)  # Right-align label
        tk.Entry(left_frame, textvariable=self.audio_path, width=50).grid(row=row, column=1, pady=5,
                                                                          sticky='w')  # Left-align entry

        row += 1
        tk.Label(left_frame, text="Transcription Output Path:").grid(row=row, column=0, sticky='e',
                                                                     pady=5)  # Right-align label
        tk.Entry(left_frame, textvariable=self.transcribe_path, width=50).grid(row=row, column=1, pady=5,
                                                                               sticky='w')  # Left-align entry

        row += 1
        tk.Label(left_frame, text="Summary Output Path:").grid(row=row, column=0, sticky='e',
                                                               pady=5)  # Right-align label
        tk.Entry(left_frame, textvariable=self.summary_path, width=50).grid(row=row, column=1, pady=5,
                                                                            sticky='w')  # Left-align entry

        row += 1
        tk.Label(left_frame, text="Frame Output Path:").grid(row=row, column=0, sticky='e', pady=5)  # Right-align label
        tk.Entry(left_frame, textvariable=self.frame_path, width=50).grid(row=row, column=1, pady=5,
                                                                          sticky='w')  # Left-align entry

        row += 1
        tk.Label(left_frame, text="Frame Time (seconds):").grid(row=row, column=0, sticky='e',
                                                                pady=5)  # Right-align label
        tk.Entry(left_frame, textvariable=self.frame_time, width=10).grid(row=row, column=1, pady=5,
                                                                          sticky='w')  # Left-align entry

        row += 1
        tk.Button(left_frame, text="Process Video", command=self.process_video).grid(row=row, column=0, columnspan=3,
                                                                                     pady=10)

        row += 1
        tk.Label(left_frame, text="Transcription:").grid(row=row, column=0, sticky='w', pady=5)

        row += 1
        self.transcribe_text = tk.Text(left_frame, height=6, width=70)
        self.transcribe_text.grid(row=row, column=0, columnspan=3, pady=5)

        row += 1
        tk.Label(left_frame, text="Summary:").grid(row=row, column=0, sticky='w', pady=5)

        row += 1
        self.summary_text = tk.Text(left_frame, height=6, width=70)
        self.summary_text.grid(row=row, column=0, columnspan=3, pady=5)

        tk.Label(right_frame, text="Video Frame Preview:").pack(pady=5)
        self.frame_label = tk.Label(right_frame)
        self.frame_label.pack(pady=5)
        self.photo = None

        # --- Right frame: for video preview ---
        tk.Label(right_frame, text="WER Results:").pack(pady=5)
        self.wer_text = tk.Text(right_frame, height=4, width=40)  # Adjusted width for right frame
        self.wer_text.pack(pady=5)

        tk.Label(right_frame, text="Evaluation Results:").pack(pady=5)
        self.eval_text = tk.Text(right_frame, height=4, width=40)  # Adjusted width for right frame
        self.eval_text.pack(pady=5)




    def browse_video(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mkv")])
        if file_path:
            filename = os.path.basename(file_path)  # e.g., 'my_video.mp4'
            base_path = os.path.splitext(filename)[0]  # e.g., 'my_video'
            self.video_path.set(file_path)
            # Set default audio, transcribe, summary, and frame paths based on video path
            self.audio_path.set(f"audios/{base_path}_audio.wav")
            self.transcribe_path.set(f"transcription_results/{base_path}_transcribe.txt")
            self.summary_path.set(f"summarizing_results/{base_path}_summary.txt")
            self.frame_path.set(f"video_frames/{base_path}_frame.jpg")

    def browse_reference(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            self.reference_path.set(file_path)

    def extract_frame(self, video_path, output_image, time_seconds):
        try:
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                self.summary_text.insert(tk.END, f"Error: Could not open video file {video_path}\n")
                return False

            cap.set(cv2.CAP_PROP_POS_MSEC, time_seconds * 1000)
            success, frame = cap.read()
            if not success:
                self.summary_text.insert(tk.END, "Error: Could not read frame from video\n")
                cap.release()
                return False

            cv2.imwrite(output_image, frame)
            self.summary_text.insert(tk.END, f"Frame saved to {output_image}\n")
            cap.release()

            image = Image.open(output_image)
            image.thumbnail((300, 300))
            self.photo = ImageTk.PhotoImage(image)
            self.frame_label.configure(image=self.photo)
            self.frame_label.image = self.photo
            return True

        except Exception as e:
            self.summary_text.insert(tk.END, f"Error extracting frame: {str(e)}\n")
            return False

    def process_video(self):
        video_path = self.video_path.get()
        audio_path = self.audio_path.get()
        transcribe_path = self.transcribe_path.get()
        reference_path = self.reference_path.get()
        summary_path = self.summary_path.get()
        frame_path = self.frame_path.get()
        frame_time = self.frame_time.get()

        if not video_path or not os.path.exists(video_path):
            messagebox.showerror("Error", "Please select a valid video file")
            return

        self.transcribe_text.delete(1.0, tk.END)
        self.wer_text.delete(1.0, tk.END)
        self.summary_text.delete(1.0, tk.END)
        self.eval_text.delete(1.0, tk.END)
        self.summary_text.insert(tk.END, "Processing...\n")
        self.frame_label.configure(image="")

        try:
            # Step 1: Extract frame
            if not self.extract_frame(video_path, frame_path, frame_time):
                messagebox.showerror("Error", "Frame extraction failed")
                return

            # Step 2: Extract audio
            extractor = AudioExtractor(video_path, audio_path)
            extracted_audio = extractor.extract_audio()
            if not extracted_audio:
                self.summary_text.insert(tk.END, "Audio extraction failed\n")
                messagebox.showerror("Error", "Audio extraction failed")
                return

            # Step 3: Transcribe audio
            transcriber = AudioTranscriber(extracted_audio, transcribe_path)
            transcribed_text = transcriber.transcribe_audio()
            if not transcribed_text:
                self.transcribe_text.insert(tk.END, "Transcription failed\n")
                self.summary_text.insert(tk.END, "Transcription failed\n")
                messagebox.showerror("Error", "Transcription failed")
                return

            self.transcribe_text.insert(tk.END, transcribed_text)
            self.summary_text.insert(tk.END, f"Transcription saved to {transcribe_path}\n")

            # Step 4: Evaluate ASR (WER)
            if reference_path and os.path.exists(reference_path):
                success, wer_result = self.asr_evaluator.evaluate_asr(reference_path, transcribe_path)
                self.wer_text.insert(tk.END, wer_result)
                if not success:
                    self.summary_text.insert(tk.END, "WER evaluation failed\n")
                    messagebox.showwarning("Warning", "WER evaluation failed")
            else:
                self.wer_text.insert(tk.END, "No reference file provided or file does not exist\n")
                self.summary_text.insert(tk.END, "Skipping WER evaluation: No reference file\n")

            # Step 5: Summarize text
            summarizer = TextSummarizer(transcribed_text)
            summary = summarizer.summarize(max_new_tokens=256, min_length=100)
            if not summary:
                self.summary_text.insert(tk.END, "Summarization failed\n")
                messagebox.showerror("Error", "Summarization failed")
                return

            with open(summary_path, 'w') as f:
                f.write(summary)
            self.summary_text.delete(1.0, tk.END)
            self.summary_text.insert(tk.END, summary)
            self.summary_text.insert(tk.END, f"\nSummary saved to {summary_path}\n")

            # Step 6: Evaluate summary
            success, eval_output = self.summary_evaluator.evaluate_summary(transcribe_path, summary_path)
            self.eval_text.delete(1.0, tk.END)
            self.eval_text.insert(tk.END, eval_output)
            if not success:
                messagebox.showerror("Error", "Summary evaluation failed")
                return

            messagebox.showinfo("Success", f"Transcription saved to {transcribe_path}\nSummary saved to {summary_path}")

        except Exception as e:
            self.summary_text.insert(tk.END, f"Error: {str(e)}\n")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoProcessorApp(root)
    root.mainloop()