from numbers import Number
import numpy as np
from enum import Enum

def boltzmann(values, temperature):
    """Returns a Boltzmann distribution of the probabilities of each option"""
    assert temperature > 0
    vals = np.array(values)/temperature
    bvals = np.exp(vals - np.max(vals)) / np.exp(vals - np.max(vals)).sum()
    return bvals


class Representation(dict):
    """A generic symbol class. This is still experimental and not used"""
    # Add comparisons for efficiency
    def __repr__(self):
        return self._content

    def __eq__(self, representation):
        if isinstance(representation, Representation):
            return self._content == representation.content
        else:
            return False

    def __ne__(self, representation):
        if isinstance(representation, Representation):
            return self._content != representation.content
        else:
            return True

class Direction(Enum):
    """Numeric constants for the direction of information flow"""
    IN = 1
    OUT = 2

class ActrIO:
    """A generic input that is passed to the model"""

    def __init__(self, name, direction=Direction.IN):
        self._name = name
        self._value = None
        self._direction = direction

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, direction):
        assert direction in Direction
        self._direction = direction

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newname):
        assert isinstance(newname, str)
        self._name = newname

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def __str__(self):
        return "[(>> In) %s = %s]" % (self._name, self.value)


class SymbolicIO(ActrIO):
    """A symbolic input. A symbol is a collection of slot-value pairs"""

    def __init__(self, name, direction=Direction.IN):
        super().__init__(name, direction)
        self._value = {}

    @property
    def value(self):
        return super().value

    @value.setter
    def value(self, newvalue):
        assert isinstance(newvalue, dict), "Value is not dictionary"
        if not isinstance(newvalue, dict):
            return
        super(SymbolicIO, self.__class__).value.fset(self, newvalue)

    def modify(self, newvalue):
        """Adds new slot-values to symbol"""
        assert isinstance(newvalue, dict), "Value is not dictionary"
        if not isinstance(newvalue, dict):
            return
        for key, value in newvalue.items():
            self.value[key] = value

    def __str__(self):
        desc = "(..Sym)"
        if self.direction == Direction.OUT:
            desc = "(Sym..)"
        return "<%s '%s'=%s>" % (desc, self._name, self.value)

    def __repr__(self):
        return self.__str__()


class NumericIO(ActrIO):
    def __init__(self, name, direction=Direction.IN):
        super().__init__(name, direction)
        self._value = 0

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        assert isinstance(value, Number), "Value is not a number"
        self._value = value

    def __str__(self):
        desc = "(..Num)"
        if self.direction == Direction.OUT:
            desc = "(Num..)"
        return "<%s '%s'=%s>" % (desc, self._name, self.value)

    def __repr__(self):
        return self.__str__()


class ProbabilityIO(NumericIO):
    """
This is just a numeric IO that forces values in [0,1]. Might not use because
probability densities might in fact exceed 1"""
    pass

class Pipe:
    """A pipe is a connection between an ActrIO and a different objects"""
    def __init__(self, source, destination):
        assert isinstance(source, ActrIO)
        assert isinstance(destination, ActrIO)
        self.source = source
        self.destination = destination

    def flow(self):
        """Sends the source information to the destination"""
        pass

class TimeKeeper:
    """A generic objects that keeps track of time internally"""
    def  __init__(self, time = 0.0):
        assert isinstance(time, Number)
        assert time >= 0
        self._time = time
        self._time_scale = 1.0 # The inner meaning of time (in seconds)

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        assert isinstance(value, Number)
        self._time = value

    @property
    def time_scale(self):
        return self._time_scale

    @time_scale.setter
    def time_scale(self, value):
        assert isinstance(value, Number)
        assert value >= 0
        self._time_scale = value

class InputOutput:
    """A generic object that has inputs and outputs"""
    def __init__(self):
        self._inputs = []
        self._outputs = []

    @property
    def inputs(self):
        return self._inputs

    def add_input(self, inpt):
        print(inpt)
        assert isinstance(inpt, ActrIO), "Input is not an ActrInput: type(ActrIO)=%s" % type(input)
        assert inpt not in self.inputs, "Input is already defined: %s" % inpt
        assert inpt.name not in [x.name for x in self.inputs], "Name already exists in inputs: " % inpt.name
        assert inpt.direction == Direction.IN, "Input Direction must be IN: " % inpt
        self.inputs.append(inpt)

    def get_input(self, name):
        assert isinstance(name, str)
        for inpt in self._inputs:
            if inpt.name == name:
                return inpt
        return None

    @property
    def outputs(self):
        return self._outputs

    def add_output(self, output):
        assert isinstance(output, ActrIO), "Input is not an ActrInput: type(ActrIO)=%s" % type(input)
        assert output not in self.outputs, "Output is already defined"
        assert output.name not in [x.name for x in self.outputs], "Name already exists in outputs"
        assert output.direction == Direction.OUT, "Direction must be OUT"
        self.outputs.append(output)

    def get_output(self, name):
        assert isinstance(name, str)
        for output in self.outputs:
            if output.name == name:
                return output
        return None

