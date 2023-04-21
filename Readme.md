## Install Packages

```bash
pip3 install flair
```
```bash
pip3 install seqeval
```

## Dataset
Once our paper get published, we will release our prepared dataset and as well as it's corresponding required source code.

## Training
Run the following script to train the model.

```bash
python3 train.py --dataset_path data\
--data_train train.txt\
--data_test test.txt\
--data_dev valid.txt\
--output_dir model\
--model_name_or_path allenai/scibert_scivocab_cased\
--layers -1\
--subtoken_pooling first_last\
--hidden_size 256\
--learning_rate 5e-05\
--use_crf True
```

## Inferencing
Run the following script to test the best model. "Use_fg_model" argment will be true when fingrained model will be tested only.

```bash
python3 test.py --dataset_path data \
--data_train train.txt\
--data_test test.txt\
--data_dev valid.txt\
--load_trainedm_dir model/best-model.pt\
--pred_txt_fl prediction.txt\
--label_dict dict_nw.pkl\
--result_file result.txt\
--use_fg_model True\
--model_name_or_path allenai/scibert_scivocab_cased
