from infrastructure.thread_worker import ThreadWorker

from PySide6.QtWidgets import QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget, QFileDialog, QProgressBar

import whisper
from datetime import datetime


class MainWindow(QMainWindow):
    """
    Main window for Audio to Text Transcriber application.
    """

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Audio to Text Transcriber")

        # UI Elements
        self.text_edit = QTextEdit()
        self.load_button = QPushButton("Load File")
        self.progress_bar = QProgressBar()

        self.load_button.clicked.connect(self.load_file)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.load_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Whisper Model
        self.model = whisper.load_model("turbo")

        # Placeholder for the worker
        self.worker = None

    def load_file(self):
        """
        Open a file dialog and start processing the selected file.
        """
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Open Audio File",
            "",
            "Audio Files (*.mp3 *.mp4 *.wav *.flac *.ogg);;All Files (*)"
        )

        if file_name:
            self.update_log("Loading file...")
            self.start_task(self.process_file, file_name)

    def process_file(self, file_name):
        """
        Process the selected audio file using Whisper.
        """
        self.update_log("Processing audio...")
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

        # Save results to a file
        with open(text_file_name, "w") as file:
            file.write(result_text)

        self.update_log(f"Results saved to {text_file_name}")
        self.text_edit.setPlainText(result_text)

    def start_task(self, long_running_task, args=None):
        """
        Start a long-running task in a separate thread.
        """
        self.update_log("Starting task...")
        self.progress_bar.setValue(0)

        self.worker = ThreadWorker(task_function=long_running_task, args=(args,))
        
        # Connect signals to handle updates and results
        self.worker.progress.connect(self.update_progress_bar)
        self.worker.finished.connect(self.save_results)
        self.worker.error.connect(self.task_error)
        self.worker.log.connect(self.update_log)

        self.worker.start()

    def update_log(self, message):
        """
        Append a message to the QTextEdit.
        """
        self.text_edit.append(message)

    def update_progress_bar(self, value):
        """
        Update the progress bar with the given value.
        """
        self.progress_bar.setValue(value)

    def task_error(self, error_message):
        """
        Handle errors during task execution.
        """
        self.update_log(f"Error: {error_message}")
        self.worker = None  # Cleanup the worker
   
