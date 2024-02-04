# Before starting

this quide is suitable for vscode

if you encounter any problems, contact [breakwater39](mailto:41043152@gm.nfu.edu.tw)

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

and you should see the results like this:

```
/Users/breakwater39/Codes/NFU-Repsitory/.venv/lib/python3.9/site-packages/google/cloud/sql/connector/refresh_utils.py:214: CryptographyDeprecationWarning: Properties that return a naïve datetime object have been deprecated. Please switch to not_valid_after_utc.
  expiration = x509.not_valid_after
TLSv1.3 is not supported with your version of OpenSSL (LibreSSL 2.8.3), falling back to TLSv1.2
Upgrade your OpenSSL version to 1.1.1 for TLSv1.3 support.
Setting environment variables for CloudSQL
GOOGLE_APPLICATION_CREDENTIALS=./Review APP/graphic-pathway-397813-95c959fdc875.json
Setting environment variables for CloudSQL
INSTANCE_CONNECTION_NAME=graphic-pathway-397813:asia-east1:nfu-113-2
DB_PORT=3306
Setting environment variables for CloudSQL
DB_NAME=commentsDB
Setting environment variables for CloudSQL
DB_USER=root
Setting environment variables for CloudSQL
DB_PASS=239mikuNFU@~@
(104001, 'Claire', 'B342222', '1245667')

```