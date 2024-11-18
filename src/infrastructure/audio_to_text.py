
import whisper
from datetime import datetime
import logging

from infrastructure.thread_worker import ThreadWorker


class AudioText():
    """
    """
    
    def __init__(self, result_callback=None, log_callback=None):
        super().__init__()

        self.__result_callback = result_callback
        self.__progress_callback = None
        self.__log_callback = log_callback

        # Whisper Model
        self.model = whisper.load_model("turbo")

        # Placeholder for the worker
        self.worker = None

    def process_file(self, file_name):
        """
        Process the selected audio file using Whisper.
        """
        #self.update_log("Processing audio...")
        result = self.model.transcribe(audio=file_name, verbose=False)
        return file_name, result['text']

    def save_results(self, result_data):
        """
        Save transcription results to a file and display them.
        """
        file_name, result_text = result_data

        # Generate a timestamped filename
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        text_file_name = f"{file_name.rsplit('.', 1)[0]}_{timestamp}.txt"

        self.worker.log(f"Loading file: {text_file_name}")

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
                task_function=long_running_task, args=(args,))

            # self.worker.progress.connect()
            self.worker.log.connect(self.__log_callback)
            self.worker.finished.connect(self.__result_callback)
            self.worker.error.connect(self.task_error)

            self.worker.start()
        except Exception as exc:
            logging.info(f"{exc}")

    def task_error(self, error_message):
        """
        Handle errors during task execution.
        """
        self.worker.log.emit(f"Error: {error_message}")
        self.worker = None  # Cleanup the worker
