# Copyright 2024 Independent Hustles
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions, and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions, and the following disclaimer in the documentation and/or other materials provided with the distribution.
# 3. Neither the name of Your Name or Organization nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import sys
from PySide6.QtCore import QStandardPaths, Qt, Slot
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QApplication, QDialog, QFileDialog, QVBoxLayout, QStyleFactory,
                               QHBoxLayout, QPushButton, QSlider, QWidget, QLabel, QStyle)
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer, QMediaFormat
from PySide6.QtMultimediaWidgets import QVideoWidget


def get_supported_mime_types():
    result = []
    
    for file_format in QMediaFormat().supportedFileFormats(QMediaFormat.ConversionMode.Decode):
        mime_type = QMediaFormat(file_format).mimeType()
        result.append(mime_type.name())
    
    result.append("audio/mpeg")
    
    return result


class MediaPlayerWidget(QWidget):

    def __init__(self):
        super().__init__()

        self._playlist = []
        self._playlist_index = -1
        self._audio_output = QAudioOutput()
        self._player = QMediaPlayer()
        self._player.setAudioOutput(self._audio_output)

        # Get the current style for standard icons
        style = QStyleFactory.create(QApplication.style().objectName())

        # Layout for the widget
        main_layout = QVBoxLayout(self)

        # Video display widget
        self._video_widget = QVideoWidget()
        main_layout.addWidget(self._video_widget)
        self._player.setVideoOutput(self._video_widget)

        # Track title label
        self._track_title_label = QLabel("No track loaded")
        main_layout.addWidget(self._track_title_label)

        # Playback position label
        self._playback_position_label = QLabel("00:00 / 00:00")
        main_layout.addWidget(self._playback_position_label)

        # Position slider (visual bar)
        self._position_slider = QSlider(Qt.Orientation.Horizontal)
        self._position_slider.setRange(0, 0)  
        self._position_slider.sliderMoved.connect(self._set_position)
        main_layout.addWidget(self._position_slider)

        # Controls layout
        controls_layout = QHBoxLayout()

        # Open button
        open_button = QPushButton("Open")
        open_button.setIcon(QIcon.fromTheme(
            "document-open",
            style.standardIcon(QStyle.StandardPixmap.SP_DirOpenIcon)
        ))
        open_button.clicked.connect(self.open)
        controls_layout.addWidget(open_button)

        # Previous button
        previous_button = QPushButton("Previous")
        previous_button.setIcon(QIcon.fromTheme(
            "media-skip-backward",
            style.standardIcon(QStyle.StandardPixmap.SP_MediaSkipBackward)
        ))
        
        previous_button.clicked.connect(self.previous_clicked)
        controls_layout.addWidget(previous_button)

        # Play button
        self._play_button = QPushButton("Play")
        self._play_button.setIcon(QIcon.fromTheme(
            "media-playback-start",
            style.standardIcon(QStyle.StandardPixmap.SP_MediaPlay)
        ))
        self._play_button.clicked.connect(self._player.play)
        controls_layout.addWidget(self._play_button)

        # Pause button
        self._pause_button = QPushButton("Pause")
        self._pause_button.setIcon(QIcon.fromTheme(
            "media-playback-pause",
            style.standardIcon(QStyle.StandardPixmap.SP_MediaPause)
        ))
        self._pause_button.clicked.connect(self._player.pause)
        controls_layout.addWidget(self._pause_button)

        # Stop button
        stop_button = QPushButton("Stop")
        stop_button.setIcon(QIcon.fromTheme(
            "media-playback-stop",
            style.standardIcon(QStyle.StandardPixmap.SP_MediaStop)
        ))
        stop_button.clicked.connect(self._ensure_stopped)
        controls_layout.addWidget(stop_button)

        # Next button
        next_button = QPushButton("Next")
        next_button.setIcon(QIcon.fromTheme(
            "media-skip-forward",
            style.standardIcon(QStyle.StandardPixmap.SP_MediaSkipForward)
        ))
        next_button.clicked.connect(self.next_clicked)
        controls_layout.addWidget(next_button)

        # Volume slider
        self._volume_slider = QSlider(Qt.Orientation.Horizontal)
        self._volume_slider.setMinimum(0)
        self._volume_slider.setMaximum(100)
        self._volume_slider.setValue(50)
        self._volume_slider.valueChanged.connect(self._audio_output.setVolume)
        controls_layout.addWidget(QLabel("Volume"))
        controls_layout.addWidget(self._volume_slider)

        main_layout.addLayout(controls_layout)

        self._mime_types = get_supported_mime_types()

        self.update_buttons(self._player.playbackState())
        self._player.playbackStateChanged.connect(self.update_buttons)

        # Connect position and duration signals
        self._player.positionChanged.connect(self._update_position)
        self._player.durationChanged.connect(self._update_duration)

    @Slot()
    def _update_position(self, position):
        # Update position label and slider
        duration = self._player.duration()
        if duration > 0:
            self._position_slider.setValue(position)
            position_formatted = f"{position // 60000:02}:{(position // 1000) % 60:02}"
            duration_formatted = f"{duration // 60000:02}:{(duration // 1000) % 60:02}"
            self._playback_position_label.setText(f"{position_formatted} / {duration_formatted}")

    @Slot()
    def _update_duration(self, duration):
        # Update slider range when the duration changes
        self._position_slider.setRange(0, duration)

    @Slot(int)
    def _set_position(self, position):
        # Set player position when slider is moved
        self._player.setPosition(position)

    @Slot()
    def open(self):
        self._ensure_stopped()
        file_dialog = QFileDialog(self)
        file_dialog.setMimeTypeFilters(self._mime_types)

        movies_location = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.MoviesLocation)
        file_dialog.setDirectory(movies_location)

        if file_dialog.exec() == QDialog.DialogCode.Accepted:
            url = file_dialog.selectedUrls()[0]
            self._playlist.append(url)
            self._playlist_index = len(self._playlist) - 1
            self._player.setSource(url)
            self._track_title_label.setText(f"Now Playing: {url.fileName()}")
            self._player.play()

    @Slot()
    def _ensure_stopped(self):
        if self._player.playbackState() != QMediaPlayer.PlaybackState.StoppedState:
            self._player.stop()

    @Slot()
    def previous_clicked(self):
        if self._player.position() <= 5000 and self._playlist_index > 0:
            self._playlist_index -= 1
            self._player.setSource(self._playlist[self._playlist_index])
        else:
            self._player.setPosition(0)

    @Slot()
    def next_clicked(self):
        if self._playlist_index < len(self._playlist) - 1:
            self._playlist_index += 1
            self._player.setSource(self._playlist[self._playlist_index])

    @Slot("QMediaPlayer::PlaybackState")
    def update_buttons(self, state):
        has_media = len(self._playlist) > 0
        self._play_button.setEnabled(has_media and state != QMediaPlayer.PlaybackState.PlayingState)
        self._pause_button.setEnabled(state == QMediaPlayer.PlaybackState.PlayingState)

    @Slot("QMediaPlayer::Error", str)
    def _player_error(self, error, error_string):
        print(f"Error: {error_string}", file=sys.stderr)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = MediaPlayerWidget()
    player.resize(800, 600)
    player.show()
    sys.exit(app.exec())
