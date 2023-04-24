import argparse
import json
import pickle as pkl
from tqdm import tqdm
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import glob
from collections import OrderedDict
from nltk.tokenize.treebank import TreebankWordDetokenizer
import requests
import re
import os
import nltk
#nltk.download("all")
from nltk.tokenize import sent_tokenize,word_tokenize
import re
import csv
import itertools
import pandas as pd
from multiprocessing import Pool
from tqdm import tqdm
from functools import partial
from sklearn.model_selection import train_test_split
import copy
from utility import *

paper_section=['related work','related works','conclusion','conclusions','future work','future works', 'acknowledgments','acknowledgment','background','previous work','previous works','corresponding authors','equal contribution','*ethics / impact statement',
 '*indicates equal contribution','*indicates equal contributions.','dwh1rlvh 0hdvxuhphqw1rlvh','*co-first author']
words_list=["et al.", "no.", "co.", "ltd.",". . .","et al"]

def get_scirc_data_format(data):
  data_scirc_format=[]
  count=0
  for i,j in enumerate(tqdm(data)):
    temp_dict=OrderedDict()
    temp_dict['entities']=[]
    method_name_temp=set(data[j])
    method_name_tmp_ls=list(method_name_temp)
    for k in method_name_tmp_ls:
      new_txt=j
      ent_tmp_dict={}
      tok_pos=re.search(k,new_txt)
      new_txt=new_txt[:tok_pos.start()] +" "+"S_SOE"+" "+new_txt[tok_pos.start():tok_pos.end()]+" "+"E_SOE"+" "+new_txt[tok_pos.end():]
      new_txt_sp=word_tokenize(new_txt)
      #print(new_txt_sp)
      for x,y in enumerate(new_txt_sp):
        if y == 'S_SOE' and count == 0:
          #print(x)
          ent_tmp_dict['start']=x
          count+=1
        if y=='E_SOE' and count == 1:
          ent_tmp_dict['end']=x-1
          count=0
      ent_tmp_dict['type']='method'
      ent_tmp_dict['name']=k
      temp_dict['entities'].append(ent_tmp_dict)
      new_txt_sp.remove('S_SOE')
      new_txt_sp.remove('E_SOE')
    temp_dict['tokens']=new_txt_sp
    #print(new_txt_sp)
    data_scirc_format.append(temp_dict)
  return data_scirc_format


def main(args):
  dataset = args.dataset
  mthd_path=args.methd_path
  first_path=args.first_path
  nt_req_mthds=args.not_req_mthds
  cg=args.cg
  train_csv=args.train_csv
  valid_csv=args.valid_csv
  test_csv=args.test_csv

  train_txt=args.train_txt
  valid_txt=args.valid_txt
  test_txt=args.test_txt
  mthd_names_dict=pkl.load(open(mthd_path,"rb"))
  print(len(mthd_names_dict))
  sent_dict_f=pkl.load(open(first_path,"rb"))
  sent_dict_paths=glob.glob(dataset+"*.pkl")

  for i in tqdm(sent_dict_paths):
    if i == first_path:
      continue
    elif i != first_path:
      sent_dict_tmp=pkl.load(open(i,"rb"))
      for j in sent_dict_tmp:
        if j in sent_dict_f:
          sent_dict_f[j].extend(sent_dict_tmp[j])
          #count_1=count_1+1
        elif j not in sent_dict_f:
          sent_dict_f[j]=sent_dict_tmp[j]
          #count_2=count_2+1

  sent_dict_final=OrderedDict()
  for i in tqdm(sent_dict_f):
    sent_dict_final[i]=list(set(sent_dict_f[i]))

  nt_rq_mthd_ls=[]
  not_req_mthd=open(nt_req_mthds,"r")
  not_req_mthd_ls=not_req_mthd.readlines()
  for i in not_req_mthd_ls:
    nt_rq_mthd_ls.append(i.strip())

  sent_dict_final_cp=copy.deepcopy(sent_dict_final)

  for i in tqdm(sent_dict_final_cp):
    if len(sent_dict_final[i])==1:
      if sent_dict_final[i][0] in nt_rq_mthd_ls:
        del sent_dict_final[i]
    elif len(sent_dict_final[i])>1:
      for j in sent_dict_final[i]:
        if j in nt_rq_mthd_ls:
          sent_dict_final[i].remove(j)
      if len(sent_dict_final[i])==0:
        del sent_dict_final[i]

  #print(len(sent_dict_final))
  indomain=OrderedDict()
  outdomain=OrderedDict()
  outdomain_strict=OrderedDict()
  yr=2017
  for i in tqdm(sent_dict_final):
    flag_in=0
    flag_out=0
    if len(sent_dict_final[i])==1:
      if int(mthd_names_dict[sent_dict_final[i][0]]['intro_yr']) <=yr:
        indomain[i]=sent_dict_final[i]
      elif int(mthd_names_dict[sent_dict_final[i][0]]['intro_yr'])>yr:
        outdomain[i]=sent_dict_final[i]
    elif len(sent_dict_final[i])>1:
      for j in sent_dict_final[i]:
        if int(mthd_names_dict[j]['intro_yr'])<=yr:
          flag_in=flag_in+1
        elif int(mthd_names_dict[j]['intro_yr'])>yr:
          flag_out=flag_out+1
      if flag_in>0 and flag_out==0:
        indomain[i]=sent_dict_final[i]
      else:
        outdomain[i]=sent_dict_final[i]
        if flag_in==0 and flag_out>0:
          outdomain_strict[i]=sent_dict_final[i]

  print(len(indomain))
  print(len(outdomain))
  indomain_data=get_scirc_data_format(indomain)
  outdomain_data=get_scirc_data_format(outdomain)
  indomain_data_train, indomain_data_test = train_test_split(indomain_data, test_size=0.33, random_state=42)

  fl_1=open(train_csv,"w")
  csv_writer_1=csv.writer(fl_1)
  fl_2=open(valid_csv,"w")
  csv_writer_2=csv.writer(fl_2)
  fl_3=open(test_csv,"w")
  csv_writer_3=csv.writer(fl_3)
  column_=["Sentence #","Word","Tag"]
  csv_writer_1.writerow(column_)
  csv_writer_2.writerow(column_)
  csv_writer_3.writerow(column_)

  if cg==True:
      term2ner_new={"method":'METHOD'}
      a=get_conll_pwc_data(indomain_data_train,csv_writer_1,term2ner_new)
      b=get_conll_pwc_data(indomain_data_test,csv_writer_2,term2ner_new)
      c=get_conll_pwc_data(outdomain_data,csv_writer_3,term2ner_new)
  elif cg==False:
      term2ner_new={'GEN':'GEN','CV':'CV','SEQ':'SEQ','RL':'RL','NLP':'NLP','AUDIO':'AUDIO','GRAPH':'GRAPH'}
      a=get_conll_pwc_data(indomain_data_train,csv_writer_1,term2ner_new)
      b=get_conll_pwc_data(indomain_data_test,csv_writer_2,term2ner_new)
      c=get_conll_pwc_data(outdomain_data,csv_writer_3,term2ner_new)
  fl_1.close()
  fl_2.close()
  fl_3.close()
  data_train_=pd.read_csv(train_csv)
  data_valid_=pd.read_csv(valid_csv)
  data_test_=pd.read_csv(test_csv)
  fl_=open(train_txt, 'w')
  tsvout_ = csv.writer(fl_, delimiter='\t')
  fl__=open(valid_txt, 'w')
  tsvout__ = csv.writer(fl__, delimiter='\t')
  fl___=open(test_txt, 'w')
  tsvout___ = csv.writer(fl___, delimiter='\t')
  for i in range(data_train_.shape[0]):
    tsvout_.writerow(data_train_.iloc[i].tolist())
  fl_.close()
  for i in range(data_valid_.shape[0]):
    tsvout__.writerow(data_valid_.iloc[i].tolist())
  fl__.close()
  for i in range(data_test_.shape[0]):
    tsvout___.writerow(data_valid_.iloc[i].tolist())
  fl__.close()



if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Creation of dataset")
	parser.add_argument("--dataset",type=str,default='',help="Path Should be given.")
	parser.add_argument("--first_path",type=str, default='', help='Path Should be given.')
	parser.add_argument("--methd_path",type=str,default='',help="Path Should be given.")
	parser.add_argument("--cg",type=bool,default='',help="Path Should be given.")
	parser.add_argument("--not_req_mthds",type=str,default='',help="Path Should be given.")
	parser.add_argument("--train_csv",type=str,default='',help="Path Should be given.")
	parser.add_argument("--valid_csv",type=str,default='',help="Path Should be given.")
	parser.add_argument("--test_csv",type=str,default='',help="Path Should be given.")
	parser.add_argument("--train_txt",type=str,default='',help="Path Should be given.")
	parser.add_argument("--valid_txt",type=str,default='',help="Path Should be given.")
	parser.add_argument("--test_txt",type=str,default='',help="Path Should be given.")
	args = parser.parse_args()
	#print(args)
	main(args)
