import glob, os, re, calendar
from datetime import datetime, timedelta

invalid_chars = '<>:"/\|?*｜\n. '
invalid_char_pattern = '|'.join(map(re.escape, invalid_chars))
webname_filter = re.compile(invalid_char_pattern)
'''re object with pattern: '<>:"/\|?*｜\\n .\''''

change_comma = ','
comma_filter = re.compile(change_comma)
'''re object with pattern: ',\''''

time_filter_zh = ['天前', '週前', '個月前', '年前']
''''天前', '週前', '個月前', '年前\''''
time_filter_en = ['days', 'week', 'month', 'year']
''''days', 'week', 'month', 'year\''''

# TODO: Add check_sql_cache
def check_loacal_cache(query: str, query_dir: str = 'SaveData', file_type: str = '.json'):
    '''Check if the given file is in local directory or database
    
    query: target file
    query_dir: target directory
    file_type: target file extension

    File name convention:

    ```text
    {title}_{type}_{time range}.json
    title: restaurant name
    type: 'all', 'filtered'
        all time or filtered time range
    time_range: '2024', '2023-03~2024-04'
        depending on type, 
    ```
    '''

    search = os.path.join(query_dir,'*')+'.'+file_type
    files = glob.glob(search)
    for file in files:
        if query in file:
            return file

    return None

def convert_to_tablename(filepath: str):
    '''Convert file path to tablename
    filepath: like './SaveData/review-Google地圖.json'

    return 
    ---

    table_name: str
        table name surrounded by sql escape
        >>> `table_name`
    '''

    table_name = '`' + filepath.split('/')[2].split('-Google')[0] + '`'
    return table_name

# TODO: create a function to create filename with date range
def gen_diagram_name(date_range: str):
    filename = './SaveData/dia.png'
    
    return filename

# TODO: create directory name by restaurant
def create_dir(name: str, path: str='SaveData'):
    if not os.path.exists(name):
        os.makedirs(name)

def sort_times(start_time: str, end_time: str):
    '''Sort time

    If user picked start time that is later than end time,
    this function will help to sort the time in right order.
    
    start_time: 'YYYY-MM'
    end_time: 'YYYY-MM'

    return right order
    '''

    # Convert the time strings to datetime objects
    start_time = datetime.strptime(start_time, '%Y-%m')
    end_time = datetime.strptime(end_time, '%Y-%m')

    # If the start time is later than the end time, swap them
    if start_time > end_time:
        start_time, end_time = end_time, start_time

    # Convert the datetime objects back to strings
    start_time = datetime.strftime(start_time, '%Y-%m')
    end_time = datetime.strftime(end_time, '%Y-%m')

    return start_time, end_time

def check_month_range(time: datetime, time_range: str='all'):
    '''Check if data in time range
    
    time: str
        format in '2024-01-01 00:00:00'
    time_range: string
        String with start time and end time, separated by space

        if 'all', ignore condition
        >>> '2003-05 2004-03'
    '''
    if time_range == 'all':
        return True

    start_date, end_date = time_range.split(' ')
    start_date = datetime.strptime(start_date, '%Y-%m')
    end_date = datetime.strptime(end_date, '%Y-%m')
    # substract one month from start date
    last_day_of_prev_month = start_date.replace(day=1) - timedelta(days=1)
    # Calculate the same day of the previous month
    start_date = last_day_of_prev_month.replace(day=1)

    # EOM: End Of Month
    start_EOM = calendar.monthrange(start_date.year, start_date.month)[1]
    end_EOM = calendar.monthrange(end_date.year, end_date.month)[1]

    # datetime object
    start_date = start_date.replace(day=start_EOM)
    end_date = end_date.replace(day=end_EOM)

    if time >= start_date and time <= end_date:
        return True
    return False

def valid_time_interval(time_interval:list[str], to_check:str):
    pos = 0
    time = ''
    valid_num = int(time_interval[0])
    valid_time_ago = time_interval[1]
    valid_interval = time_interval[2]

    # Find date in review text
    review_rel_time = to_check.split()

    if review_rel_time[1] not in time_interval[1]:
        return False

    # review: "time" ago != "valide time" ago
    if review_rel_time[1] != valid_time_ago:
        return False
    if valid_interval == 'after':
        if int(review_rel_time[0]) > valid_num:
            return False
    if valid_interval == 'before':
        if int(review_rel_time[0]) < valid_num:
            return False
    return True

def get_review_abs_time(time_ago: str):
    review_rel_time = time_ago.split()
    time_now = datetime.now()
    if review_rel_time[1] == time_filter_zh[0]:
        new_time = time_now - timedelta(days=int(review_rel_time[0]))
    if review_rel_time[1] == time_filter_zh[1]:
        new_time = time_now - timedelta(weeks=int(review_rel_time[0]))
    if review_rel_time[1] == time_filter_zh[2]:
        new_time = time_now - timedelta(days=int(review_rel_time[0])*30)
    if review_rel_time[1] == time_filter_zh[3]:
        new_time = time_now - timedelta(days=int(review_rel_time[0])*365)
        return new_time.strftime('%Y/')
    return new_time.strftime('%Y/%m')