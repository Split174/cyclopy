### A tool for calculating the cyclomatic complexity of projects written in python

# Installation

```
pip3 install cyclopy
```

# Calculation in a local directory

single file:

```cyclopy -f "./cc.py"``` 

![single file example](https://raw.githubusercontent.com/Split174/cyclopy/assets/example_cc_single.png)

project:

```cyclopy -s path_to_project_src``` 

![example local dir](https://raw.githubusercontent.com/Split174/cyclopy/assets/example_cc_localdir.png)


# Computing from git repository

```cyclopy -g "https://github.com/Split174/financial-accounting"```

![git example](https://raw.githubusercontent.com/Split174/cyclopy/assets/example_cc1.png)


# Calculate with limit flag

```cyclopy -g "https://github.com/Split174/financial-accounting" -l 5```

![limit flag example](https://raw.githubusercontent.com/Split174/cyclopy/assets/example_cc_limitflag.png)
