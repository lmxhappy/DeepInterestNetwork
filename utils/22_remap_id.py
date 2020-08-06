#!/usr/bin/env python
# coding: utf-8

# In[30]:


# coding: utf-8

import random
import pickle
import numpy as np

random.seed(1234)

with open('../raw_data/reviews.pkl', 'rb') as f:
  reviews_df = pickle.load(f)
  reviews_df = reviews_df[['reviewerID', 'asin', 'unixReviewTime']]
    

with open('../raw_data/meta.pkl', 'rb') as f:
  meta_df = pickle.load(f)

  # 丢了大部分字段，只保留了两个字段
  meta_df = meta_df[['asin', 'categories']]


# In[32]:


# 这是什么操作呢？？？
meta_df2 = meta_df
meta_df2['categories'] = meta_df2['categories'].map(lambda x: x[-1][-1])


# In[34]:


def build_map(df, col_name):
  '''
  对df做修改——label encode；返回映射关系和key集合
  '''
  key = sorted(df[col_name].unique().tolist())
  # 这是做了labelEncode啊
  m = dict(zip(key, range(len(key))))
  df[col_name] = df[col_name].map(lambda x: m[x])
  return m, key

asin_map, asin_key = build_map(meta_df2, 'asin')
cate_map, cate_key = build_map(meta_df2, 'categories')
revi_map, revi_key = build_map(reviews_df, 'reviewerID')


# In[35]:


meta_df2


# In[37]:


user_count, item_count, cate_count, example_count =    len(revi_map), len(asin_map), len(cate_map), reviews_df.shape[0]
print('user_count: %d\titem_count: %d\tcate_count: %d\texample_count: %d' %
      (user_count, item_count, cate_count, example_count))


# In[38]:


# 根据产品的labelEncode进行排序，这样的目的是什么？
meta_df3 = meta_df2.sort_values('asin').reset_index(drop=True)


# In[41]:


reviews_df['asin'] = reviews_df['asin'].map(lambda x: asin_map[x])


# In[42]:


reviews_df2 = reviews_df


# In[43]:


# 也排序
reviews_df3 = reviews_df2.sort_values(['reviewerID', 'unixReviewTime'])                 .reset_index(drop=True)


# In[44]:


# 只保留了3个字段
reviews_df3 = reviews_df3[['reviewerID', 'asin', 'unixReviewTime']]


# In[45]:


reviews_df3


# In[48]:


meta_df3['categories']


# In[49]:


meta_df3['categories'].values


# In[50]:


# 这是什么操作呢？？？
# cate_list = [meta_df3['categories'][i] for i in range(len(asin_map))]
# cate_list = np.array(cate_list, dtype=np.int32)


# In[51]:


cate_arr = meta_df3['categories'].values


# In[20]:


# 存下来，下个环节用
with open('../raw_data/remap.pkl', 'wb') as f:
  pickle.dump(reviews_df, f, pickle.HIGHEST_PROTOCOL) # uid, iid
  pickle.dump(cate_arr, f, pickle.HIGHEST_PROTOCOL) # cid of iid line
  pickle.dump((user_count, item_count, cate_count, example_count),
              f, pickle.HIGHEST_PROTOCOL)
  pickle.dump((asin_key, cate_key, revi_key), f, pickle.HIGHEST_PROTOCOL)

