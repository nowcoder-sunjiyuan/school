import datetime
import os

now = datetime.datetime.now()
data_path = '/Users/nowcoder/data'
# 3 天前 ？
before_days = 3
train_files, test_files = [], []
start_time = now + datetime.timedelta(days=-before_days)
file_list = os.listdir(os.path.join(data_path, start_time.strftime("%Y%m%d")))
train_files += [os.path.join(data_path, start_time.strftime('%Y%m%d'), fn)
                for fn in file_list if fn > start_time.strftime('%Y%m%d%H')]
for i in range(before_days):
    cur = (start_time + datetime.timedelta(days=i + 1)).strftime('%Y%m%d')
    if not os.path.exists(os.path.join(data_path, cur)):
        continue
    file_list = os.listdir(os.path.join(data_path, cur))
    train_files += [os.path.join(data_path, cur, fn) for fn in file_list]
train_files.sort()

test_files = train_files[(before_days - 1) * 24:]
train_files = train_files[:(before_days - 1) * 24]

# self.train_files += train_files
# self.test_files += test_files
# logger.info(f"添加的文件数量：训练集 {len(train_files)} 测试集 {len(test_files)}")