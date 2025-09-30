from modules.module import Module, NumericInput, NumericOutput, ActrInput
from numbers import Number
import pandas as pd

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

    @property
    def outputs(self):
        return self._outputs

class Model(TimeKeeper, InputOutput):
    """A model is a collection of interaction modules that responds to inputs"""
    def __init__(self):
        TimeKeeper.__init__(self)
        InputOutput.__init__(self)
        self._modules = []
        self._time_input = NumericInput("time")
        self._time_output = NumericOutput("rt")

    @property
    def modules(self):
        return self._modules

    def add_module(self, module):
        """Adds a module"""
        assert isinstance(module, Module)
        self._modules.append(module)

        for input in module.inputs:
            self.inputs.add(input)

        for output in module.outputs:
            self.outputs.add(input)


    def run(self):
        # First, update all the inputs, especially time.
        pass

class DataModel(Model):
    """A specific type of model whose inputs are columns in a Pandas DataFrame"""
    def __init__(self, dataframe=None):
        Model.__init__(self)
        assert isinstance(dataframe, pd.DataFrame)
        self._dataframe = dataframe

    def use_mle(self):
        """A module can use MLE iff all of its mapped outputs have probabilities"""
        pass

    def run(self):
        for i in self.dataframe:
            pass


def model():
    """Creates a model based on the specific modules"""
    return Model()


