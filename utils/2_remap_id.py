# coding: utf-8
'''

code一下
'''
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

  # 这是categories本来有多个，demo：[['Electronics', 'GPS & Navigation', 'Vehicle GPS', 'Trucking GPS']]
  # 现在只取其中的'Trucking GPS'
  meta_df['categories'] = meta_df['categories'].map(lambda x: x[-1][-1])

def build_map(df, col_name):
  '''
  对df做修改；返回映射关系和key集合
  '''
  key = sorted(df[col_name].unique().tolist())
  # 这是做了labelEncode啊
  m = dict(zip(key, range(len(key))))
  df[col_name] = df[col_name].map(lambda x: m[x])
  return m, key

asin_map, asin_key = build_map(meta_df, 'asin')
cate_map, cate_key = build_map(meta_df, 'categories')
revi_map, revi_key = build_map(reviews_df, 'reviewerID')

user_count, item_count, cate_count, example_count =\
    len(revi_map), len(asin_map), len(cate_map), reviews_df.shape[0]
print('user_count: %d\titem_count: %d\tcate_count: %d\texample_count: %d' %
      (user_count, item_count, cate_count, example_count))

# 根据产品的labelEncode进行排序，这样的目的是什么？
meta_df = meta_df.sort_values('asin')
meta_df = meta_df.reset_index(drop=True)

# 转成 label code
reviews_df['asin'] = reviews_df['asin'].map(lambda x: asin_map[x])
# 也排序
reviews_df = reviews_df.sort_values(['reviewerID', 'unixReviewTime'])
reviews_df = reviews_df.reset_index(drop=True)
# 只保留了3个字段
reviews_df = reviews_df[['reviewerID', 'asin', 'unixReviewTime']]

# 这是什么操作呢？？？
# cate_list = [meta_df['categories'][i] for i in range(len(asin_map))]
# cate_list = np.array(cate_list, dtype=np.int32)
cate_arr = meta_df3['categories'].values

# 存下来，下个环节用
with open('../raw_data/remap.pkl', 'wb') as f:
  pickle.dump(reviews_df, f, pickle.HIGHEST_PROTOCOL) # uid, iid
  pickle.dump(cate_arr, f, pickle.HIGHEST_PROTOCOL) # cid of iid line
  pickle.dump((user_count, item_count, cate_count, example_count),
              f, pickle.HIGHEST_PROTOCOL)
  pickle.dump((asin_key, cate_key, revi_key), f, pickle.HIGHEST_PROTOCOL)
