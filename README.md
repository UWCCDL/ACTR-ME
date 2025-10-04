
![image](logo.png) 

# ACTR-ME: ACT-R, Made Easy

A Python package to use ACT-R to analyze behavioral data.

## What is this?

This is a prototype for how ACT-R could be reimplemented to allow for faster creation of reasonable and 
sound models within a typical cognitive psych / cognitive neuroscience workflow. It allows for simulating 
behavior as well as fitting trial-by-trial data of participant data.

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
* All modules are optional: it is possible to create a model that uses, for example, only declarative memory, or only 
declarative memory combined with a visual module.
* Modules can be connected with each other for simple, sequential workflow