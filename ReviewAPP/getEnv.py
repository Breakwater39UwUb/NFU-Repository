# save these into environment variables

# export GOOGLE_APPLICATION_CREDENTIALS=/graphic-pathway-397813-95c959fdc875.json
# export INSTANCE_CONNECTION_NAME='graphic-pathway-397813:asia-east1:nfu-113-2'
# export DB_PORT='3306'
# export DB_NAME='commentsDB'
# export DB_USER='root'
# export DB_PASS='239mikuNFU@~@'

import os

check_list = ["GOOGLE_APPLICATION_CREDENTIALS", "INSTANCE_CONNECTION_NAME", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASS"]
vars = {check_list[0]: "./ReviewAPP/graphic-pathway-397813-95c959fdc875.json",
        check_list[1]: "graphic-pathway-397813:asia-east1:nfu-113-2",
        check_list[2]: "3306",
        check_list[3]: "commentsDB",
        check_list[4]: "root",
        check_list[5]: "239mikuNFU@~@"}

def test_env_vars():
    for arg in check_list:
        env_var = os.environ.get(arg)
        if(env_var == None):
            print('Setting environment variables for CloudSQL')
            os.environ[arg] = vars[arg]
            env_var = os.environ.get(arg)
        print(f'{arg}={env_var}')
