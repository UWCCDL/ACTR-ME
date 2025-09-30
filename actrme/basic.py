from numbers import Number


class ActrInput():
    """A generic input that is passed to the a model"""

    def __init__(self, name):
        self._name = name
        self._value = None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def __str__(self):
        return "<[I] %s = %s>" % (self._name, self.value)


class ActrOutput():
    def __init__(self, name):
        self._name = name
        self._value = None


class SymbolicInput(ActrInput):
    """A symbolic input. A symbol is a collection of slot-value pairs"""

    def __init__(self, name):
        super().__init__(name)
        self._value = {}

    @property
    def value(self):
        return super().value

    @value.setter
    def value(self, newvalue):
        assert isinstance(newvalue, dict), "Value is not dictionary"
        if not isinstance(newvalue, dict):
            return
        super(SymbolicInput, self.__class__).value.fset(self, newvalue)

    def modify(self, newvalue):
        """Adds new slot-values to symbol"""
        assert isinstance(newvalue, dict), "Value is not dictionary"
        if not isinstance(newvalue, dict):
            return
        for key, value in newvalue.items():
            self.value[key] = value


class NumericInput(ActrInput):
    def __init__(self, name):
        super().__init__(name)
        self._value = {}


class SymbolicOutput(ActrOutput):
    pass


class NumericOutput(ActrOutput):
    pass


class ProbabilityOutput(ActrOutput):
    pass


class TimeKeeper():
    """A generic objects that keeps track of time internally"""
    def  __init__(self, time = 0.0):
        assert isinstance(time, Number)
        assert time >= 0
        self._time = time

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        assert isinstance(value, Number)
        self._time = value

class InputOutput():
    """A generic objects that has inputs and outputs"""
    def __init__(self, inputs = [], outputs = []):
        self._inputs = inputs
        self._outputs = outputs

    @property
    def inputs(self):
        return self._inputs

    def add_input(self, input):
        assert isinstance(input, ActrInput)
        if input not in self.inputs:
            self._inputs.append(input)

    @property
    def outputs(self):
        return self._outputs

    def add_output(self, output):
        assert isinstance(output, ActrOutput)
        if output not in self._outputs:
            self._outputs.append(output)

