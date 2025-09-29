from modules.module import Module, NumericInput, NumericOutput, ActrInput
from numbers import Number

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


class Model(TimeKeeper):
    """A model is a collection of interaction modules that responds to inputs"""
    def __init__(self):
        self._modules = []
        self._time_input = NumericInput("time")
        self._time_output = NumericOutput("rt")

    def run(self):
        # First, update all the inputs, especially time.
        pass

class DataModel(Model):
    """A specific type of model whose inputs are columns in a Pandas DataFrame"""
    def __init__(self, dataframe=None):
        self._dataframe = dataframe
        self._modules = []
        self.inputs = {}
        self.outputs = {}
    
    def add_module(self, module):
        """Adds a module"""
        if isinstance(module, Module):
            module.model = self
            self._modules.append(module)
            
            for input in model.inputs:
                self.inputs.add(input)
                
            for input in model.inputs:
                self.inputs.add(input)
            
        
    def use_mle(self):
        """A module can use MLE iff all of its mapped outputs have probabilities"""
        pass

    def run(self):
        for i in self.dataframe:
            pass


def model():
    """Creates a model based on the specific modules"""
    return Model()


