### A tool for calculating the cyclomatic complexity of projects written in python

#### Installation

```
git clone https://github.com/Split174/cyclopy ~/path/to/
cd ~/path/to/
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Usage

##### Calculation in a local directory

single file:

```python cc.py -f cc.py``` 

project:

```python cc.py -d path_to_project_src``` 

##### Computing from git repository

```python3 cc.py -g "https://github.com/Split174/financial-accounting```

