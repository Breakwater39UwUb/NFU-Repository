import csv, json
# PyTorch
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torch.utils.data.dataset import random_split
import torch.utils.data as data

# BERT Related Libraries
from transformers import BertTokenizer, BertForSequenceClassification

# Python
import pandas as pd
import numpy as np
import os, platform
from my_Packages.bert_paths import multi_label_model
D = ''
device = None

def review_analyze(TEXT: list = [], file_path: str = None):
    '''BERT Predict Multi-labels
    
    TEXT: list of reviews
    file: path to review

    returns list of tuples
        >>> [(label: list of int, text: list of string, time: list of time)]

    Examples:
    ```python
    Passing a list of reviews
    >>> review_analyze(TEXT=list_of_reviews)
    Passing a file containing reviews(csv, json)
    >>> review_analyze(file='SaveData/review.json')
    ```
    '''

    TIME = []
    if file_path is not None:
        TEXT = []
        # Read reviews from json
        if file_path.split('.')[-1] == 'json':
            file = open(file_path, 'r', encoding='utf-8')
            lines = json.load(file)
            for line in lines:
                TEXT.append(line['comment'])
                TIME.append(line['time'])
            file.close()

        # Read reviews from csv
        if file_path.split('.')[-1] == 'csv':
            file = open(file_path, 'r', encoding='utf-8')
            lines = csv.reader(file)
            for line in lines:
                TEXT.append(line[1])
                TIME.append(line[2])
            file.close()

        # debug output
        print(TEXT[0])

    Predictions = []

    # ML Parameters
    LabelNum = 4
    global D
    if (platform.processor() == 'arm'):
        D = 'mps'
    else:
        D = 'cuda'

    global device
    device = torch.device(D)
    print("using device",device)

    # hard code the label dimension to be 4 (because the data has 4 classes)
    num_labels = LabelNum

    # Define model
    model = BertForSequenceClassification.from_pretrained('bert-base-chinese', num_labels=LabelNum)
    model.to(device)

    # Define tokenizer
    tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')

    model.load_state_dict(torch.load(multi_label_model, device))

    for i in range(len(TEXT)):
        if len(TEXT[i]) > 512:
            TEXT[i] = TEXT[i][0:512]
        labels = Predict(model, TEXT[i], tokenizer)
        Predictions.append((labels, TEXT[i], TIME[i]))

    return Predictions

def Predict(model, text, tokenizer):
    # global D
    # device = torch.device(D)
    model.eval()     # Enter Evaluation Mode
    # tokenize the sentences
    encoding = tokenizer(text, return_tensors='pt')
    input_ids = encoding['input_ids']

    attention_mask = encoding['attention_mask']

    # move to GPU if necessary
    global device
    input_ids = input_ids.to(device)
    attention_mask = attention_mask.to(device)

    # generate prediction
    outputs = model(input_ids, attention_mask=attention_mask)  # NOT USING INTERNAL CrossEntropyLoss
    prob = outputs.logits.sigmoid()   # BCEWithLogitsLoss has sigmoid

    # take the index of the highest prob as prediction output
    THRESHOLD = 0.6
    prediction = prob.detach().clone()
    # print(prediction)
    prediction[prediction > THRESHOLD] = 1
    prediction[prediction <= THRESHOLD] = 0

    # AnswerLabel=[]
    HaveAnswer=0

    # for i in range(len(prediction[0])):
    #     if prediction[0][i]==1:
    #         HaveAnswer=1
    #         AnswerLabel.append(text)
    # AnswerLabel.append(text)

    # if HaveAnswer==0:
    #     AnswerLabel.append("No Answer")

    Prediction=[]
    for i in range(len(prediction[0])):
        Prediction.append(int(prediction.tolist()[0][i]))

    return Prediction
