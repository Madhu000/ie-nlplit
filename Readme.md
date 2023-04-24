## Install Packages

```bash
pip3 install flair
```
```bash
pip3 install seqeval
```

## Dataset
To reproduce our results on Best performing model In ``LFGB" you can download the dataset from this link [Link](https://drive.google.com/drive/folders/1oX6c6Xzj6EWIxP_QgUCfcKhHFOk-0Ir0?usp=sharing)

To prepare the other dataset just download all the files present in this folder and unzip the zip file. Then run the following 

```bash
python3 data_prep.py --dataset="/sentence_dict/"\
--first_path="sentence_mthd_1.pkl"\
--methd_path="method_final.pkl"\
--cg=False\
--not_req_mthds="not_rq_ent.txt"\
--train_csv="method_train.csv"\
--valid_csv="method_valid.csv"\
--test_csv="method_test.csv"\
--train_txt="Output_dir/train.txt"\
--valid_txt="Output_dir/valid.txt"\
--test_txt="Output_dir/test.txt"
```

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
