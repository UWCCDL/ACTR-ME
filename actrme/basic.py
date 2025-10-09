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
        self._owner = None

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

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, newowner):
        assert isinstance(newowner, Module) or isinstance(newowner, Model)
        self._owner = newowner

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
        assert isinstance(inpt, ActrIO), "Input is not an ActrIO: type = %s" % type(inpt)
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


class Connection:
    """A connection between two entitiers"""
    def __init__(self, source, destination):
        self._source = source
        self._destination = destination

    @property
    def source(self):
        return self._source

    @property
    def destination(self):
        return self._destination

class ModuleConnection(Connection):
    """A connection between two modules"""
    def __init__(self, source, destination, extract=None):
        assert isinstance(source, ActrIO)
        assert source.direction == Direction.OUT
        assert isinstance(destination, ActrIO)
        assert destination.direction == Direction.IN
        Connection.__init__(self, source, destination)
        self._extract = extract

    def propagate(self, module):
        pass

class Module(InputOutput):
    """A generic module class"""

    def __init__(self, name="GenericModule"):
        InputOutput.__init__(self)
        self._name = name
        self._model = None
        self._duration = 0.0
        self._duration_probability = 1.0
        self._probability = 1.0

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, newmodel):
        assert isinstance(newmodel, Model)
        self._model = newmodel

    @property
    def duration(self):
        """Returns the duration of a run"""
        return self._duration

    @duration.setter
    def duration(self, newduration):
        """Sets the duration of the module"""
        assert isinstance(newduration, Number)
        assert newduration >= 0.0
        self._duration = newduration

    @property
    def duration_probability(self):
        """Returns the probability of the duration of the module"""
        return self._duration_probability

    @duration_probability.setter
    def duration_probability(self, probability):
        """Sets the probability of the duration of the module"""
        assert isinstance(probability, Number)
        assert probability >= 0.0
        self._duration_probability = probability

    @property
    def probability(self):
        """Returns the probability of the module"""
        return self._probability

    @probability.setter
    def probability(self, probability):
        """Returns the probability of the module"""
        assert isinstance(probability, Number)
        assert probability >= 0.0
        self._probability = probability

    def run(self):
        # Applies all the functions
        # Returns time
        pass

    def __str__(self):
        return "<%s [module]>" % (self._name)

class Model(TimeKeeper, InputOutput):
    """A model is a collection of interaction modules that responds to inputs"""
    def __init__(self):
        TimeKeeper.__init__(self)
        InputOutput.__init__(self)
        self._modules = []
        self._time_input = NumericIO("time",
                                                  direction=Direction.IN)
        self._time_output = NumericIO("rt",
                                                   direction=Direction.OUT)
        self.add_input(self._time_input)
        self.add_output(self._time_output)

    @property
    def modules(self):
        return self._modules

    def add_module(self, mod):
        """Adds a module"""
        assert isinstance(mod, Module)
        self._modules.append(mod)

    def remove_module(self, mod):
        """Removes a module"""
        assert isinstance(mod, Module)
        assert mod in self._modules
        # Remove any inputs connected to that module
        mod_inputs = [x for x in self.inputs if x.module == mod]
        if len(mod_inputs) > 0:
            for input in mod_inputs:
                self.inputs.remove(input)
        # Remove the module itself
        self._modules.remove(mod)

    def add_input(self, input):
        """Adds an input module"""
        assert isinstance(input, ActrIO)
        assert input.direction == Direction.IN
        assert input.module in self._modules
        self._inputs.append(input)

    def run(self):
        """Generic run function"""
        # This should be a simple generic function that runs through all the
        # non-empty input modules and propagates them until the model is stable.
        # (e.g., no more cognitive cycles).
        modules_to_update = list(set([x.module for x in self.inputs]))
        for module in modules_to_update:
            pass



class DataInputMapping:
    """An input mapping a mapping from a column of a dataframe to a module input"""
    def __init__(self, source, destination, rename):
        self._source = source
        self._destination = destination
        self._rename = rename

    @property
    def source(self):
        return self._source
    @property
    def destination(self):
        return self._destination
    @property
    def rename(self):
        return self._rename

    def __str__(self):
        name = '' if self._name == None else '%s' % self._name
        return "<Value %s From '%s' To '%s'>" % (name, self._source.name, self._destination)

    def __repr__(self):
        return self.__str__()

class DataOutputMapping:
    """An output mapping from  module output to column of a dataframe"""

    def __init__(self, source, destination, extract=None, rename=None):
        self._source = source
        self._destination = destination
        self._extract = extract

    @property
    def source(self):
        return self._source
    @property
    def destination(self):
        return self._destination

    @property
    def extract(self):
        return self._extract

    def __str__(self):
        val = '' if self._extract == None else '%s' % self.extract
        return "<Value %s From %s To '%s'>" % (val, self._source.name, self._destination)

    def __repr__(self):
        return self.__str__()