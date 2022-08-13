import os
import sys
import scipy.io
import scipy.misc
from PIL import Image
import numpy as np
import tensorflow as tf
from tensorflow.python.framework.ops import EagerTensor
import pprint
import time

class utils:
  def clip_0_1(image):
    """
    Truncate all the pixels in the tensor to be between 0 and 1
    
    Arguments:
    image -- Tensor
    J_style -- style cost coded above

    Returns:
    Tensor
    """
    return tf.clip_by_value(image, clip_value_min=0.0, clip_value_max=1.0)

  def tensor_to_image(tensor):
    """
    Converts the given tensor into a PIL image
    
    Arguments:
    tensor -- Tensor
    
    Returns:
    Image: A PIL image
    """
    tensor = tensor * 255
    tensor = np.array(tensor, dtype=np.uint8)
    if np.ndim(tensor) > 3:
        assert tensor.shape[0] == 1
        tensor = tensor[0]
    return Image.fromarray(tensor)
  
  def generate_noise(image):
    generated_image = tf.Variable(tf.image.convert_image_dtype(image, tf.float32))
    noise = tf.random.uniform(tf.shape(generated_image), -0.25, 0.25)
    generated_image = tf.add(generated_image, noise)
    generated_image = tf.clip_by_value(generated_image, clip_value_min=0.0, clip_value_max=1.0)
    return generated_image

class Render:
  img_size = 400
  vgg = tf.keras.applications.VGG19(
    include_top=False, # exclude the fc layer
    input_shape=(img_size, img_size, 3),
    weights='pretrained-model/vgg19_weights_tf_dim_ordering_tf_kernels_notop.h5'
  )

  content_layer = [('block5_conv4', 1)]
  STYLE_LAYERS = [
    ('block1_conv1', 0.2),
    ('block2_conv1', 0.2),
    ('block3_conv1', 0.2),
    ('block4_conv1', 0.2),
    ('block5_conv1', 0.2)
  ]

  def __init__(self, content_file, style_file):
    self.content_file = content_file
    self.style_file = style_file
  
  def compute_content_cost(content_output, generated_output):
    """
    Computes the content cost
    
    Arguments:
    a_C -- tensor of dimension (1, n_H, n_W, n_C), hidden layer activations representing content of the image C 
    a_G -- tensor of dimension (1, n_H, n_W, n_C), hidden layer activations representing content of the image G
    
    Returns: 
    J_content -- scalar that you compute using equation 1 above.
    """
    a_C = content_output[-1]
    a_G = generated_output[-1]
    
    _, n_H, n_W, n_C = a_G.get_shape().as_list()
    a_C_unrolled = tf.reshape(tf.transpose(a_C, perm=[0,3,1,2]), shape=[n_H * n_W, n_C])
    a_G_unrolled = tf.reshape(tf.transpose(a_G, perm=[0,3,1,2]), shape=[n_H * n_W, n_C])
    
    J_content = tf.reduce_sum(tf.square(tf.subtract(a_C_unrolled, a_G_unrolled))) / (4 * n_H * n_W * n_C)
    return J_content
  
  def gram_matrix(A):
    """
    Argument:
    A -- matrix of shape (n_C, n_H*n_W)
    
    Returns:
    GA -- Gram matrix of A, of shape (n_C, n_C)
    """  
    GA = tf.matmul(A, tf.transpose(A))
    return GA
  
  def compute_layer_style_cost(self, a_S, a_G):
    """
    Arguments:
    a_S -- tensor of dimension (1, n_H, n_W, n_C), hidden layer activations representing style of the image S 
    a_G -- tensor of dimension (1, n_H, n_W, n_C), hidden layer activations representing style of the image G
    
    Returns: 
    J_style_layer -- tensor representing a scalar value, style cost defined above by equation (2)
    """
    _, n_H, n_W, n_C = a_G.get_shape().as_list()
    
    a_S = tf.reshape(tf.transpose(a_S, perm=[0,3,1,2]), shape=[n_C, n_H * n_W])
    a_G = tf.reshape(tf.transpose(a_G, perm=[0,3,1,2]), shape=[n_C, n_H * n_W])

    GS = self.gram_matrix(a_S)
    GG = self.gram_matrix(a_G)

    J_style_layer = tf.reduce_sum(tf.square(tf.subtract(GS, GG))) / (4 * n_C * n_C * n_H * n_H * n_W * n_W)
    return J_style_layer
  
  def compute_style_cost(self, style_image_output, generated_image_output, STYLE_LAYERS=STYLE_LAYERS):
    """
    Computes the overall style cost from several chosen layers
    
    Arguments:
    style_image_output -- our tensorflow model
    generated_image_output --
    STYLE_LAYERS -- A python list containing:
                        - the names of the layers we would like to extract style from
                        - a coefficient for each of them
    
    Returns: 
    J_style -- tensor representing a scalar value, style cost defined above by equation (2)
    """
    J_style = 0
    a_S = style_image_output[:-1]
    a_G = generated_image_output[:-1]
    for i, weight in zip(range(len(a_S)), STYLE_LAYERS):  
        J_style_layer = self.compute_layer_style_cost(a_S[i], a_G[i])
        J_style += weight[1] * J_style_layer

    return J_style

  @tf.function()
  def total_cost(J_content, J_style, alpha = 10, beta = 40):
    """
    Computes the total cost function

    Arguments:
    J_content -- content cost coded above
    J_style -- style cost coded above
    alpha -- hyperparameter weighting the importance of the content cost
    beta -- hyperparameter weighting the importance of the style cost

    Returns:
    J -- total cost as defined by the formula above.
    """
    J = alpha * J_content + beta * J_style
    return J
  
  def get_layer_outputs(vgg, layer_names):
    """ Creates a vgg model that returns a list of intermediate output values."""
    outputs = [vgg.get_layer(layer[0]).output for layer in layer_names]
    model = tf.keras.Model([vgg.input], outputs)
    return model
  
  @tf.function()
  def train_step(self, generated_image, content_image, style_image, optimizer=tf.keras.optimizers.Adam(learning_rate=0.01)):    
    vgg_model_outputs = self.get_layer_outputs(self.vgg, self.STYLE_LAYERS + self.content_layer)
    content_target = self.vgg_model_outputs(content_image)  # Content encoder
    style_targets = self.vgg_model_outputs(style_image)     # Style enconder

    preprocessed_content =  tf.Variable(tf.image.convert_image_dtype(content_image, tf.float32))
    preprocessed_style =  tf.Variable(tf.image.convert_image_dtype(style_image, tf.float32))

    a_C = vgg_model_outputs(preprocessed_content)
    a_S = vgg_model_outputs(preprocessed_style)
    with tf.GradientTape() as tape:
        a_G = vgg_model_outputs(generated_image)
        
        J_style = self.compute_style_cost(a_S, a_G)
        J_content = self.compute_content_cost(a_C, a_G)
        J = self.total_cost(J_content, J_style)
        
    grad = tape.gradient(J, generated_image)

    optimizer.apply_gradients([(grad, generated_image)])
    generated_image.assign(utils.clip_0_1(generated_image))
    utils
    return J

if __name__ == '__main__':  
  print('First param:', sys.argv[1])
  print('Second param:', sys.argv[2])