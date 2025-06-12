class SubprocessWorker(QThread):
    output_line = pyqtSignal(str)
    error_line  = pyqtSignal(str)
    finished    = pyqtSignal(int)

    def __init__(self, command):
        super().__init__()
        self.command = command

    def run(self):
        process = subprocess.Popen(
            self.command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )

        def read_stream(stream, signal):
            for line in stream:
                signal.emit(line)
            stream.close()

        stdout_thread = threading.Thread(target=read_stream, args=(process.stdout, self.output_line))
        stderr_thread = threading.Thread(target=read_stream, args=(process.stderr, self.error_line))

        stdout_thread.start()
        stderr_thread.start()

        stdout_thread.join()
        stderr_thread.join()

        exit_code = process.wait()
        self.finished.emit(exit_code)
