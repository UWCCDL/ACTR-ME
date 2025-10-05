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
        """Generic run function"""
        # This should be a simple generic function that runs through all the
        # non-empty input modules and propagates them until the model is stable.
        # (e.g., no more cognitive cycles).



class DataInputMapping:
    """An input mapping a mapping from a column of a dataframe to a module input"""
    def __init__(self, source, destination, rename):
        self._source = source
        self._destination = destination
        self._rename = rename

    @property
    def source(self):
        return self._source
    @property
    def destination(self):
        return self._destination
    @property
    def rename(self):
        return self._rename

    def __str__(self):
        name = '' if self._name == None else '%s' % self._name
        return "<Value %s From '%s' To '%s'>" % (name, self._source.name, self._destination)

    def __repr__(self):
        return self.__str__()

class DataOutputMapping:
    """An output mapping from  module output to column of a dataframe"""

    def __init__(self, source, destination, extract=None, rename=None):
        self._source = source
        self._destination = destination
        self._extract = extract

    @property
    def source(self):
        return self._source
    @property
    def destination(self):
        return self._destination

    @property
    def extract(self):
        return self._extract

    def __str__(self):
        val = '' if self._extract == None else '%s' % self.extract
        return "<Value %s From %s To '%s'>" % (val, self._source.name, self._destination)

    def __repr__(self):
        return self.__str__()


class DataModel(Model):
    """A specific type of model whose inputs are columns in a Pandas DataFrame"""
    def __init__(self, dataframe=None):
        Model.__init__(self)
        assert isinstance(dataframe, pd.DataFrame)
        self._dataframe = dataframe
        self._input_mappings = []
        self._output_mappings = []

    @property
    def dataframe(self):
        return self._dataframe

    @dataframe.setter
    def dataframe(self, dataframe):
        self._dataframe = dataframe

    @property
    def input_mappings(self):
        return self._input_mappings

    @property
    def output_mappings(self):
        return self._output_mappings

    def mappings(self):
        return {**self._input_mappings, **self._input_mappings}

    def connect_input(self, column, inpt, rename=None):
        """Connects a dataframe column to an input"""
        assert isinstance(column, str)
        assert isinstance(inpt, basic.ActrIO)
        assert inpt.direction == basic.Direction.IN
        assert column in self._dataframe.columns, "Column '%s' not in dataframe" % column
        mapping = DataInputMapping(column, input, rename)
        self._input_mappings.append(mapping)

    def connect_output(self, column, outpt, extract=None):
        """Connects a dataframe column to an output"""
        assert isinstance(column, str)
        assert isinstance(outpt, basic.ActrIO)
        assert outpt.direction == basic.Direction.OUT
        assert column in self._dataframe.columns
        if extract == None:
            extract = column
        mapping = DataOutputMapping(column, outpt, extract=extract)
        self._output_mappings.append(mapping)

    def fit(self):
        """A module can use MLE iff all of its mapped outputs have probabilities"""
        pass

    def propagate(self):
        """propagate"""
        pass

    def run(self):
        for index, row in self._dataframe.iterrows():
            # Set up all the inputs
            for mapping in self.input_mappings:
                column = mapping.source
                actrio = mapping.destination
                name = column if mapping.rename is None else mapping.rename
                if isinstance(actrio, basic.SymbolicIO):
                    actrio.modify({name:str(row[column])})
                elif isinstance(column, basic.NumericIO):
                    actrio.value = float(row[column])

            # Now run the model
            self.propagate()

            # Now collect the outputs and store them in the desired columns
            for mapping in self.output_mappings:
                column = mapping.destination
                actrio = mapping.source
                extract = mapping.extract
                assert isinstance(actrio, basic.ActrIO)
                assert isinstance(column, str)
                assert isinstance(extract, str)
                if isinstance(actrio, basic.SymbolicIO):
                    row.at[index, column] = actrio.value[extract]
                elif isinstance(column, basic.NumericIO):
                    row.at[index, column] = actrio.value

