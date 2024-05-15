import glob, os, re

def check_loacal_cache(query: str, query_dir: str = 'SaveData', file_type: str = '.json'):
    '''Check if the given file is in local directory or database
    
    query: target file
    query_dir: target directory
    file_type: target file extension
    '''
    search = os.path.join(query_dir,'*')+'.'+file_type
    files = glob.glob(search)
    for file in files:
        if query in file:
            return True

    return False

def convert_to_tablename(filepath: str):
    '''Convert file path to tablename
    filepath: like './SaveData/review-Google地圖.json'

    return 
    ---

    table_name: str
        table name surrounded by sql escape
        >>> `table_name`
    '''

    table_name = '`' + filepath.split('/')[1].split('-')[0] + '`'
    return table_name
