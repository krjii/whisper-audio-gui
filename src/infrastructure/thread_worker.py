
from PySide6.QtCore import Signal, QThread


class ThreadWorker(QThread):
    """
    Worker thread for executing long-running tasks in the background with progress updates.
    """
    finished = Signal(object)
    progress = Signal(int)           
    error = Signal(str)              
    log = Signal(str)                

    def __init__(self, task_function, args=None, parent=None):
        super().__init__(parent)
        self.task_function = task_function
        self.args = args or ()

    def run(self):
        """
        Execute the assigned task function in a separate thread.
        """
        try:
            self.log.emit("Task started...")
            
            results = self.task_function(*self.args)
            
            self.finished.emit(results)
            self.log.emit("Task completed successfully!")
        except Exception as e:
            self.error.emit(f"Error during task execution: {str(e)}")
