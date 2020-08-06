# coding: utf-8
'''

'''
import random
import pickle

random.seed(1234)

with open('../raw_data/remap.pkl', 'rb') as f:
  reviews_df = pickle.load(f)
  cate_list = pickle.load(f)
  user_count, item_count, cate_count, example_count = pickle.load(f)

train_set = []
test_set = []

# 都是按照人、时间升序排列的
for reviewerID, hist in reviews_df.groupby('reviewerID'):
#   print(hist)
#   user历史上的产品是正样本
  pos_list = hist['asin'].tolist()
  neg_list = [random.randint(0, item_count-1) for i in range(len(pos_list))]

#   之前的是过去的，中间某有个是candidate item，过去的都是行为序列
  for i in range(1, len(pos_list)):
    hist_asin = pos_list[:i]
    if i != len(pos_list) - 1:
      train_set.append((reviewerID, hist_asin, pos_list[i], 1))
      train_set.append((reviewerID, hist_asin, neg_list[i], 0))
    else:
#       每个人一条样本做测试，格式跟train_set的还不一样。形如 (1, [41862, 46010, 54171, 56540, 58134], (62555, 2288))
      label = (pos_list[i], neg_list[i])
      test_set.append((reviewerID, hist_asin, label))

random.shuffle(train_set)
random.shuffle(test_set)

assert len(test_set) == user_count
# assert(len(test_set) + len(train_set) // 2 == reviews_df.shape[0])

with open('dataset.pkl', 'wb') as f:
  pickle.dump(train_set, f, pickle.HIGHEST_PROTOCOL)
  pickle.dump(test_set, f, pickle.HIGHEST_PROTOCOL)

  # 下面这两个，拿出来没用，又赛道另外一个文件里了
  pickle.dump(cate_list, f, pickle.HIGHEST_PROTOCOL)
  pickle.dump((user_count, item_count, cate_count), f, pickle.HIGHEST_PROTOCOL)