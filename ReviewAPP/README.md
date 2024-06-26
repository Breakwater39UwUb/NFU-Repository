# ReviewAPP

- [ReviewAPP](#reviewapp)
  - [Brief Introduction](#brief-introduction)
  - [Guide to install and development](#guide-to-install-and-development)
    - [Install](#install)
      - [pytorch](#pytorch)
    - [Development](#development)
  - [How to use](#how-to-use)
  - [Todo](#todo)
    - [Fix](#fix)
  - [Dataset](#dataset)
  - [Database implementation](#database-implementation)
  - [Issue and work-around](#issue-and-work-around)
  - [git commands](#git-commands)

## Brief Introduction

Web implementates with flask

Scraper is forked and modified from [MajideND][scraper reference]

~~[pyside2_for_android][]~~

Scraped data from internet are saved in the [SaveDate](./SaveData/)

## Guide to install and development

### Install

1. Download this project.

    ```bash
    git clone https://github.com/Breakwater39UwUb/NFU-Repository.git
    ```

2. Go to ReviewAPP directory

    ```bash
    cd ./ReviewAPP
    ```

3. Create python virtual environment

    1. Create through python command

        ```bash
        /ReviewAPP $ python -m venv env
        ```

    2. Alternatively, you can create through VS Code.
       1. <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd>
       2. Enter `Create Environment`
       3. Select `Venv`
       4. Select `Python 3.9.7 64-bit` or other version
       5. Select `requirements.txt`
       6. Press <kbd>OK</kbd>
       7. VS Code auto create environment with specified requirements packages.
    3. Activate virtual environment

       ```bash
       Set-ExecutionPolicy Unrestricted -Scope Process
       env\Scripts\activate
       ```

4. After creating the virtual environment, install packages

    ```bash
    /ReviewAPP $ pip install -r requirements.txt
    ```

5. Setup MySQL server connection configuration

    Make sure you have the URL host in [ngrok.txt](./ngrok.txt),
    for further steps, see [here][ref_sql]

6. Download the trained_model from OneDrive

   - Download the file from [this link][trained_model].
     - multi_label-model.zip
     - trinary_model.zip
   - Extract the file to project root like this:

       ```text
        +-- ReviewAPP
        |   +-- trained_model
        |   +-- web
        |   +-- app.py
       ```

#### pytorch

```bash
pip install torch==2.2.1 torchvision==0.17.1 torchaudio==2.2.1 --index-url https://download.pytorch.org/whl/cu118
```

### Development

User send url to API `get_Url`,
then check if local cache is expired,
scrape web if expired, else use cached.

Cached file saves review time, text and labels.

File name convention:

```text
{title}_{type}_{time range}.json

title: restaurant name
type: 'all', 'filtered'
  all time or filtered time range
time_range: '2024', '2023-03~2024-04'
  depending on type, 
```

> If you met any error, contact [防波堤](mailto:41043152@gm.nfu.edu.tw)

## How to use

Run application

```bash
ReviewAPP $ python app.py
```

In browser, go to <http://127.0.0.1:8900>

All saved reviews in `SaveDate/{restaurant}/`

## Todo

- To prevent ngrok.txt path is not found, add a try/catch block
  - Make quick troubleshooting guide for users

- Close the chromedriver properly, preventing from too many zombie processes in background

### Fix

1. Web scraper sometimes doen't works as expected.
2. Weird error from flask

    ```bash
    "GET /null HTTP/1.1" 404 -
    ```

## Dataset

BERT multi class model

- 8864 records
  - 7178 (90%) for training
  - 798 (10%) for validating
  - 888 (10%) for testing

BERT multi label model

- 3346 records
  - (%)for training
  - (%) for validating
  - (10%) for testing

## Database implementation

```text
+-- Database: reviews
    +-- Table: reviews
    |   +-- column 1: time_range CHAR(8)
    |   +-- column 2: rating INT
    |   +-- column 3: txt VARCHAR(1024)
```

## Issue and work-around

1. open pyside6-designer on macOS in a virtual environment

    ```bash
    open .venv/lib/python3.9/site-packages/PySide6/Designer.app 
    ```

2. generate python code from ui files

    ```bash
    pyuic5.exe -x ./Src/uifiles.ui -o ouput.py
    ```

3. Can not run predict on macOS

    AssertionError: Torch not compiled with CUDA enabled

    ```bash
    pip3 install torch torchvision torchaudio
    ```

4. Web scraping take too long to get reviews on website

    [This restaurant][restaurant_url1] takes 3 minutes to get 554 reviews, but 925 on the website.

## git commands

1. Marked assume-unchanged.

    This will tell git you want to start ignoring the changes to the file

    ```bash
    git update-index --assume-unchanged path/to/file
    ```

    When you want to start keeping track again

    ```bash
    git update-index --no-assume-unchanged path/to/file
    ```

1. Show marked assume-unchanged.

    You can use `git ls-files -v`. If the character printed is lower-case, the file is marked assume-unchanged.

    To print just the files that are unchanged use:

    ```bash
    git ls-files -v | grep '^[[:lower:]]'
    ```

    To embrace your lazy programmer, turn this into a git alias. Edit your .gitconfig file to add this snippet:

    ```conf
    [alias]
        ignored = !git ls-files -v | grep "^[[:lower:]]"
    ```

    Now typing `git ignored` will give you output like this:

    ```bash
    h path/to/ignored.file
    h another/ignored.file
    ```

[pyside2_for_android]: https://stackoverflow.com/questions/70907303/pyside2-for-android-development "Android Development"
[trained_model]: https://nfuedu-my.sharepoint.com/personal/41043152_nfu_edu_tw/_layouts/15/onedrive.aspx?id=%2Fpersonal%2F41043152%5Fnfu%5Fedu%5Ftw%2FDocuments%2FSchool%5Fproject%5F113 "Model link"
[restaurant_url1]: https://www.google.com/maps/place/%E7%95%B0%E4%BA%BA%E9%A4%A8+%E6%9D%B1%E8%8B%B1%E5%BA%97/@24.14262,120.7056438,20z/data=!4m6!3m5!1s0x34693dc4fc54b2bd:0xb150f911a4f6a718!8m2!3d24.14262!4d120.7062393!16s%2Fg%2F11j5npjg01?entry=ttu "Link for web scraping"
[ref_sql]: ./guide%20to%20test%20CloudSQL.md#set_ngrok_host "Reference on other Markdown"
[scraper reference]: https://github.com/MajideND/scraping-reviews-from-googlemaps
