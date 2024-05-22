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
flask_template_path = 'web/'	# web/templates/
home_page = 'web.html'	# main.html
predict_page = 'predict.html'
analysis_page = 'analysis.html'
platform = ''
user_rating = 1	# may delete this
bert_rating = 1	# may delete this

app = Flask(__name__,
            template_folder=flask_template_path,
            static_folder=flask_template_path,
            static_url_path='')
app.debug = True

@app.route("/")
def Home():
    return render_template(home_page)

@app.route("/get_user_review", methods=['POST'])
def get_user_review():
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

    user_rating = request.form['star'] + '星'
    txt = [request.form['txt']]
    # This loop is used to Quinary class
    # answers = []
    # for t in range(30):
    #     answers.append(review_predict(q_inputs=txt))
    # bert_rating =  max(set(answers), key=answers.count) + '星'
    
    answer = (review_predict(q_input=txt))
    if answer == '0':
        bert_rating = 'Negative (1, 2 star)'
    if answer == '1':
        bert_rating = 'Neutral (3 star)'
    if answer == '2':
        bert_rating = 'Positive (4, 5 star)'

    return render_template(predict_page, users = user_rating, berts = bert_rating)

@app.route("/get_predict")
def get_predict():
    '''Show BERT multi-label classification prediction
    
    Get reviews from the given url and save them as csv or json files.
    
    Read and predict 4 labels of reviews from the files.
    
    return
        calculate all label and show results on web
    '''
    
    # TODO: format should select by user

    try:
        # may remove the check_cache until client web have proper function to handle
        global scrape_url
        review_file = get_reviews(url=scrape_url, webname=platform, format= 'json', check_cache=True)
        predictions = review_analyze(file_path=review_file)
        debug_type(predictions)
        analysis = calculate_labels(predictions)
        return render_template(analysis_page,
                            str1=analysis[0], str2=analysis[1], str3=analysis[2], str4=analysis[3])
    except:
        raise Exception(f'Failed to get review on\n{scrape_url}\n')

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

@app.route("/get_platform", methods=['GET','POST'])
def get_platform():
    '''Set platform to set scrape web
    Foodpanda | Googlemaps
    '''

    global platform
    platform = request.get_json()
    return ('', 204)

@app.route("/get_url", methods=['GET', 'POST'])
def get_url():
    '''Get url for web scraper
    '''
    
    global scrape_url
    scrape_url = request.get_json()
    
    if scrape_url is None :
        raise ValueError('Please input a url under "Overview tab".')
    return ('', 204)

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

def sort_by_label(data: list, label: int):
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
    plt.show()

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
    plt.show()

if __name__ == "__main__":
    app.run(port=8900)
