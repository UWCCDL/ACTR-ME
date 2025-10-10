
![image](logo.png) 

# ACTR-ME: ACT-R, Made Easy

A Python package to use ACT-R to analyze behavioral data.

## What is this?

This is a prototype for how ACT-R could be reimplemented to allow for faster creation of reasonable and 
sound models within a typical cognitive psych / cognitive neuroscience workflow. It allows for simulating 
behavior as well as fitting trial-by-trial data of participant data. 

(It is _not_ a full reimplementation of ACT-R, and it does not conform precisely the the ACT-R theory).
### Examples

Some simple, interactive examples of its use are included in the [examples](./examples/examples.ipynb) Jupyter Notebook.  

## Why?

ACT-R is a much better _theory_ to explain behavior that most other models, but researchers still 
prefer other packages such DDM, RL. In fact, even memory researchers seem to prefer DDM or RL to ACT-R.
Why? Most psych/neuro folks want to use models to measure and compare things (patients, conditions, items) 
on their way to understand the mind. ACT-R __can__ do that, but not in an easy way that fits with the typical, 
data analysis workflow of behavioral researchers.

## Design Choices

A few design choices were made:

* All code is written in native Python to allow faster integration with common data science libraries (Numpy, Scipy, 
Matplotlib)
* Production rules are not used unless strictly necessary
* All modules are optional: It is possible to create a model that uses, for example, only declarative memory, or only 
declarative memory combined with a visual module.
* Modules can be connected with each other for simple, sequential workflow
* Models are simple collections of interconnected modules.
* It should be trivial to create a model to analyze a datafile.   

## Classes and Definitions

* A _model_ is a collection of interconnected _modules_. A model functions as the interface between the interconnected  
modules and an outside environment, which could be either another other software or a datafile. 
  * A model has _inputs_ and _outputs_. Inputs and outputs need to be specified from the list of modules within the 
model. A model automatically includes four outputs: the _response_, its associated _probability_, the _response time_, 
and the associated _response time probability_. The probabilities might not be computed. 
  * A model must define a `run` function; the run function examines the model's current inputs and updates and controls
how these inputs flow through the modules.
  * A model must define its own timing. The model keeps track of its internal activity, updates its modules about its 
the current time.    
* A _module_ is a component that provides some basic cognitive ability, such as declarative or procedural memory, 
modeled at the desired level of interest. A models possesses inputs and outputs. A model's output can be connected to 
another model's input, thus describing the flow of control.
  * A module must contain at least one input and one output.
  * A module must define a `run` function; the run function examines the module's current inputs and updates and 
its outputs through its own internal logic and timing.
  * A module must keep track of its own internal time. Before each run, the model might update the module's current 
time for consistency. 
* Inputs and Outputs are the abstract ways in which modules pass information through each other. They can be of two 
types:
  * Symbolic inputs and outputs are dictionary-like key-value structures ("chunks" and "slot-value" pairs in ACT-R
lingo)
  * Numeric inputs and outputs are Python `float`. 
* Inputs and outputs are connected by Connection objects, which define the logic of the connection.
  * All connections are between an input and an output. A dataframe can serves as either an input or an output
  * Connections have an internal logic. For example:
    * Connections between a numeric input and a numeric output simply overwrite the output's value with the input's.
    * Connections between two symbols could either overwrite the entire symbol, or add its contents to the output.
    * Connections between a numeric input and a symbolic output add the numeric value to the output's slot-value pairs. 
      * This connection requires a specification of which key will be overwritten.
      * If the key does not exist, it will be added.
    * Connections between a symbolic input and a numeric output extract the numeric value from a slot and use it
as the value of the output.
      * This connection requires a specification of which slot will be looked at. 
      * The slot must exist.
      * The slot's value will be coerced to `float`.