# 使用說明
1. 設定網址

    把網址放進 [env.py](./env.py)

    ```python
        URLs = [
            # 把網址放入此串列, 用雙引號 "" 包住
        ]
    ```
    主程式的第 127 行 的 env.URLs 會從這裡讀網址

    ```python
        for pages in env.URLs:
            ...
    ```

2. 執行 [app.py](./app.py)

3. 程式會輸出 csv 檔案