import sys
f=open(sys.argv[1],'r')
import math
import os

stop_words=['i', 'me', 'my', 'myself','one','we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'do', 'should', 'now']

re_ex=['!','@',';','$','%','^','&','*','(',')','-','_','+','=','{','}','[',']','|','\','<','>',''','"','?']
count=0
list=[]
data=[]

for i in f:
    if '<answer instance=' in i:
        k=i.split('"')
        list.append(k[1])
        list.append(k[3])
    elif '<context>' in i:
        count=1
    elif count==1:
        text= i
        list.append(i)
        count=0
    else:
        pass
    if len(list)==3:
        data.append((list[0],list[1],list[2]))
        list=[]
    else:
        continue


n=len(data)
fold=5
f_length=int(round(len(data)/fold))
count=1
data_fold=[]
for i in range(0,n,f_length):
    if i+f_length<n:
        data_fold.append(data[i:i+f_length])
    else:
        data_fold.append(data[i:n])


comp_data=[] # [(test_data,train_data),(test_data,train_data)]

for i in range(0,fold):
    train_data=[]
    test_data=data_fold[i]
    for j in range(0,fold):
        if j!=i:
            train_data=train_data+data_fold[j]
        else:
            continue
    comp_data.append((test_data,train_data))


def sense_extraction(data):
    traversed=[]
    feature_list=[]
    n=len(data)
    for i in range(0,n):
        if data[i][1] not in traversed:
            feature_list.append(data[i][1])
            traversed.append(data[i][1])
        else:
            continue
    return feature_list


def target_word(train_data):
    target=train_data[0][1]
    target=target.split('%')
    target_text=target[0]
    target_text='<head>'+str(target_text)+'</head>'
    return target_text

def cleaning(word):
    text=''
    for i in word:
        if i.isalpha():
            text=text+i
        else:
            continue
    return text

def feature_extraction(text,target_word_):
    split_t=text.split()
    word_list_=[]
    for i in split_t:
        i=i.lower()
        k=str(i)
        if str(i) not in word_list_:
            if ((i not in stop_words) and (i not in re_ex) and (i not in target_word_)):
                word_=cleaning(i)
                if word_ not in '':
                    word_list_.append(word_)
                else:
                    continue
            else:
                 continue
        else:
            continue
    return word_list_



def feature_dict(train_data,target_word_):
    n=len(train_data)
    feature_dict_={}
    for i in range(0,n):
        feature=train_data[i][1]
        if  feature in feature_dict_.keys():
            text=train_data[i][2]
            word_list_=feature_extraction(text,target_word_)
            for k in word_list_:
                if k in feature_dict_[feature].keys():
                    feature_dict_[feature][k]=feature_dict_[feature][k]+1
                else:
                    feature_dict_[feature][k]=1
        else:
            feature_dict_[feature]={}
    return feature_dict_


def sense_count_(train_data):
    n=len(train_data)
    sense_count={}
    for i in train_data:
        if i[1] in sense_count.keys():
            sense_count[i[1]]=sense_count[i[1]]+1
        else:
            sense_count[i[1]]=1
    return sense_count


def score(word_list_,feature_dict_,sense,sense_count,m):
    score=0
    for i in word_list_:
        if i in feature_dict_[sense].keys():
            p_f_s=(feature_dict_[sense][i]+1)/(sense_count[sense]+1)
            p_s=sense_count[sense]/m
            prob=math.log(p_f_s*p_s)
        else:
            p_f_s=(1)/(sense_count[sense]+1)  #vocab)
            p_s=sense_count[sense]/m
            prob=math.log(p_f_s*p_s)
        score=score+prob
    return score




def max_score_key(dict):
    for i in dict.keys():
        max_key=i
        break
    for i in dict.keys():
        if dict[i]>dict[max_key]:
            max_key=i
        else:
            continue
    return max_key


def naive_bayes_wsd(train_data,test_data):
    target_word_=target_word(train_data)
    feature_dict_=feature_dict(train_data,target_word_)
    actual_data=[]
    predicted_data=[]
    n=len(test_data)
    sense_count=sense_count_(train_data)
    m=len(train_data)
    for i in range(0,n):
        text=test_data[i][2]
        word_list_=feature_extraction(text,target_word_)
        prob={}
        for j in feature_dict_.keys():
            sense=j
            prob[j]=score(word_list_,feature_dict_,sense,sense_count,m)
        max_key=max_score_key(prob)
        actual_data.append((test_data[i][0],test_data[i][1]))
        predicted_data.append((test_data[i][0],max_key))

    return actual_data,predicted_data


def accuracy(actual_label,predicted_label):
    n=len(actual_data)
    count=0
    error_text=[]
    for i in range(0,n):
        if actual_label[i][1]==predicted_label[i][1]:
            count=count+1
        else:
            continue
    accuracy_=count/n

    return accuracy_

sum=0
n=len(comp_data)
acc=[]


file_name=str(sys.argv[1])+'.out'
if os.path.exists(file_name):
  os.remove(file_name)

f=open(file_name,'x')

for i in range(0,n):
    test_data=comp_data[i][0]
    train_data=comp_data[i][1]
    actual_data,predicted_data=naive_bayes_wsd(train_data,test_data)
    accuracy_=accuracy(actual_data,predicted_data)
    key_text='Fold_'+str(i+1)+'_Accuracy:'
    acc.append((key_text,accuracy_))
    sum=sum+accuracy_
    fold_text='Fold '+str(i+1)+'\n'
    f.write(fold_text)
    for j in range(0,len(predicted_data)):
        text=predicted_data[j][0]+' '+predicted_data[j][1]+'\n'
        f.write(text)

print('Accuracy for the '+str(sys.argv[1])+' dataset:')
for i in range(0,len(acc)):
    print(acc[i][0],round(acc[i][1]*100.0,2),'%')
print('Average_Accuracy:',round(100*sum/n,2),'%')
