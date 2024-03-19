import csv
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
import os
from Packages.bert_paths import PATH_multi_label_model

def review_analyze(TEXT: list, file: str = None):
    '''BERT Predict Multi-labels
    
    TEXT: list of reviews
    file: path of json file

    returns list of label predictions
    '''

    Predictions = []

    # ML Parameters
    LabelNum = 4
    D = 'cuda'

    device = torch.device(D)
    print("using device",device)

    # hard code the label dimension to be 4 (because the data has 4 classes)
    num_labels = LabelNum

    # Define model
    model = BertForSequenceClassification.from_pretrained('bert-base-chinese', num_labels=LabelNum)
    model.to(device)

    # Define tokenizer
    tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')

    model.load_state_dict(torch.load(PATH_multi_label_model))

    for i in range(len(TEXT)):
        Prediction, Answer = Predict(model, TEXT[i], device, D, tokenizer)
        Predictions.append(Prediction)

    return Predictions

def Predict(model, text , device, D, tokenizer):
    device = torch.device(D)
    model.eval()     # Enter Evaluation Mode
    # tokenize the sentences
    encoding = tokenizer(text, return_tensors='pt')
    input_ids = encoding['input_ids']

    attention_mask = encoding['attention_mask']

    # move to GPU if necessary
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

    AnswerLabel=[]
    HaveAnswer=0

    for i in range(len(prediction[0])):
        if prediction[0][i]==1:
            HaveAnswer=1
            AnswerLabel.append(text)

    if HaveAnswer==0:
        AnswerLabel.append("No Answer")

    Prediction=[]
    for i in range(len(prediction[0])):
        Prediction.append(int(prediction.tolist()[0][i]))

    return Prediction,AnswerLabel
