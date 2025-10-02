from actrme.module import Module
from actrme.basic import TimeKeeper, InputOutput, NumericInput, NumericOutput
from numbers import Number
import pandas as pd


class Model(TimeKeeper, InputOutput):
    """A model is a collection of interaction modules that responds to inputs"""
    def __init__(self):
        TimeKeeper.__init__(self)
        InputOutput.__init__(self)
        self._modules = []
        self._time_input = NumericInput("time")
        self._time_output = NumericOutput("rt")
        self.add_input(self._time_input)
        self.add_output(self._time_output)

    @property
    def modules(self):
        return self._modules

    def add_module(self, mod):
        """Adds a module"""
        assert isinstance(mod, Module)
        self._modules.append(mod)

        for input in mod.inputs:
            self.inputs.add(input)

        for output in mod.outputs:
            self.outputs.add(output)


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
        #for i in self.dataframe:
        pass


def model():
    """Creates a model based on the specific modules"""
    return Model()


