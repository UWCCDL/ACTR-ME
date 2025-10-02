from numbers import Number

class Representation:
    """A generic symbol class. This is still experimental and not used"""
    def __init__(self, content):
        assert isinstance(content, dict)
        self._content = content

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        assert isinstance(value, dict)
        self._content = value

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


class ActrInput:
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
        return "[(>> In) %s = %s]" % (self._name, self.value)


class ActrOutput:
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

    def __str__(self):
        return "[(>> Sym) %s = %s]" % (self._name, self.value)


class NumericInput(ActrInput):
    def __init__(self, name):
        super().__init__(name)
        self._value = 0

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        assert isinstance(value, Number), "Value is not a number"
        self._value = value

    def __str__(self):
        return "[(>> Num) %s = %s]" % (self._name, self.value)


class SymbolicOutput(ActrOutput):
    pass


class NumericOutput(ActrOutput):
    pass


class ProbabilityOutput(NumericOutput):
    pass


class TimeKeeper:
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

class InputOutput:
    """A generic object that has inputs and outputs"""
    def __init__(self, inputs = [], outputs = []):
        self._inputs = inputs
        self._outputs = outputs

    @property
    def inputs(self):
        return self._inputs

    def add_input(self, inpt):
        assert isinstance(inpt, ActrInput), "Input is not an ActrInput: type(ActrInput)=%s" % type(input)
        if inpt not in self._inputs:
            self._inputs.append(inpt)

    @property
    def outputs(self):
        return self._outputs

    def add_output(self, output):
        assert isinstance(output, ActrOutput)
        if output not in self._outputs:
            self._outputs.append(output)

