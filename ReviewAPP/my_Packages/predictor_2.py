'''Multi-label classification

'''
# PyTorch
import torch
# import torch.nn as nn
# import torch.optim as optim
# from torch.utils.data import DataLoader
# from torch.utils.data.dataset import random_split
# import torch.utils.data as data

# BERT Related Libraries
from transformers import BertTokenizer, BertForSequenceClassification

# Python
import os, csv, json
from my_Packages.bert_paths import multi_label_model

def review_analyze(TEXT: list = [], file_path: str = None):
    '''BERT Predict Multi-labels
    
    TEXT: list of reviews
    file: path to review

    returns list of tuples
        >>> [(label: list[int], text: str, time: list[str])]

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
        # print(TEXT[0])

    Predictions = []

    # ML Parameters
    LabelNum = 4

    # hard code the label dimension to be 4 (because the data has 4 classes)
    num_labels = LabelNum

    # Define model
    global device
    set_device_by_platform()
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
    save_predictions(Predictions, file_path)
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

def set_device_by_platform():
    global device
    if torch.backends.mps.is_available():
        D = 'mps'
    elif torch.cuda.is_available():
        D = 'cuda'
    else:
        D = 'cpu'
    device = torch.device(D)
    print("using device",device)

def save_predictions(data: list, save_path: str):
    '''Save predictions to json file
    
    save_path: /SaveData/SHOPNAME/SHOPNAME.json
    '''

    save_path = save_path.split(os.path.sep)
    dir_ = os.path.sep.join(save_path[:-1])
    file = 'prediction_' + save_path[1] + '.json'
    save_path = os.path.sep.join([dir_, file])

    SAVES = [{'labels': row[0], 'content': row[1], 'time_range': row[2]} for row in data]

    with open(save_path, 'w', encoding='utf-8') as file:
        json.dump(SAVES, file, ensure_ascii=False, indent=4)