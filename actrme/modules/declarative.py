import copy

from copy import copy
import numpy as np
from numbers import Number
from actrme.basic import SymbolicIO, NumericIO, Direction, boltzmann, TimeKeeper
from actrme.module import Module
from random import choices


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
        """Sets the content of a memory"""
        assert type(contents) == dict
        self._contents = copy(contents)

    def add_trace(self, time):
        """Add a trace to the current memory
        :type time: Number
        """
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
        Module.__init__(self)
        #print(self.inputs)
        self._memories = []
        self._model = None
        self._noise = 0.2
        self._decay_rate = 0.5
        self._threshold = 0
        self._latency_factor = 1.0
        self._encode_on_retrieval = True
        self._encode = SymbolicIO(name="encode", direction = Direction.IN)
        self._cue = SymbolicIO(name="cue", direction = Direction.IN)
        self._retrieval = SymbolicIO(name="retrieval", direction=Direction.OUT)
        self._rt = NumericIO(name="retrieval time", direction=Direction.OUT)
        self._retrieval_probability = NumericIO(name="retrieval probability", direction=Direction.OUT)
        self.add_input(self._encode)
        self.add_input(self._cue)
        self.add_output(self._retrieval)
        self.add_output(self._rt)
        self.add_output(self._retrieval_probability)

    @property
    def noise(self):
        return self._noise

    @noise.setter
    def noise(self, value):
        assert isinstance(value, Number)
        assert value > 0
        self._noise = value

    @property
    def threshold(self):
        return self._threshold

    @threshold.setter
    def threshold(self, value):
        assert isinstance(value, Number)
        self._threshold = value

    @property
    def latency_factor(self):
        return self._latency_factor

    @latency_factor.setter
    def latency_factor(self, value):
        assert isinstance(value, Number)
        self._latency_factor = value

    @property
    def encode_on_retrieval(self):
        return self._encode_on_retrieval

    @encode_on_retrieval.setter
    def encode_on_retrieval(self, value):
        assert isinstance(value, bool)
        self._encode_on_retrieval = value

    def retrieval_probability(self, memory):
        """Computes the probability of a memory at a certain time t"""
        assert isinstance(memory, Memory)
        assert memory in self._memories
        A = memory.activation(self.time)
        T = self.threshold
        s = self.noise
        return 1 / (1 + np.exp((-A + T)/s))

    def retrieval_time(self, memory):
        """Computes the time of a memory at a certain time t"""
        assert isinstance(memory, Memory)
        assert memory in self._memories
        A = memory.activation(self.time)
        T = self.threshold
        F = self.latency_factor
        s = self.noise
        return np.exp(F * (-A + T)/s)

    def reset(self):
        self._memories = []
        self.time = 0

    def encode(self, contents):
        """Adds a trace to an existing memory or encodes a new one"""
        assert isinstance(contents, dict)
        all_contents = [m.contents for m in self._memories]
        if contents in all_contents:
            ii = all_contents.index(contents)
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
            weights = boltzmann([x.activation(self.time) for x in conflict_set], self.noise)
            target = choices(conflict_set, weights=weights, k=1)[0]
            self._retrieval.value = copy(target.contents)
            self._rt.value = self.retrieval_time(target)
            self._retrieval_probability.value = self.retrieval_probability(target)
            return target
        else:
            T = self.threshold
            F = self.latency_factor
            s = self.noise
            self._retrieval.value = {}
            self._rt.value = np.exp(F * (-T) / s)
            return None

    def run(self):
        if self._encode is not None:
            pass
        ## Should always return duration
        return 0.0
