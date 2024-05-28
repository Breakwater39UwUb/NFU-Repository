'''
This module contains functions to plot review counts per time
'''
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from collections import defaultdict
from my_Packages.utils import check_month_range
global labels
labels = {0: 'Food', 1: 'Price', 2: 'Service', 3: 'Environment'}
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

def plot_by_label(data: list,
                  label: int,
                  time_range: str,
                  save_filename: str = None,
                  save_folder: str = None):
    '''Count given label per month
    
    data: list[tuple]
        reviews from review_analyze
        >>> ([1, 1, 1, 1], 'text', '2024/02')
    label: int from label list
        >>> 0: food, 1: price, 2: service, 3: environment
    time_range: string
        start month and end month, separated by space
        >>> '2003-05 2004-03'
    chart_type: str
        >>> 'plot' or 'bar'
    save_filename: str
        image file name
    save_folder: str
        path
    '''
    counts = defaultdict(int)
    label_counts = defaultdict(int)

    # Count the number of data points for each month
    for d in data:
        time = datetime.strptime(d[2], "%Y/%m")

        # Check if the data points are in the time range
        if check_month_range(time, time_range) is not True:
            continue

        counts[time] += 1

        # count label
        if (d[0][label]):
            label_counts[time] += 1
        else:
            label_counts[time] += 0

    # Sort times and counts for plotting
    times, counts = zip(*sorted(counts.items()))
    times, label_counts = zip(*sorted(label_counts.items()))
    fig, ax = plt.subplots(figsize=(12, 6))
    # ax.plot(times, counts)
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m'))

    global labels
    print(f'debug-----------------------------------------------------------\n{times}\n{counts}')
    plt.bar(times, counts, 10, color='red', label='Total')
    plt.plot(times, label_counts, label=f'Label: {labels[label]}')
    plt.xlabel('Month')
    plt.ylabel('Review Count')
    plt.legend()
    plt.title('Label Count per month')

    # TODO: Save file to ./Saved_images
    # TODO: Create directory if it doesn't exist
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