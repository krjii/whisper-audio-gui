
from PySide6.QtWidgets import QGroupBox, QPushButton, QVBoxLayout,\
    QWidget, QHBoxLayout, QPlainTextEdit, QFileDialog, QProgressBar
    
from PySide6.QtCore import Slot
    
from infrastructure.audio_to_text import AudioText

class AudioTextControls(QWidget):
    """
    classdocs
    """


    def __init__(self):
        super().__init__()
        
        self.audio_to_text = AudioText(result_callback=self.display_results, 
                                       log_callback=self.update_log)

        self.buttons_groupbox = self.create_buttons_groupbox()
        
        self._progress_bar = self.create_progress_bar()
        
        # Main layout for the widget
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.buttons_groupbox)
        self.layout.addWidget(self._progress_bar)
        
        self.setLayout(self.layout)
        
    def class_name(self, o):
        return o.metaObject().className()
        
    def create_buttons_groupbox(self):
        result = QGroupBox("Buttons")

        self.transcribe_audio_pushbutton = QPushButton("Transcribe Audio")
        self.transcribe_audio_pushbutton.clicked.connect(self.load_file)
        self.transcribe_audio_pushbutton.setDefault(True)

        self.plain_textedit = QPlainTextEdit("")
        self.plain_textedit.setReadOnly(True)

        tool_layout = QHBoxLayout()
        tool_layout.addWidget(self.plain_textedit)

        button_layout = QVBoxLayout()
        button_layout.addWidget(self.transcribe_audio_pushbutton)
        button_layout.addLayout(tool_layout)
        button_layout.addStretch(1)
        
        
        main_layout = QHBoxLayout(result)
        main_layout.addLayout(button_layout)
        main_layout.addStretch()
        
        return result
        
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
            self.audio_to_text.start_task(file_name)
    
    def update_log(self, message):
        """
        Append a message to the QTextEdit.
        """
        self.plain_textedit.appendPlainText(message)

    @Slot()
    def update_progress_bar(self, value):
        """
        Update the progress bar with the given value.
        """
        cur_val = self._progress_bar.value()
        max_val = self._progress_bar.maximum()

        self._progress_bar.setValue(cur_val + (max_val - cur_val) / 100)
        
    def display_results(self, result_text):
        """
        """
        
        text_file_name = result_text[0]
        result_output = result_text[1]    
        
        self.update_log(f"Results saved to {text_file_name} \n")
     
        self.update_log(f"Transcribed Audio \n {result_output}")
        
    def create_progress_bar(self):
        """
        """

        result = QProgressBar()
        result.setRange(0, 10000)
        result.setValue(0)

        return result
