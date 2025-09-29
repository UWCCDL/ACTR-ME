import pandas as pd
import numpy as np
from modules.module import Module


class Model():
    """A model is a collection of interaction modules that responds to inputs"""
    def __init__(self):
        pass

    def run(self):
        pass

class DataModel(Model):
    """A specific type of model whose inputs are columns in a Pandas DataFrame"""
    def __init__(self, dataframe):
        self._dataframe = dataframe
        self._modules = []
        self.inputs = {}
        self.outputs = {}
    
    def add_module(self, module):
        """Adds a module"""
        if isinstance(module, Module):
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


