import tensorflow as tf
from tensorflow import keras

class FullyConnectedTower(keras.layers.Layer):
    """
    若干个全连接层组成的塔
    """

    def __init__(self,
                 tower_units: list,
                 tower_name: str,
                 hidden_activation,
                 regularizer=keras.regularizers.L2(0.00001),
                 use_bn=True,
                 dropout=0.0,
                 output_activation=None,
                 seed=2023,
                 **kwargs):
        self.tower_units = tower_units
        self.hidden_activation = hidden_activation
        self.output_activation = output_activation
        self.regularizer = regularizer
        self.use_bn = use_bn
        self.tower_name = tower_name
        self.seed = seed
        self.dropout = dropout

        self.kernels = None
        self.biases = None
        self.activations = None
        if self.use_bn:
            self.batch_normalizations = None
        self.dropout_layers = None

        super(FullyConnectedTower, self).__init__(**kwargs)

    def build(self, input_shape): #(none, 50, 128)
        input_size = input_shape[-1]
        kernel_units = [int(input_size)] + list(self.tower_units)  # [128, 64, 32, 1]
        self.kernels = [self.add_weight(name=f"{self.tower_name}_kernel_{i}",
                                        shape=(kernel_units[i], kernel_units[i + 1]),
                                        initializer=keras.initializers.glorot_normal(seed=self.seed),
                                        regularizer=self.regularizer,
                                        trainable=True) for i in range(len(self.tower_units))]
        self.biases = [self.add_weight(name=f"{self.tower_name}_bias_{i}",
                                       shape=(self.tower_units[i],),
                                       initializer=keras.initializers.Zeros(),
                                       trainable=True) for i in range(len(self.tower_units))]
        if self.use_bn:
            self.batch_normalizations = [keras.layers.BatchNormalization() for i in range(len(self.tower_units))]

        self.activations = [_get_activation(self.hidden_activation) for _ in range(len(self.tower_units) - 1)] + \
                           [_get_activation(self.output_activation)]

        if self.dropout > 0.0:
            self.dropout_layers = [keras.layers.Dropout(self.dropout) for i in range(len(self.tower_units))]

        super(FullyConnectedTower, self).build(input_shape)

    def call(self, inputs, training=None, **kwargs):
        tower_input = inputs
        for i in range(len(self.tower_units)):
            cur = tf.nn.bias_add(tf.tensordot(tower_input, self.kernels[i], axes=(-1, 0)), self.biases[i])
            if self.use_bn:
                cur = self.batch_normalizations[i](cur, training=training)
            try:
                cur = self.activations[i](cur, training=training)
            except TypeError:
                if self.activations[i]:
                    cur = self.activations[i](cur)
            if self.dropout > 0.0:
                cur = self.dropout_layers[i](cur)
            tower_input = cur

        return tower_input


def din_attention_unit(tower_units, name):
    return FullyConnectedTower(tower_units=tower_units,
                               tower_name=name,
                               hidden_activation="Dice",
                               name=name + "_layer")

class TargetAttention(keras.layers.Layer):
    """
    -inputs: [query, keys]
        - query-shape: (batch_size, embedding_dim) or (batch_size, 1, embedding_dim)
        - keys-shape: (batch_size, seq_len, embedding_dim)
    - outputs: attention weights
        -shape: (batch_size, seq_len, 1)
    DIN 原文中在 att_unit 输出的权重后加了一层 softmax
    """

    def __init__(self, att_units, seq_len, embedding_dim, use_softmax=True, tower_name="", **kwargs):
        self.att_module = din_attention_unit(att_units, tower_name)
        self.seq_len = seq_len
        self.embedding_dim = embedding_dim
        self.use_softmax = use_softmax
        super(TargetAttention, self).__init__(**kwargs)

    @tf.autograph.experimental.do_not_convert
    def call(self, inputs, **kwargs): # inputs [(none, 32), (none, 50, 32)]
        query_dim = len(tf.keras.backend.int_shape(inputs[0]))
        if query_dim == 2:
            query = tf.reshape(inputs[0], shape=(-1, 1, self.embedding_dim))  #(none, 1, 32)
        else:
            assert query_dim == 3, "query shape 错误"
            query = inputs[0]
        queries = tf.tile(query, multiples=[1, self.seq_len, 1])  # (none, 50, 32)
        keys = inputs[1]  # (none, 50, 32)
        att_unit_input = tf.concat([queries, keys, queries - keys, queries * keys], axis=-1)  # [none, 50, 32 * 4]
        att_module_output = self.att_module(att_unit_input)
        if self.use_softmax:
            att_module_output = tf.squeeze(att_module_output, axis=-1)
            att_module_output = tf.nn.softmax(att_module_output)
            att_module_output = tf.expand_dims(att_module_output, axis=-1)
        return att_module_output  # (None, seq_len, 1)

def _get_activation(ac):
    activation = None
    if ac is None:
        pass
    if isinstance(ac, str):
        if ac == "Dice":
            activation = Dice()
        elif ac == "relu":
            activation = keras.activations.relu
        elif ac == "selu":
            activation = keras.activations.selu
        elif ac == "sigmoid":
            activation = keras.activations.sigmoid
        else:
            raise AttributeError("激活函数输入错误")
    elif isinstance(ac, type(keras.activations.softmax)) or isinstance(ac, type(tf.nn.sigmoid)):
        activation = ac
    return activation

class Dice(keras.layers.Layer):
    """
    DIN 用的激活函数
    """

    def __init__(self, axis=-1, epsilon=1e-9, **kwargs):
        self.axis = axis
        self.epsilon = epsilon
        self.batch_normalization = None
        self.alpha = None
        super(Dice, self).__init__(**kwargs)

    def build(self, input_shape):
        self.batch_normalization = keras.layers.BatchNormalization(axis=self.axis, epsilon=self.epsilon, center=False,
                                                                   scale=False)
        self.alpha = self.add_weight(shape=(input_shape[-1],), initializer=keras.initializers.Zeros(),
                                     dtype=tf.float32, name="Dice_alpha")
        super(Dice, self).build(input_shape)

    def call(self, inputs, training=None, **kwargs):
        inputs_normed = self.batch_normalization(inputs, training=training)
        x_p = tf.sigmoid(inputs_normed)
        return self.alpha * (1.0 - x_p) * inputs + x_p * inputs

