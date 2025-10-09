import actrme.basic as basic
import pandas as pd

class DataModel(basic.Model):
    """A specific type of model whose inputs are columns in a Pandas DataFrame"""
    def __init__(self, dataframe=None):
        basic.Model.__init__(self)
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
        mapping = basic.DataInputMapping(column, input, rename)
        self._input_mappings.append(mapping)

    def connect_output(self, column, outpt, extract=None):
        """Connects a dataframe column to an output"""
        assert isinstance(column, str)
        assert isinstance(outpt, basic.ActrIO)
        assert outpt.direction == basic.Direction.OUT
        assert column in self._dataframe.columns
        if extract == None:
            extract = column
        mapping = basic.DataOutputMapping(column, outpt, extract=extract)
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

