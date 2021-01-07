### A tool for calculating the cyclomatic complexity of projects written in python

# Installation

```
pip3 install cyclopy
```

# Calculation in a local directory

single file:

```python cc.py -f "./cc.py"``` 

![single file example](https://raw.githubusercontent.com/Split174/cyclopy/assets/example_cc_single.png)

project:

```python cc.py -s path_to_project_src``` 

![example local dir](https://raw.githubusercontent.com/Split174/cyclopy/assets/example_cc_localdir.png)


# Computing from git repository

```python3 cc.py -g "https://github.com/Split174/financial-accounting"```

![git example](https://raw.githubusercontent.com/Split174/cyclopy/assets/example_cc1.png)


# Calculate with limit flag

```python3 cc.py -g "https://github.com/Split174/financial-accounting" -l 5```

![limit flag example](https://raw.githubusercontent.com/Split174/cyclopy/assets/example_cc_limitflag.png)
