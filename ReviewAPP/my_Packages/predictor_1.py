# multiclass classification, which filter garbage reviews

import torch
import pickle
from core import to_bert_ids, use_model
from my_Packages import bert_paths

global device 
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

def init_multi_class_model():

    # load and init
    pkl_file = open(bert_paths.pkl_file, 'rb')
    data_features = pickle.load(pkl_file)
    answer_dic = data_features['answer_dic']
        
    # BERT
    model_setting = {
        "model_name":"bert",
        "config_file_path":bert_paths.config_file,
        "model_file_path":bert_paths.model_file,
        "vocab_file_path":bert_paths.vocab_file,
        "num_labels":bert_paths.ClassNum  # 分幾類
    }

    # ALBERT
    # model_setting = {
    #     "model_name":"albert", 
    #     "config_file_path":"trained_model/config.json", 
    #     "model_file_path":"trained_model/pytorch_model.bin", 
    #     "vocab_file_path":"albert/albert_tiny/vocab.txt",
    #     "num_labels":149 # 分幾類
    # }
    
    global model, tokenizer
    model, tokenizer = use_model(**model_setting)
    model.to(device)
    model.eval()

def review_predict(q_input: str):
    '''Returns review prediction
    
    Parameters
    q_input: string
        Review string, length less than 512.
        String greater than 512 will cut
        sub string the first 512 characters

    Returns
    prediction: string
        number in range (0, class-1)
    '''
    # Unknown block
    # ans_label = []
    # for q_input in q_inputs:
    #     bert_ids = to_bert_ids(tokenizer,q_input)
    #     assert len(bert_ids) <= 512
    #     input_ids = torch.LongTensor(bert_ids).unsqueeze(0)

    #     # predict
    #     outputs = model(input_ids)
    #     predicts = outputs[:2]
    #     predicts = predicts[0]
    #     max_val = torch.max(predicts)
    #     label = (predicts == max_val).nonzero().numpy()[0][1]
    #     ans_label.append(answer_dic.to_text(label))
        
    # if len(ans_label) == 1:
    #     return ans_label[0]
    
    # return ans_label
    
    encoding = tokenizer(q_input, return_tensors='pt', padding=True, truncation=True, max_length=512)
    input_ids = encoding['input_ids']
    attention_mask = encoding['attention_mask']

    # move to GPU if necessary
    input_ids = input_ids.to(device)
    attention_mask = attention_mask.to(device)

    # generate prediction
    outputs = model(input_ids, attention_mask=attention_mask)
    #print(outputs)

    # use Softmax to convert to probability
    logits = outputs[0]
    prob = torch.softmax(logits, dim=1)

    # take the index of the highest prob as prediction output
    prediction = prob.max(1)[1]
    prediction = str(prediction.tolist()[0])
    # print(prediction)
    #prediction = prediction.split("tensor([")[1].split("],")[0]
    
    return(prediction)

init_multi_class_model()