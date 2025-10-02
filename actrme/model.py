from actrme.module import Module
import actrme.basic as basic #import TimeKeeper, InputOutput, NumericIO, Direction
import pandas as pd


class Model(basic.TimeKeeper, basic.InputOutput):
    """A model is a collection of interaction modules that responds to inputs"""
    def __init__(self):
        basic.TimeKeeper.__init__(self)
        basic.InputOutput.__init__(self)
        self._modules = []
        self._time_input = basic.NumericIO("time", direction=basic.Direction.IN)
        self._time_output = basic.NumericIO("rt", direction=basic.Direction.OUT)
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
            self.inputs.append(input)

        for output in mod.outputs:
            self.outputs.append(output)


    def run(self):
        # First, update all the inputs, especially time.
        pass

class DataModel(Model):
    """A specific type of model whose inputs are columns in a Pandas DataFrame"""
    def __init__(self, dataframe=None):
        Model.__init__(self)
        assert isinstance(dataframe, pd.DataFrame)
        self._dataframe = dataframe

    def connect(self, column, input):
        """Connects a dataframe column to an input"""
        assert isinstance(column, str)
        assert isinstance(input, basic.ActrIO)
        pass

    def use_mle(self):
        """A module can use MLE iff all of its mapped outputs have probabilities"""
        pass

    def run(self):
        #for i in self.dataframe:
        pass