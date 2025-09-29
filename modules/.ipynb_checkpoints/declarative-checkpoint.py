from module import *

class Memory:
    """An internal representation of a memory (or "chunk" in ACT-R lingo)"""
    def __init__(self, contents={}, d=0.5):
        self._contents = contents
        self._traces = []
        self.d = 0.5
        
    @property
    def contents(self):
        return self._contents

    @contents.setter
    def set_contents():
        pass

    def add_trace(time):
        pass


class DeclarativeMemory(Module):
    """A wrapper for PyACTUp"""
    def __init__(self):
        self._encode = SymbolicInput("encode")
        self._cue = SymbolicInput("cue")
        self._retrieval = SymbolicOutput("retrieval")
        self._rt = NumericOutput("rt")

    def inputs(self):
        return [self._encode, self._cue]

    def encode(self, contents):
        """Adds a trace to an existing memory or encodes a new one"""
        pass

    def retrieve(self, cue):
        """Retrieves the best matching memory"""
        self.retrieval.set_contents()

    def run(self):
        if self._encode is not None:
            pass