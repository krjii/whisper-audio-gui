
from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication
from presentation.view.media_player_main import MediaPlayerMain


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    window = MediaPlayerMain()
    window.show()
    
    sys.exit(app.exec())
