import numpy as np

class DataInput:
  def __init__(self, data, batch_size):
        self.batch_size = batch_size
        self.data = data

        # 一个epoch有多少个batch
        self.epoch_size = len(self.data) // self.batch_size
        # 呵呵，ceiling一下
        if self.epoch_size * self.batch_size < len(self.data):
            self.epoch_size += 1

        # 做什么用？第i batch
        self.i = 0

  def __iter__(self):
        return self

  def __next__(self):
        '''
         self.data里的，一个训练样本的4个组成部分：# reviewerID, hist_asin, candidate item, label
        :return: 批次，数据
            数据是一个元组，(reviewerID, candidate item id, label, hist_asin, hist_asin序列长度)
                元组里的元素除了hist_asin外，其它都是shape为(batch_size,)的一维数组；hist_asin是shape为（batch_size，44）的矩阵
        '''
        # i最大是epoch_size-1
        if self.i == self.epoch_size:
            raise StopIteration
        # 长度为32的list，每个元素，就是训练集里的元素，# reviewerID, hist_asin, candidate item, label
        ts = self.data[self.i * self.batch_size : min((self.i+1) * self.batch_size,
                                                      len(self.data))]
        self.i += 1

        # 这就是一个训练样本的4个组成部分
        # reviewerID, hist_asin, candidate item, label
        # u: reviewerID： 长度32的一维数组
        # i: candicate item：长度32的一维数组
        # y: label。shape: 长度32的一维数组
        # sl: 是历史序列的长度，sl应该是sequence length的意思
        u, i, y, sl = [], [], [], []
        for t in ts:
              u.append(t[0])
              i.append(t[2])
              y.append(t[3])
              sl.append(len(t[1]))
        # 最大44
        max_sl = max(sl)

        # shape：32*44
        hist_i = np.zeros([len(ts), max_sl], np.int64)

        # 为什么要这么搞啊？？？目的是啥呢？？？return一个这个，一个长度
        k = 0
        for t in ts:
            seq = t[1]
            for l in range(len(seq)):
                hist_i[k][l] = seq[l]
            k += 1

        # hist：shape是（32,44)的一个矩阵
        return self.i, (u, i, y, hist_i, sl)

class DataInputTest:
  def __init__(self, data, batch_size):

      self.batch_size = batch_size
      self.data = data
      self.epoch_size = len(self.data) // self.batch_size
      if self.epoch_size * self.batch_size < len(self.data):
          self.epoch_size += 1
      self.i = 0

  def __iter__(self):
      return self

  def __next__(self):

      if self.i == self.epoch_size:
        raise StopIteration

      ts = self.data[self.i * self.batch_size : min((self.i+1) * self.batch_size,
                                                    len(self.data))]
      self.i += 1

      u, i, j, sl = [], [], [], []
      for t in ts:
        u.append(t[0])
        i.append(t[2][0])
        j.append(t[2][1])
        sl.append(len(t[1]))
      max_sl = max(sl)

      hist_i = np.zeros([len(ts), max_sl], np.int64)

      k = 0
      for t in ts:
        for l in range(len(t[1])):
          hist_i[k][l] = t[1][l]
        k += 1

      return self.i, (u, i, j, hist_i, sl)

if __name__ == '__main__':
    train_set = [1,2,3,4,5,6,7,8,9,10]
    train_batch_size = 2
    my_intput = DataInput(train_set, train_batch_size)
    for item in my_intput:
        print(item)