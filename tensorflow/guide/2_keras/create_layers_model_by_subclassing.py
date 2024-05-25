import tensorflow as tf
from tensorflow import keras

## 强制 TensorFlow 在 eager 模式下运行函数
tf.config.run_functions_eagerly(True)

class Linear(keras.layers.Layer):
    def __init__(self, units=32):
        print("Linear __init__")
        super(Linear, self).__init__()
        self.units = units

    def build(self, input_shape):
        print("Linear __build__")
        self.w = self.add_weight(
            shape=(input_shape[-1], self.units),
            initializer="random_normal",
            trainable=True,
        )
        self.b = self.add_weight(
            shape=(self.units,), initializer="random_normal", trainable=True
        )

    def call(self, inputs):
        print("Linear call")
        return tf.matmul(inputs, self.w) + self.b

class MLPBlock(keras.layers.Layer):
    def __init__(self):
        print("MLPBlock __init__")
        super(MLPBlock, self).__init__()
        self.linear_1 = Linear(32)
        self.linear_2 = Linear(32)
        self.linear_3 = Linear(1)

    @tf.autograph.experimental.do_not_convert
    def call(self, inputs):
        print("MLPBlock call top")
        x = self.linear_1(inputs)
        x = tf.nn.relu(x)
        x = self.linear_2(x)
        x = tf.nn.relu(x)
        print("MLPBlock call end")
        return self.linear_3(x)


mlp = MLPBlock()
input = tf.keras.Input((64,))
mlp(input)
for weight in mlp.weights:
    print(weight.name, weight.shape)

