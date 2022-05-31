# Delator

A simple tool that collects TODOS and reports them as GitHub issues.

## How it works

1. Finds an unreported TODO,
2. Commits the reported TODO to the git repo 
3. Reports it to the GitHub as an issue,
4. Repeats the process until all of the unreported TODOs are reported.


## TODO Parsing

### JS Example
```
// TODO: Do something COOL
//  Create api for user
//  Create api for admin
```
Regular experssion - ```^(.*)TODO: .*(\n//(.*).*)*``` - https://regex101.com/r/BWcBjl/1

### Python Example
```
# TODO: Do something COOL
#  Create api for user
#  Create api for admin
```
Regular experssion - ```^(.*)TODO: .*(\n#(.*).*)*``` - https://regex101.com/r/5uzV1Z/1

### Golang Example
```
// TODO: Do something COOL
//  Create api for user
//  Create api for admin
```
Regular experssion - ```^(.*)TODO: .*(\n//(.*).*)*``` - https://regex101.com/r/BWcBjl/1



## How to install

### First Example
- git clone ```https://github.com/leirons/Delator.git```

## Second Example
- pip3 install Delator


## How to run
it will automatically reference the origin remote as standart

Args:

    Required:
        --token
    Not Required:
        --ignore_files
        --ignore_directories


### First Example
```
python main.py --token='your personal token from github'
```

### Second Example
```
python main.py --token='your personal token from github',--ignore_files=d.py,s.py --ignore_directories=secret
```

### Third Example
```
python main.py --token='your personal token from github',--ignore_directories=settings,data
```

### Fourth Example
```
python main.py --token='your personal token from github' --ignore_files=d.py,m.py,secret_data.py
```




