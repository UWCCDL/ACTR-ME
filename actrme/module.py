## essential ACT-R modules: Declarative and Procedural memories
import actrme.model as model
from actrme.basic import InputOutput, TimeKeeper, SymbolicOutput, SymbolicInput, NumericOutput, NumericInput

class Module(InputOutput):
    """A generic module class"""

    def __init__(self, name="GenericModule"):
        InputOutput.__init__(self)
        self._name = name
        self._model = None

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, newmodel):
        assert isinstance(newmodel, Model)
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
