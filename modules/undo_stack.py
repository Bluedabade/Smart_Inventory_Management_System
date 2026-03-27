from datetime import datetime


class UndoStack:
    def __init__(self):
        self.stack = []

    def push(self, action):
        if "timestamp" not in action:
            action["timestamp"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.stack.append(action)

    def pop(self):
        if self.is_empty():
            return None
        return self.stack.pop()

    def peek(self):
        if self.is_empty():
            return None
        return self.stack[-1]

    def is_empty(self):
        return len(self.stack) == 0

    def get_all(self):
        return self.stack.copy()

    def size(self):
        return len(self.stack)