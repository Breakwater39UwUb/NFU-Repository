# multiclass classification, which filter garbage reviews

import torch
import pickle
from core import to_bert_ids, use_model
from Packages import bert_paths

def review_predict(q_inputs: list):
    '''Returns original review and prediction
    q_inputs: list of strings

    returns list of prediction
    '''

    # load and init
    pkl_file = open(bert_paths.pkl_file, 'rb')
    data_features = pickle.load(pkl_file)
    answer_dic = data_features['answer_dic']
        
    # BERT
    model_setting = {
        "model_name":"bert", 
        "config_file_path":"trained_model/config.json", 
        "model_file_path":"trained_model/pytorch_model.bin", 
        "vocab_file_path":bert_paths.vocab_file,
        "num_labels":5  # 分幾類
    }    

    # ALBERT
    # model_setting = {
    #     "model_name":"albert", 
    #     "config_file_path":"trained_model/config.json", 
    #     "model_file_path":"trained_model/pytorch_model.bin", 
    #     "vocab_file_path":"albert/albert_tiny/vocab.txt",
    #     "num_labels":149 # 分幾類
    # }
    
    #
    model, tokenizer = use_model(**model_setting)
    model.eval()

    #
    ans_label = []
    for q_input in q_inputs:
        bert_ids = to_bert_ids(tokenizer,q_input)
        assert len(bert_ids) <= 512
        input_ids = torch.LongTensor(bert_ids).unsqueeze(0)

        # predict
        outputs = model(input_ids)
        predicts = outputs[:2]
        predicts = predicts[0]
        max_val = torch.max(predicts)
        label = (predicts == max_val).nonzero().numpy()[0][1]
        ans_label.append(answer_dic.to_text(label))
        
    if len(ans_label) == 1:
        return ans_label[0]
    
    return ans_label

