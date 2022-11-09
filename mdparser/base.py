from typing import Iterable

class ParsingException(Exception):
    pass

class IterBuff:

    idx: int
    cur: str
    lookahead: str

    def __init__(self, iterable: Iterable):
        self.it = iter(iterable)
        self.idx = 0
        self.cur: str = None
        self.lookahead: str = next(self.it)
        return
    
    def __next__(self):
        if self.lookahead is None:
            raise StopIteration

        self.idx += 1
        self.cur = self.lookahead
        try:
            self.lookahead = next(self.it)
        except StopIteration:
            self.lookahead = None

        return self.cur
    
    def next(self):
        self.__next__()
        return self
