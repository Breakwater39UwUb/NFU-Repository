# Before starting

this quide is suitable for vscode

# Guidelines

## step 1

in the terminal, check current directory is

    NFU-Repsitory>

then create a python virtual environment by running these commands in terminal
```bash
py -m venv env
# activate python virtual environment
.\env\Scripts\activate
# deactivate python virtual environment
.\env\Scripts\activate
```

if you encounter problems to execute this command, try this powershell command

```
Set-ExecutionPolicy Unrestricted -Scope Process
```

install dependencies packages

    pip install -r requirements_for_sql.txt

## step 2

under virtual environment, run sql_connect_test.py

the test function will create a new table on the SQL

