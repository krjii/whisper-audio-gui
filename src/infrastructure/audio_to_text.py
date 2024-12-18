import whisper
from datetime import datetime
import logging

from infrastructure.thread_worker import ThreadWorker


class AudioText:
    """
    Class for processing audio files and converting them to text using Whisper.
    """

    def __init__(self, result_callback=None, log_callback=None):
        super().__init__()

        self.__result_callback = result_callback
        self.__progress_callback = None
        self.__log_callback = log_callback

        print("Initializing audio_to_text...")
        try:
            # Correct model name (e.g., 'base' instead of 'turbo')
            self.model = whisper.load_model("base")
        except AttributeError as e:
            print(f"Error: {e}")
            print("Whisper module not found or incorrect import?")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            print("Initialization complete.")

        # Placeholder for the worker
        self.worker = None

    def process_file(self, file_name):
        """
        Process the selected audio file using Whisper.
        """
        try:
            result = self.model.transcribe(audio=file_name, verbose=False)
            return file_name, result['text']
        except Exception as e:
            logging.error(f"Error processing file: {e}")
            return file_name, f"Error: {e}"

    def save_results(self, result_data):
        """
        Save transcription results to a file and display them.
        """
        file_name, result_text = result_data

        # Generate a timestamped filename
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        text_file_name = f"{file_name.rsplit('.', 1)[0]}_{timestamp}.txt"

        if self.worker and hasattr(self.worker, 'log'):
            self.worker.log(f"Saving file: {text_file_name}")

        # Save results to a file
        with open(text_file_name, "w") as file:
            file.write(result_text)

        return text_file_name, result_text

    def start_task(self, args=None):
        """
        Start a long-running task in a separate thread.
        """
        try:
            long_running_task = self.process_file
            self.worker = ThreadWorker(
                task_function=long_running_task, args=(args,)
            )

            # Connect log callback if provided
            if self.__log_callback:
                self.worker.log.connect(self.__log_callback)

            self.worker.finished.connect(self.__result_callback)
            self.worker.error.connect(self.task_error)

            self.worker.start()
        except Exception as exc:
            logging.info(f"Error starting task: {exc}")

    def task_error(self, error_message):
        """
        Handle errors during task execution.
        """
        if self.worker and hasattr(self.worker, 'log'):
            self.worker.log.emit(f"Error: {error_message}")
        self.worker = None  # Cleanup the worker
