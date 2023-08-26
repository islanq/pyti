from collections import deque

class PrintManager:
    def __init__(self):
        self.queue = deque()
        self.max_lines = 9
        self.max_chars = 40

    def _split_long_line(self, line):
        # Split long lines into chunks of max_chars length
        return [line[i:i+self.max_chars] for i in range(0, len(line), self.max_chars)]

    def add_to_queue(self, text):
        lines = text.split('\n')
        for line in lines:
            if len(line) > self.max_chars:
                # If line is too long, split it
                self.queue.extend(self._split_long_line(line))
            else:
                self.queue.append(line)

        self._display()

    def _display(self):
        while len(self.queue) >= self.max_lines:
            # Print the first max_lines-1 from the queue
            for _ in range(self.max_lines - 1):
                print(self.queue.popleft())  # Use popleft() to efficiently dequeue from the left
            input("Press any key to continue...")  # Wait for user input

        # Print any remaining lines in the queue
        while self.queue:
            print(self.queue.popleft())