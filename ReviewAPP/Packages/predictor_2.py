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
import time

PATH = 'trained_model/model'

def predict_multiclass(TEXT: list):
    '''Predict Multiclass
    TEXT: list of reviews
    '''
    # ML Parameters
    LabelNum = 4
    D = 'cuda'

    device = torch.device(D)
    print("using device",device)

    # hard code the label dimension to be 6 (because the data has 6 classes)
    num_labels = LabelNum

    # Define model
    model = BertForSequenceClassification.from_pretrained('bert-base-chinese', num_labels=LabelNum)
    model.to(device)

    # Define tokenizer
    tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')

    model.load_state_dict(torch.load(PATH))

    for i in range(len(TEXT)):
        Answer=Predict(model, TEXT[i], device, D, tokenizer)
        print(Answer)

def Predict(model, text , device, D, tokenizer):
    device = torch.device(D)
    model.eval()     # Enter Evaluation Mode
    # tokenize the sentences
    print(text)
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
    print(prediction)        
    prediction[prediction > THRESHOLD] = 1
    prediction[prediction <= THRESHOLD] = 0
            
    
    # print completed result
    
    return prediction[0]
