import os
import sys


class ProgressBar(object):
    def __init__(self, name, total):
        self.name = name
        self.total = total
        self.count = 0
        _, cols = os.popen('stty size', 'r').read().split()
        self.char_total = int(cols) - len(name) - 15
        self.show_total = 0
        self.end = False

    @property
    def get_bar(self):
        ratio = self.count / self.total
        chars_to_show = int(ratio * self.char_total)
        if chars_to_show > self.show_total:
            self.show_total = chars_to_show
        b = "{scale:<{count}}".format(scale="#" * self.show_total, count=self.char_total)
        percent = '{:.0%}'.format(ratio)
        if self.count < self.total:
            bar = f"{self.name} {b} {percent}\r"
        else:
            bar = f"{self.name} {b} {percent}\n"
            self.end = True
        return bar

    def update(self, incr=1):
        if not self.end:
            self.count += incr
            if self.count >= self.total:
                self.count = self.total
            self.flush()

    def flush(self):
        sys.stdout.write(self.get_bar)
        sys.stdout.flush()
