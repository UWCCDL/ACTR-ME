import copy

from modules.module import *
from copy import copy
import numpy as np
from numbers import Number
from actrme import TimeKeeper


class Memory:
    """An internal representation of a memory (or "chunk" in ACT-R lingo)"""

    def __init__(self, creation_time=0.0, contents={}, decay_rate=0.5):
        assert isinstance(contents, dict)
        self._contents = copy(contents)
        self._traces = [creation_time]
        self._decay_rate = decay_rate

    @property
    def decay_rate(self):
        return self._decay_rate

    @decay_rate.setter
    def decay_rate(self, value):
        self._decay_rate = value

    @property
    def contents(self):
        return self._contents

    @contents.setter
    def contents(self, contents):
        assert type(contents) == dict
        self._contents = copy(contents)

    def add_trace(self, time):
        assert isinstance(time, Number)
        self._traces.append(time)

    def remove_trace(self, time):
        """Removes a trace from the memory"""
        assert isinstance(time, Number)
        assert time in self._traces
        self._traces.remove(time)

    def activation(self, time):
        """Computes the activation of a memory at a certain time t"""
        assert isinstance(time, Number)
        odds = 0.0
        for t_i in self._traces:
            if t_i < time:
                odds += (time - t_i) ** (-self.decay_rate)
        if odds > 0:
            return np.log(odds)
        else:
            return np.nan

    def __repr__(self):
        return "<Memory [%d] %s>" % (len(self._traces), self._contents)


class DeclarativeMemory(Module, TimeKeeper):
    """A simple declarative memory module"""

    def __init__(self):
        TimeKeeper.__init__(self)
        self._memories = []
        self._model = None
        self._noise = 0.2
        self._decay_rate = 0.5
        self._encode = SymbolicInput("encode")
        self._cue = SymbolicInput("cue")
        self._retrieval = SymbolicOutput("retrieval")
        self._rt = NumericOutput("rt")

    def reset(self):
        self._memories = []

    def inputs(self):
        return [self._encode, self._cue]

    def encode(self, contents):
        """Adds a trace to an existing memory or encodes a new one"""
        assert isinstance(contents, dict)
        all = [m.contents for m in self._memories]
        if contents in all:
            ii = all.index(contents)
            self._memories[ii].add_trace(time=self.time)
        else:
            m = Memory(creation_time=self.time,
                       contents=contents)
            self._memories.append(m)


    def retrieve(self, cue):
        """Retrieves the best matching memory"""
        assert isinstance(cue, dict)
        conflict_set = []
        for m in self._memories:
            if cue.items() <= m.contents.items():
                conflict_set.append(m)
        if len(conflict_set) > 0:
            return conflict_set[0]
        return None

    def run(self):
        if self._encode is not None:
            pass
