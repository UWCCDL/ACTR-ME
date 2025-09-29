## essential ACT-R modules: Declarative and Procedural memories


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


class Module:
    """A generic module class"""

    def __init__(self, name="GenericModule"):
        self._name = name
        self._model = None

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, newmodel):
        assert isinstance(newmodel, actrme.Model)
        self._model = newmodel

    def run(self):
        # Applies all the functions
        # Returns time
        pass

    def __str__(self):
        return "<%s [module]>" % (self._name)

    # Setters and getters should go here
    # ...
    # And then
