## essential ACT-R modules: Declarative and Procedural memories

import pyactup as pya

class ActrInput():
    """A generic input that is passed to the a model"""
    def __init__(self, name):
        self._name = name
        self._value = None
    
    @property
    def value(self):
        return self._value

    @value.setter
    def set_value(self, value):
        self._value = value

class ActrOutput():
    def __init__(self, name):
        self._name = name
        self._value = None 


class SymbolicInput(ActrInput):
    """A symbolic input. A symbol is a collection of slot-value pairs"""
    def __init__(self, name):
        super().__init__(name)
        self.value = {}

    @property
    def value(self):
        super().value

    @value.setter
    def set_value(self, newvalue):
        if isinstance(newvalue, dict):
            super().value = newvalue

    def modify(self, newvalue):
        """Adds new slot-values to symbol"""
        pass
        

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

    def __init__(self, name="GenericModule", version = "0.0"):
        self._name = name
        self._version = version

    def run(self):
        # Applies all the functions
        pass

    def __str__(self):
        return "<%s [module]>" % (self._name)
        

    # Setters and getters should go here
    # ...
    # And then
