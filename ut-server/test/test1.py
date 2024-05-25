import tensorflow as tf
from tensorflow import keras
from utils import nn_utils as nn

target_att_layer = nn.TargetAttention(
            att_units=[64, 32, 1],
            seq_len=50,
            embedding_dim=32,
            tower_name="entity_id_shared_attention"
        )
breakpoint()
query = keras.Input(shape=(32,))
all_seq_keys = keras.Input(shape=(50, 32))
att_weights = target_att_layer([query, all_seq_keys])
print(att_weights)