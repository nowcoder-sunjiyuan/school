import tensorflow as tf
from tensorflow import keras
import os
import json

data_path = "/home/web/sunjiyuan/data/essm/v1"

STRING_TYPE = 'string'
INT_TYPE = 'int64'
FLOAT_TYPE = 'float32'
TYPE_DICT = {STRING_TYPE: tf.string, INT_TYPE: tf.int64, FLOAT_TYPE: tf.float32}
## 所有的输入的特征
all_feature = json.load(open(f'../model_features/.json'))


## 加载文件
train_files, test_files = [], []
file_list = os.listdir(os.path.join(data_path, "/20240517"))
train_files += [os.path.join(data_path, "/2024051722", fn)
                for fn in file_list if fn > "2024051722"]

## _build_feature_description
feature_description = {}
for key, value in all_feature.items():
    feature_description[key] = tf.io.FixedLenFeature(shape=(value[1],), dtype=TYPE_DICT[value[0]])



def _read(files, feature_description, filter_fn, whether_train):
    params = {
        "filenames": [],
        "feature_description": feature_description,
        "batch_size": 1024,
        "shuffle": whether_train,
        "labels": ['label', 'cvr_label']
    }
    if filter_fn is not None:
        params["filter_fn"] = filter_fn
    if whether_train:
        params["use_weight"] = True
        params["weight_name"] = 'CES'
    if len(files) > 0:
        params["filenames"] = files
        dataset = read_tfrecord(**params)
    else:
        assert not whether_train, "训练数据不能为空"
        dataset = None
    return dataset

def read_tfrecord(
        filenames,
        feature_description,
        batch_size, shuffle,
        shuffle_buffer_size=2048,
        num_parallel_calls=8,
        prefetch_num=1,
        labels=tuple(),
        use_weight=False,
        weight_name=None,
        filter_fn=None
):
    def _parse_example(example_proto):
        features = tf.io.parse_single_example(example_proto, feature_description)
        _labels = []
        for label in labels:
            _labels.append(features.pop(label))
        if use_weight:
            if not weight_name:
                raise AttributeError('权重列的名称不能为空！')
            weight = features.pop(weight_name)
            return features, tuple(_labels), weight
        return features, tuple(_labels)

    def _input():
        dataset = tf.data.TFRecordDataset(filenames)
        if filter_fn:
            dataset = dataset.filter(filter_fn)
        dataset = dataset.map(_parse_example, num_parallel_calls=num_parallel_calls)
        if shuffle:
            dataset = dataset.shuffle(shuffle_buffer_size)
        dataset = dataset.batch(batch_size)
        if prefetch_num > 0:
            dataset = dataset.prefetch(buffer_size=batch_size * prefetch_num)
        return dataset

    return _input