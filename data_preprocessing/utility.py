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
  
def get_conll_pwc_data(data,csv_writer,term2ner):
  wh_ent=[]
  wh_ent_temp=[]
  data_new=[]
  for i,j in enumerate(tqdm(data)):
    #print(i)
    ent_dict=[]
    ent_dict_new=[]
    data_new_temp={}
    sent_label=[0]*len(j['tokens'])
    #print(j['entities'])
    for k in j['entities']:
      if k['type'] in term2ner:
        #print(term2ner)
        tag=term2ner[k['type']]
        #print(tag)
        # count=count+1
        indx_list=list(range(k['start'],k['end']))
        ent_dict.append([k['type'],indx_list])
    wh_ent_temp.append(ent_dict)
    ent_dict_cp=ent_dict.copy()
    #print(wh_ent_temp)
    if len(ent_dict)>1:
      for x,y in itertools.combinations(ent_dict, 2):
        z=list(set(x[-1]).intersection(y[-1]))
        #print(z)
        if len(z)>0:
          try:
            if len(x[-1])>len(y[-1]):
              #print("Now",ent_dict_cp)
              ent_dict_cp.remove(y)
            else:
              #print("Now",ent_dict_cp)
              ent_dict_cp.remove(x)
          except:
            pass
      if len(ent_dict_new)==0:
        ent_dict_new.extend(ent_dict_cp)
      wh_ent.append(ent_dict_new)
    elif len(ent_dict)<=1:
      ent_dict_new.extend(ent_dict)
    for m,n in enumerate(ent_dict_new):
      if len(n[-1])>1:
        for p,q in enumerate(n[-1]):
          sent_temp=[]
          if p==0:
            sent_temp.append(j['tokens'][q])
            sent_temp.append('B')
            sent_label[q]=sent_temp
          elif p!=0:
            try:
              sent_temp.append(j['tokens'][q])
              sent_temp.append('I')
              sent_label[q]=sent_temp
            except:
              pass
      elif len(n[-1])==1:
        try:
          sent_temp=[]
          sent_temp.append(j['tokens'][n[-1][0]])
          sent_temp.append('B')
          sent_label[n[-1][0]]=sent_temp
        except:
          pass
    for r,s in enumerate(sent_label):
      if s==0:
        sent_label[r]=[j['tokens'][r],'O']
    for r,s in enumerate(sent_label):
      if r==0:
        s.insert(r,'Sentence: {}'.format(i+1))
      else:
        s.insert(0,None)
    csv_writer.writerows(sent_label)
  return 0
  
def get_scirc_data_format_fg(data):
  data_scirc_format=[]
  count=0
  for i,j in enumerate(tqdm(data)):
    temp_dict={}
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
      ent_tmp_dict['type']=mthd_names_dict[k]['method_type']
      ent_tmp_dict['name']=k
      temp_dict['entities'].append(ent_tmp_dict)
      new_txt_sp.remove('S_SOE')
      new_txt_sp.remove('E_SOE')
    temp_dict['tokens']=new_txt_sp
    #print(new_txt_sp)
    data_scirc_format.append(temp_dict)
  return data_scirc_format

def get_conll_pwc_data_fg(data,csv_writer,term2ner):
  wh_ent=[]
  wh_ent_temp=[]
  data_new=[]
  for i,j in enumerate(tqdm(data)):
    #print(i)
    ent_dict=[]
    ent_dict_new=[]
    data_new_temp={}
    sent_label=[0]*len(j['tokens'])
    #print(j['entities'])
    for k in j['entities']:
      if k['type'] in term2ner:
        tag=term2ner[k['type']]
        #print(tag)
        # count=count+1
        indx_list=list(range(k['start'],k['end']))
        ent_dict.append([k['type'],indx_list])
    wh_ent_temp.append(ent_dict)
    ent_dict_cp=ent_dict.copy()
    #print(wh_ent_temp)
    if len(ent_dict)>1:
      for x,y in itertools.combinations(ent_dict, 2):
        z=list(set(x[-1]).intersection(y[-1]))
        #print(z)
        if len(z)>0:
          try:
            if len(x[-1])>len(y[-1]):
              #print("Now",ent_dict_cp)
              ent_dict_cp.remove(y)
            else:
              #print("Now",ent_dict_cp)
              ent_dict_cp.remove(x)
          except:
            pass
      if len(ent_dict_new)==0:
        ent_dict_new.extend(ent_dict_cp)
      wh_ent.append(ent_dict_new)
    elif len(ent_dict)<=1:
      ent_dict_new.extend(ent_dict)
    for m,n in enumerate(ent_dict_new):
      if len(n[-1])>1:
        for p,q in enumerate(n[-1]):
          sent_temp=[]
          if p==0:
            sent_temp.append(j['tokens'][q])
            sent_temp.append('B-{}'.format(n[0]))
            sent_label[q]=sent_temp
          elif p!=0:
            try:
              sent_temp.append(j['tokens'][q])
              sent_temp.append('I-{}'.format(n[0]))
              sent_label[q]=sent_temp
            except:
              pass
      elif len(n[-1])==1:
        try:
          sent_temp=[]
          sent_temp.append(j['tokens'][n[-1][0]])
          sent_temp.append('B-{}'.format(n[0]))
          sent_label[n[-1][0]]=sent_temp
        except:
          pass
    for r,s in enumerate(sent_label):
      if s==0:
        sent_label[r]=[j['tokens'][r],'O']
    for r,s in enumerate(sent_label):
      if r==0:
        s.insert(r,'Sentence: {}'.format(i+1))
      else:
        s.insert(0,None)
    csv_writer.writerows(sent_label)
  return 0