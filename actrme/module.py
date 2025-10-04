## essential ACT-R modules: Declarative and Procedural memories
from number import Number
from actrme.basic import InputOutput, ActrIO, Direction
import actrme.model as model

class Connection:
    """A connection between two entitiers"""
    def __init__(self, source, destination):
        self._source = source
        self._destination = destination

    @property
    def source(self):
        return self._source

    @property
    def destination(self):
        return self._destination

class ModuleConnection(Connection):
    """A connection between two modules"""
    def __init__(self, source, destination, extract=None):
        assert isinstance(source, ActrIO)
        assert source.direction == Direction.OUT
        assert isinstance(destination, ActrIO)
        assert destination.direction == Direction.IN
        Connection.__init__(self, source, destination)
        self._extract = extract

    def propagate(self, module):
        pass

class Module(InputOutput):
    """A generic module class"""

    def __init__(self, name="GenericModule"):
        InputOutput.__init__(self)
        self._name = name
        self._model = None
        self._duration = 0.0
        self._duration_probability = 1.0
        self._probability = 1.0

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, newmodel):
        assert isinstance(newmodel, model.Model)
        self._model = newmodel

    @property
    def duration(self):
        """Returns the """
        return self._duration

    @property.setter
    def duration(self, duration):
        """Sets the duration of the module"""
        assert isinstance(duration, Number)
        assert duration >= 0.0
        self._duration = duration

    @property
    def duration_probability(self):
        """Returns the probability of the duration of the module"""
        return self._duration_probability

    @property.setter
    def duration_probability(self, probability):
        """Sets the probability of the duration of the module"""
        assert isinstance(probability, Number)
        assert probability >= 0.0
        self._duration_probability = probability

    @property
    def probability(self):
        """Returns the probability of the module"""
        return self._probability

    @property.setter
    def probability(self, probability):
        """Returns the probability of the module"""
        assert isinstance(probability, Number)
        assert probability >= 0.0
        self._probability = probability

    def run(self):
        # Applies all the functions
        # Returns time
        pass

    def __str__(self):
        return "<%s [module]>" % (self._name)