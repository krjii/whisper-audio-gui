from PySide6.QtCore import Signal, QThread


class ThreadWorker(QThread):
    """
    Worker thread for executing long-running tasks in the background with progress updates.
    """
    finished = Signal(object)        # Emit results when the task is complete
    progress = Signal(int)           # Emit progress updates (0-100)
    error = Signal(str)              # Emit error messages
    log = Signal(str)                # Emit log messages

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
            
            # Pass the `progress` signal as a callback to the task function
            results = self.task_function(*self.args)
            
            self.finished.emit(results)
            self.log.emit("Task completed successfully!")
        except Exception as e:
            self.error.emit(f"Error during task execution: {str(e)}")
