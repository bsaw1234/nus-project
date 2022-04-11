


#from surprise import BaselineOnly
from surprise import KNNBasic
from surprise import KNNWithMeans
from surprise import Dataset
from surprise import accuracy
from surprise import Reader
from surprise.model_selection import train_test_split
from surprise.model_selection import cross_validate

import numpy as np
import pandas as pd

from google.colab import drive
drive.mount('/content/drive')

client = ''
profile = ''
inv_amt = ''
inv_period = ''

#*********************
pfolio_file = "/content/drive/My Drive/pfolio2.csv"
pfolio_df_read = pd.read_csv(pfolio_file)
df_ss = pd.read_csv('/content/drive/My Drive/pfolio2.csvstock_sentiment.csv')
df_stock = pd.read_csv('/content/drive/My Drive/stock.csv')
df_client = pd.read_csv('/content/drive/My Drive/client.csv')

pfolio_df_read
pfolio_df= pd.DataFrame(data=pfolio_df_read, columns=['Client','Product','rating'])
pfolio_df 
#*********************

#*********************
reader2 = Reader(rating_scale=(1,5)) # assumes data contains: user, item, ratings (in this order)
data2 = Dataset.load_from_df(pfolio_df, reader2)
#*********************

#*********************
pfolio_df 
#*********************

#*********************
# build a model using user-based or item-based CF
trainset2 = data2.build_full_trainset()  # use all data (ie no train/test split)

# select the model type, below are some examples, you can adjust the parmeters if you wish
#algo = BaselineOnly() # computes baselines for all users and items
#algo = KNNBasic() # default method = User-based CF, default similarity is MSD (euclidean), default k=40
algo2 = KNNBasic(k=40,sim_options={'name': 'pearson'}) # User-based CF using pearson
#algo = KNNBasic(sim_options={'name': 'cosine', 'user_based': False}) # item-based CF using cosine
#algo = KNNWithMeans(k=40,sim_options={'name': 'pearson'}) 

algo2.fit(trainset2) # build the model
#*********************

#*********************
# predict ratings for a given target user and target item

#select a target user
rawuid2 = 'Sreekanth' 

# select an item (e.g. pick any one of the below)
rawiid2 = 'APPL' # was rated by 
#rawiid = 'NightListener' # was not rated by 
#rawiid = 'LadyinWater' # was not rated by 
#rawiid = 'JustMyLuck' # was not rated by 

# convert user and items names (raw ids) into indexes (inner ids)
# surprise jargon: raw ids are the user & item names as given in the datafile, they can be ints or strings
# inner ids are indexes into the sorted rawids
uid2 = trainset2.to_inner_uid(rawuid2)
iid2 = trainset2.to_inner_iid(rawiid2)

uid2,iid2
#*********************

#*********************
print("inner ids:","user=",uid2,"item=",iid2)

# if the actual rating is known it can be passed as an argument
realrating2 = dict(trainset2.ur[uid2])[iid2]; realrating2  # retrieve the real rating
pred2 = algo2.predict(rawuid2, rawiid2, r_ui = realrating2, verbose = True)
pred2
#*********************

#*********************
# if the actual rating is unknown then it can be omitted
pred2 = algo2.predict(rawuid2, rawiid2)
pred2 
#*********************

#*********************
# make rating predictions for ALL of the users in the dataset

# first get the unseen items for each user
unseen2 = trainset2.build_anti_testset() # get all ratings that are not in the trainset
print("num unseen=",len(unseen2))
#print("sample of unseen:",unseen[0:3]) # the rating shown is the global mean rating, the actual rating is unknown
unseen2
#*********************

#************************
# now make ratings predictions for each users for all of their unseen items - this may be slow for big datasets
predictions2 = algo2.test(unseen2)
print("num preds made=",len(predictions2))
predictions2
#************************

#************************
# to predict only the ratings for the target user on their unseen items (specfied earlier by rawuid)
# we extract the targetuser from unseen
# how do the predictions for Toby compare with the results in the earlier workshops?

targetonly2 = list()
for ruid, riid, r in unseen2:
    print(ruid,riid)
    if (ruid == rawuid2):
        targetonly2.append((ruid, riid, r))        
print("targetdata=",targetonly2)  
predictions2 = algo2.test(targetonly2)
predictions2
#************************

#************************
from collections import defaultdict

def get_top_n2(predictions2, n=10):
    # First map the predictions to each user.
    top_n2 = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions2:
        #print(uid,iid)
        top_n2[uid].append((iid, est))
    # Then sort the predictions for each user and retrieve the k highest ones.
    for uid, user_ratings in top_n2.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True) # sort on predicted rating
        top_n2[uid] = user_ratings[:n]
    return top_n2
#************************

#************************
# now get the actual recommended items for the target user (Toby) - the topN rated items
get_top_n2(predictions2)
top_dict=get_top_n2(predictions2)
top_dict
#************************

#top_df = pd.DataFrame([[k] + v[0] for k, v in top_dict.items()],columns=['client', 'symbol', 'rating'])
#top_df = pd.DataFrame([(k, v[0][0], v[0][1]) for k, v in top_dict.items()],columns=['client', 'symbol', 'rating'])
#top_df = pd.DataFrame([[k] + j for k,v in top_dict.items() for j in v], columns=['symbol', 'rating'])

top_df1 = pd.DataFrame(list(top_dict.items()), columns=['id', 'category'])
top_df2=top_df1['category']
#top_df = pd.DataFrame(top_df1, columns='category', index='id')
print(top_df2)

top_df3 = pd.DataFrame(list(top_df2[0]), columns=['symbol', 'rating'])
print(top_df3)


top_df3.to_csv('top_df.csv')

import csv as csv

with open('reco_op1.csv', 'w') as f:
    write = csv.writer(f) 
    write.writerows(top_df3)

df_ss

df_stock

df_client

#merged_data = pd.merge(top_df, df_stock,  how='left', left_on='[symbol]', right_on='[symbol]')
merged_data1 = top_df3.merge(df_stock, on=["symbol"])
merged_data2 = merged_data1.merge(df_ss,on=["symbol"])
#merged_data3 = merged_data2.merge(df_client, on=["client"])
merged_data2

merged_data3 = merged_data2.sort_values(['trend_rank','ss_rank'])
merged_data3

df_up_all_senti = merged_data3[merged_data3['trend']=='Up']
df_up_all_senti

df_up_all_senti.to_csv('reco_output_to_ui_from_green.csv',index=False)