import glob

def check_loacal_cache(query: str, query_dir: str = 'SaveData\\', file_type: str = '.json'):
    '''Check if the given file is in local directory or database
    
    query: target file
    query_dir: target directory
    file_type: target file extension
    '''

    files = glob.glob(query_dir+'*.'+file_type)
    for file in files:
        if query in file:
            return True
        
    return False