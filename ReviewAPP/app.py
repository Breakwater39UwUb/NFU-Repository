from flask import Flask, request, render_template, json, url_for
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from numpy import arange
import numpy as np
from datetime import datetime, timedelta
from collections import defaultdict
from my_Packages.scraper import get_reviews
from my_Packages.predictor_1 import review_predict
from my_Packages.predictor_2 import review_analyze
import pandas as pd
from pathlib import Path
flask_template_path = 'web/'	# web/templates/
home_page = 'web.html'	# main.html
predict_page = 'predict.html'
new_predict_page = 'new_predict.html'
analysis_page = 'analysis.html'
platform = ''
chart_html= 'chart.html'
user_rating = 1
bert_rating = 1	# may delete this
answer = ''
bert_rating = ''
id = 0
global labels
labels = {0: 'Food', 1: 'Price', 2: 'Service', 3: 'Environment'}


app = Flask(__name__,
            template_folder=flask_template_path,
            static_folder=flask_template_path,
            static_url_path='')
app.debug = True

@app.route("/")
def Home():
    '''path = 'image/'

    file = Path('image/Food.png')
    file2 = Path('image/Price.png')
    file3 = Path('image/Service.png')
    file4 = Path('image/Conment.png')
    print('Sample Folder: ', os.listdir(path))
    try:
        file.unlink()
        file2.unlink()
        file3.unlink()
        file4.unlink()
        print('Delete File')
        print('Sample Folder: ', os.listdir(path))
    except OSError as e:
        print (f"Delete Problem: {e.strerror}")'''
    return render_template('main.html')

@app.route("/get_Star", methods=['GET','POST']) # Funtion to get Star value
def get_Star():
    '''Set platform to set scrape web
    Foodpanda | Googlemaps
    '''
    global user_rating  
    user_rating  = request.get_json()
    print (user_rating)
    return render_template(predict_page)

@app.route("/get_Passed", methods=['GET','POST']) # Funtion to handle get Star value
def get_Passed():
    passed = request.get_json()
    print (passed)
    '''if(passed == 1):
        path = 'image/'
        file = Path('image/Food.png')
        file2 = Path('image/Price.png')
        file3 = Path('image/Service.png')
        file4 = Path('image/Conment.png')
        print('Sample Folder: ', os.listdir(path))
        try:
            file.unlink()
            file2.unlink()
            file3.unlink()
            file4.unlink()
            print('Delete File')
            print('Sample Folder: ', os.listdir(path))
        except OSError as e:
            print (f"Delete Problem: {e.strerror}")'''

    
    return render_template(predict_page)

@app.route('/get_Change', methods=['POST','GET'])  
def get_Change():    
    '''Show BERT multiclass classification prediction

    Get rating and review from user by form.

    Returns
    user_rating: string
        original user rating
    bert_rating: string
        number in range 0 to 2(class number)
        
        - '0', Negative (1, 2 star)
        - '1', Neutral (3 star)
        - '2', Positive (4, 5 star)
    '''
    if request.method == "POST":
        data = request.form.get("txtbox") 

    print(data)
    answer = (review_predict(q_input=data))  
    
    global bert_rating
    if answer == '0':
        bert_rating = '負向(1,2 星)' # Negative (1, 2 star) 
        #英文子太長超出去，所以改中文
    if answer == '1':
        bert_rating = '中立(3 星)' # Neutral (3 star)
        #英文子太長超出去，所以改中文
    if answer == '2':
        bert_rating = '正向(4,5 星)' # Positive (4, 5 star)
        #英文子太長超出去，所以改中文
    if(data != " "):
       return render_template(new_predict_page, users = user_rating, berts = bert_rating, user_txt = data)
    # This loop is used to Quinary class
    # answers = []
    # for t in range(30):
    #     answers.append(review_predict(q_inputs=txt))
    # bert_rating =  max(set(answers), key=answers.count) + '星'
    

@app.route( "/get_Url" , methods=['POST','GET'])
def get_Url():

    
    # TODO: format should select by user
    global id
    if request.method == "POST":
        data_url = request.form.get("txtbox")  
        id+=1
    print(data_url)

    if data_url is None :
        raise ValueError('Please input a url under "Overview tab".')
    
    try:

        if(data_url != " "):
            # may remove the check_cache until client web have proper function to handle
            review_file = get_reviews(url=data_url, webname=platform, format= 'json', check_cache=True)
            predictions = review_analyze(file_path=review_file)
            filtered_data = [d for d in predictions  if d[2].split('/')[1] != '']
            sort_by_label(filtered_data,0,'Food.png','web')
            sort_by_label(filtered_data,1,'Price.png','web')
            sort_by_label(filtered_data,2,'Service.png','web')
            sort_by_label(filtered_data,3,'Conment.png','web')
            debug_type(predictions)
            analysis = calculate_labels(predictions)
            return render_template(chart_html,
                                str1=analysis[0], str2=analysis[1], str3=analysis[2], str4=analysis[3],
                                Food = "image/Food.png",
                                Price = "image/Price.png",
                                Service = "image/Service.png",
                                Conment = "image/Conment.png"
                                )
        
    except:
        raise Exception(f'Failed to get review on\n{data_url}\n')

def calculate_labels(labels: list[tuple]):
    '''Calculate all labels and show results on web

    labels: list of tuples
        [(label, text, time), ]

    4 labels:
        [food, price, service, environment]
    '''

    analysis = [0, 0, 0, 0]

    for label in labels:
        index = 0
        for value in label[0]:
            if value:
                analysis[index] += 1
            index += 1

    return analysis





def read_review_file(FILE: str):
    '''Read lines from file for the BERT
    '''

    TEXT = []

    if FILE.split('.')[-1] == 'json':
        with open(FILE, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for line in data:
                TEXT.append(line['comment'])
        return TEXT

def debug_type(var):
    print('----------')
    print(f'Type: {type(var)}')
    if type(var) is list:
        print(f'type(var[0]): {type(var[0])}')
        print(f'var[0]: {var[0]}')
    else:
        print(f'value: {var}')

@app.route("/get_chart_args", methods=['GET', 'POST'])
def get_chart_args():
    '''

    get time range, check range within a year or not,
    if picked across a year, alert it to only pick within a year
    or range from one year ealier.
    time range: [start, end]

    choose one label type, food, price...

    '''

def sort_by_month(data: list):
    '''Count reviews per month

    data: list[tuple]
        reviews from review_analyze
    chart_type: str
        >>> 'plot' or 'bar'
    '''
    counts = defaultdict(int)

    # Count the number of data points for each month
    for d in data:
        # Extract time
        time = datetime.strptime(d[2], "%Y/%m")
        # Increment count
        counts[time] += 1

    # Sort times and counts for plotting
    times, counts = zip(*sorted(counts.items()))
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(times, counts)
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m'))

    plt.plot(times, counts)
    plt.xlabel('Month')
    plt.ylabel('Data Count')
    plt.title('Data Count Over Time')
    plt.show()

def sort_by_label(data: list, label: int, save_filename: str = None, save_folder: str = None):
    '''Count 1 label per month
    
    data: list of data
        [[label], content, time]
    label: int of label
    '''
    counts = defaultdict(int)
    label_counts = defaultdict(int)

    # Count the number of data points for each month
    for d in data:
        time = datetime.strptime(d[2], "%Y/%m")
        counts[time] += 1

        if (d[0][label]):
            label_counts[time] += 1
        else:
            label_counts[time] += 0

    # Sort times and counts for plotting
    times, counts = zip(*sorted(counts.items()))
    times, label_counts = zip(*sorted(label_counts.items()))
    fig, ax = plt.subplots(figsize=(12, 6))
    # ax.plot(times, counts)
    # ax.xaxis.set_major_locator(mdates.MonthLocator())
    # ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m'))

    global labels
    plt.bar(times, counts, 10, color='red', label='Total')
    plt.plot(times, label_counts, label=f'Label: {labels[label]}')
    plt.xlabel('Month')
    plt.ylabel('Data Count')
    plt.legend()
    plt.title('label Count per Time')
    #plt.show()
    if save_folder:
        os.makedirs(save_folder, exist_ok=True)
        save_path = os.path.join(save_folder, save_filename)
        plt.savefig(save_path)


def compare_labels(data: list, comp_labels: list):
    '''Compare data with given labels
    
    data: list[tuple]
        list of reviews
    comp_labels: list[int]
        list of labels to compare

        ex:
        >>> compare data with 'Food', 'Service', 'Enviroment'
        >>> [0, 2, 3]
    '''

    bar_width = 10

    # create list of labels counter
    label_counts = []
    for n in range(4):
        label_counts.append(defaultdict(int))

    for d in data:
        time = datetime.strptime(d[2], "%Y/%m")
        for label in comp_labels:
            if (d[0][label]):
                label_counts[label][time] += 1
                continue
            label_counts[label][time] += 0
            
    bar_width = 0.15  # Adjust as needed

    fig, ax = plt.subplots(figsize=(12, 6))

    # Convert times to numbers for plotting
    all_times = sorted(list(set([time for index in comp_labels for time in label_counts[index].keys()])))
    time_indices = np.arange(len(all_times))

    for i, index in enumerate(comp_labels):
        counts = [label_counts[index].get(time, 0) for time in all_times]
        plt.bar(time_indices + i*bar_width, counts, bar_width, label=labels[index])

    plt.xlabel('Month')
    plt.ylabel('Data Count')
    plt.legend()
    plt.title('Label Count per Time')
    plt.xticks(time_indices + bar_width, [time.strftime("%Y/%m") for time in all_times])
    #plt.show()


if __name__ == "__main__":
    app.run(port=8900)
