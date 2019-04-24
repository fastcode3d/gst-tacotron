import numpy as np
import tensorflow as tf
from tensorflow.contrib.rnn import RNNCell
from .modules import prenet
from hparams import hparams as hp
class FrameProjection:
    """Projection layer to r * num_mels dimensions or num_mels dimensions
    """

    def __init__(self, shape=hp.num_mels, activation=None, scope=None):
        """
        Args:
          shape: integer, dimensionality of output space (r*n_mels for decoder or n_mels for postnet)
          activation: callable, activation function
          scope: FrameProjection scope.
        """
        super(FrameProjection, self).__init__()

        self.shape = shape
        self.activation = activation
        self.scope = 'linear_projection' if scope is None else scope
        self.dense = tf.layers.Dense(units=shape, activation=activation, name='projection_{}'.format(self.scope))

    def __call__(self, inputs):
        with tf.variable_scope(self.scope):
            # If activation==None, this returns a simple Linear projection
            # else the projection will be passed through an activation function
            # output = tf.layers.dense(inputs, units=self.shape, activation=self.activation,
            # name='projection_{}'.format(self.scope))
            return self.dense(inputs)
class DecoderPrenetWrapper(RNNCell):
  '''Runs RNN inputs through a prenet before sending them to the cell.'''
  def __init__(self, cell, is_training):
    super(DecoderPrenetWrapper, self).__init__()
    self._cell = cell
    self._is_training = is_training

  @property
  def state_size(self):
    return self._cell.state_size

  @property
  def output_size(self):
    return self._cell.output_size

  def call(self, inputs, state):
    prenet_out = prenet(inputs, self._is_training, scope='decoder_prenet')
    return self._cell(prenet_out, state)

  def zero_state(self, batch_size, dtype):
    return self._cell.zero_state(batch_size, dtype)



class ConcatOutputAndAttentionWrapper(RNNCell):
  '''Concatenates RNN cell output with the attention context vector.

  This is expected to wrap a cell wrapped with an AttentionWrapper constructed with
  attention_layer_size=None and output_attention=False. Such a cell's state will include an
  "attention" field that is the context vector.
  '''
  def __init__(self, cell):
    super(ConcatOutputAndAttentionWrapper, self).__init__()
    self._cell = cell

  @property
  def state_size(self):
    return self._cell.state_size

  @property
  def output_size(self):
    return self._cell.output_size + self._cell.state_size.attention

  def call(self, inputs, state):
    output, res_state = self._cell(inputs, state)
    return tf.concat([output, res_state.attention], axis=-1), res_state

  def zero_state(self, batch_size, dtype):
    return self._cell.zero_state(batch_size, dtype)

class ZoneoutWrapper(RNNCell):
  """Add Zoneout to a RNN cell."""

  def __init__(self, cell, zoneout_drop_prob, is_training=True):
    self._cell = cell
    self._zoneout_prob = zoneout_drop_prob
    self._is_training = is_training

  @property
  def state_size(self):
    return self._cell.state_size

  @property
  def output_size(self):
    return self._cell.output_size

  def __call__(self, inputs, state, scope=None):
    output, new_state = self._cell(inputs, state, scope)
    if not isinstance(self._cell.state_size, tuple):
      new_state = tf.split(value=new_state, num_or_size_splits=2, axis=1)
      state = tf.split(value=state, num_or_size_splits=2, axis=1)
    final_new_state = [new_state[0], new_state[1]]
    if self._is_training:
      for i, state_element in enumerate(state):
        random_tensor = 1 - self._zoneout_prob  # keep probability
        random_tensor += tf.random_uniform(tf.shape(state_element))
        # 0. if [zoneout_prob, 1.0) and 1. if [1.0, 1.0 + zoneout_prob)
        binary_tensor = tf.floor(random_tensor)
        final_new_state[
            i] = (new_state[i] - state_element) * binary_tensor + state_element
    else:
      for i, state_element in enumerate(state):
        final_new_state[
            i] = state_element * self._zoneout_prob + new_state[i] * (
                1 - self._zoneout_prob)
    if isinstance(self._cell.state_size, tuple):
      return output, tf.contrib.rnn.LSTMStateTuple(
          final_new_state[0], final_new_state[1])

    return output, tf.concat([final_new_state[0], final_new_state[1]], 1)

