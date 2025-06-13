import contextlib

class Trace:
    def __init__(self):
        self.traces = []

    @contextlib.contextmanager
    def trace(self, message):
        try:
            self.traces.append(message)
            yield
        finally:
            self.traces.pop()

    def get_trace(self, message=None):
        if message is not None:
            return ': '.join(self.traces + [message])
        else:
            return ': '.join(self.traces)
