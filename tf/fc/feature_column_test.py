import tensorflow as tf
from tensorflow import feature_column


# 定义一个包含颜色分类特征的样本
color_data = {
    'color': [0, 1, 2, 2, 1, 0]
}

# 创建 categorical_column_with_identity 特征列
color_column = tf.feature_column.categorical_column_with_identity(key='color', num_buckets=3)

# 转换特征列为稀疏向量
indicator = tf.feature_column.indicator_column(color_column)

print(indicator)