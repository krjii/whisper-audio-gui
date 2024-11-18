
from __future__ import annotations

from PySide6.QtCore import QTimer, Slot, qVersion
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog, 
                               QGridLayout, QGroupBox, QHBoxLayout, QLabel,
                               QProgressBar, QStyleFactory)

from presentation.view.audio_text_controls import AudioTextControls
from presentation.view.player import MediaPlayerWidget

DIR_OPEN_ICON = ":/qt-project.org/styles/commonstyle/images/diropen-128.png"
COMPUTER_ICON = ":/qt-project.org/styles/commonstyle/images/computer-32.png"

def style_names():
    """Return a list of styles, default platform style first"""
    default_style_name = QApplication.style().objectName().lower()
    result = []
    for style in QStyleFactory.keys():
        if style.lower() == default_style_name:
            result.insert(0, style)
        else:
            result.append(style)
    return result

def format_geometry(rect):
    """Format a geometry as a X11 geometry specification"""
    w = rect.width()
    h = rect.height()
    x = rect.x()
    y = rect.y()
    return f"{w}x{h}{x:+d}{y:+d}"

def screen_info(widget):
    """Format information on the screens"""
    policy = QGuiApplication.highDpiScaleFactorRoundingPolicy()
    policy_string = str(policy).split('.')[-1]
    result = f"<p>High DPI scale factor rounding policy: {policy_string}</p><ol>"
    for screen in QGuiApplication.screens():
        current = screen == widget.screen()
        result += "<li>"
        if current:
            result += "<i>"
        name = screen.name()
        geometry = format_geometry(screen.geometry())
        dpi = int(screen.logicalDotsPerInchX())
        dpr = screen.devicePixelRatio()
        result += f'"{name}" {geometry} {dpi}DPI, DPR={dpr}'
        if current:
            result += "</i>"
        result += "</li>"
    result += "</ol>"
    return result


class MediaPlayerMain(QDialog):
    """Dialog displaying a gallery of Qt Widgets"""

    def __init__(self):
        super().__init__()
        
        self.audio_text_controls = AudioTextControls()
        self.media_player = MediaPlayerWidget()

        self._style_combobox = QComboBox()
        self._style_combobox.addItems(style_names())

        style_label = QLabel("Style:")
        style_label.setBuddy(self._style_combobox)

        disable_widgets_checkbox = QCheckBox("Disable widgets")

        simple_media_player_groupbox = self.create_media_player_groupbox()

        self._style_combobox.textActivated.connect(self.change_style)
        disable_widgets_checkbox.toggled.connect(self.audio_text_controls.setDisabled)
        disable_widgets_checkbox.toggled.connect(simple_media_player_groupbox.setDisabled)

        top_layout = QHBoxLayout()
        top_layout.addWidget(style_label)
        top_layout.addWidget(self._style_combobox)
        top_layout.addStretch(1)
        top_layout.addWidget(disable_widgets_checkbox)

        main_layout = QGridLayout(self)
        main_layout.addLayout(top_layout, 0, 0, 1, 2)
        main_layout.addWidget(self.audio_text_controls, 1, 0)
        main_layout.addWidget(simple_media_player_groupbox, 1, 1)

        qv = qVersion()
        self.setWindowTitle(f"Whisper-Ai-Transcriber {qv}")

    def setVisible(self, visible):
        super(MediaPlayerMain, self).setVisible(visible)

    @Slot(str)
    def change_style(self, style_name):
        QApplication.setStyle(QStyleFactory.create(style_name))

    def create_media_player_groupbox(self):
        result = QGroupBox("Media Player")
                
        layout = QGridLayout(result)
        layout.addWidget(self.media_player)
        layout.setRowStretch(5, 1)

        return result
