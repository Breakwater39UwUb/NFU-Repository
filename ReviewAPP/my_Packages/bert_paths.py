'''
Contains BERT paths
- pickle file
- vocabulary file
- multi-label model file
- multi-class model file
- config file

Other arguments
- classification number
- model name
- saved file directory
'''

pkl_file = 'trained_model/data_features.pkl'
vocab_file = 'trained_model/bert-base-chinese-vocab.txt'
multi_label_model = 'trained_model/model'
model_file = 'trained_model/model.safetensors'
config_file = 'trained_model/config.json'
ModelName = "trained_model"
ClassNum = 3

SAVEDIR = './SaveData/'