## essential ACT-R modules: Declarative and Procedural memories

import pyactup as pya


class ActrInput():
    """A generic input that is passed to the a model"""
    def __init__(self, name):
        self._name = name
        self._value = None

class ActrOutput():
    def __init__(self, name):
        self._name = name
        self._value = None 

class SymbolicInput(ActrInput):
    pass

class NumericInput(ActrInput):
    pass

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


class DeclarativeMemory(Module):
    """A wrapper for PyACTUp"""
    def __init__(self):
        super().__init__(name="Declarative Memory", version="0.1")
        self._memory = pya.Memory()

        # Inputs
        self._encode = SymbolicInput("encode")
        self._cue = SymbolicInput("cue")

        # Outputs
        self._retrieval = SymbolicOutput("retrieval")
        self._rt = NumericOutput("rt")

        # Config parameter
        self._rencode_on_retrieval = True

    def inputs(self):
        return [self._encode, self._cue]

    def run(self):
        pass


def ProceduralMemory(Module):
    """A simple rule-based system"""
    def __init__(self):
        self.name = "Procedural" 
    
    def learn(rule):
        pass

    def response(condition):
        pass
