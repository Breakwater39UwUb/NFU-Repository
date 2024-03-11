# ReviewAPP

Web implementates with flask

~~[pyside2_for_android][]~~

Scraped data from internet are saved in the [SaveDate](./SaveData/)

## Guide to debugging and development

### 1. Make sure you have the URL host in [ngrok.txt](./ngrok.txt), for steps, see [here](./guide%20to%20test%20CloudSQL.md#set_ngrok_host)

### 2. if you see ```'Error to scrape the webdriver'``` in terminal, just try again

### 3. Properly sets the flask templates directory

### 4. Download the [trained_model][] from OneDrive

- Download the file from above link.
- Extract the file to project root like this:

    ```+-- Database: reviews
        +-- ReviewAPP
        |   +-- albert
        |   +-- Images
        |   +-- SaveData
        |   +-- Src
        |   +-- trained_model
        |   +-- web
        |   +-- app.py
    ```

> If you met any error, contact [防波堤](mailto:41043152@gm.nfu.edu.tw)

## Web interface

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

[pyside2_for_android]: https://stackoverflow.com/questions/70907303/pyside2-for-android-development "Android Development"
[trained_model]: https://nfuedu-my.sharepoint.com/:u:/g/personal/41043152_nfu_edu_tw/EehfyMuKe0VFmVjRY1o0gYABA3Om_QTfJMLkevAbtKZpKA?e=a4oAik
