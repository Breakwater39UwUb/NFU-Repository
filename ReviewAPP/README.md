# ReviewAPP

- [ReviewAPP](#reviewapp)
  - [Brief Introduction](#brief-introduction)
  - [Guide to install and development](#guide-to-install-and-development)
    - [Install](#install)
    - [Development](#development)
  - [How to use](#how-to-use)
  - [Todo](#todo)
  - [Fix](#fix)
  - [Dataset](#dataset)
  - [Database implementation](#database-implementation)
  - [Issue and work-around](#issue-and-work-around)

## Brief Introduction

Web implementates with flask

~~[pyside2_for_android][]~~

Scraped data from internet are saved in the [SaveDate](./SaveData/)

## Guide to install and development

### Install

1. Download this project.

    ```bash
    git clone https://github.com/Breakwater39UwUb/NFU-Repsitory.git
    ```

2. Go to ReviewAPP directory

    ```bash
    cd ./ReviewAPP
    ```

3. Create python virtual environment

    ```bash
    /ReviewAPP $ pip -m venv env
    ```

    Alternatively, you can create through VS Code.

4. After creating the virtual environment, install packages

    ```bash
    /ReviewAPP $ pip install -r requirements.txt
    ```

5. Setup MySQL server connection configuration

    Make sure you have the URL host in [ngrok.txt](./ngrok.txt),
    for further steps, see [here][ref_sql]

6. Download the trained_model from OneDrive

   - Download the file from [this link][trained_model].
   - Extract the file to project root like this:

       ```text
           +-- ReviewAPP
           |   +-- albert
           |   +-- Images
           |   +-- SaveData
           |   +-- Src
           |   +-- trained_model
           |   +-- web
           |   +-- app.py
       ```

### Development

If you see ```'Error to scrape the webdriver'``` in terminal, just try again

> If you met any error, contact [防波堤](mailto:41043152@gm.nfu.edu.tw)

## How to use

Run application

```bash
ReviewAPP $ python app.py
```

In browser, go to <http://127.0.0.1:8900>

## Todo

- To prevent ngrok.txt path is not found, add a try/catch block
  - Make quick troubleshooting guide for users

- Close the chromedriver properly, preventing from too many zombie processes in background

## Fix

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
    |   +-- column 1: rating INT
    |   +-- column 2: txt VARCHAR(1024)
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

[pyside2_for_android]: https://stackoverflow.com/questions/70907303/pyside2-for-android-development "Android Development"
[trained_model]: https://nfuedu-my.sharepoint.com/:u:/g/personal/41043152_nfu_edu_tw/EehfyMuKe0VFmVjRY1o0gYAB7gOqdc0cXsKPx_ZrZMEq2w "Model link"
[restaurant_url1]: https://www.google.com/maps/place/%E7%95%B0%E4%BA%BA%E9%A4%A8+%E6%9D%B1%E8%8B%B1%E5%BA%97/@24.14262,120.7056438,20z/data=!4m6!3m5!1s0x34693dc4fc54b2bd:0xb150f911a4f6a718!8m2!3d24.14262!4d120.7062393!16s%2Fg%2F11j5npjg01?entry=ttu "Link for web scraping"
[ref_sql]: ./guide%20to%20test%20CloudSQL.md#set_ngrok_host "Reference on other Markdown"
