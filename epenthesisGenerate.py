
import tensorflow as tf
from IPython.display import display, Audio
import numpy as np
import PIL.Image
from IPython.display import display, Audio
import time as time
import scipy.io.wavfile

# Load the graph
tf.reset_default_graph()
saver = tf.train.import_meta_graph('/projects/580_waves_august2020/scripts/GAN_data/epenthesisGAN/epenthesisGANfolder/infer/infer.meta')
graph = tf.get_default_graph()
sess = tf.InteractiveSession()
saver.restore(sess, '/projects/580_waves_august2020/scripts/GAN_data/epenthesisGAN/epenthesisGANfolder/model.ckpt-9403')


#ngenerate = 100
ndisplay = 950

ngenerate = 950


# Sample latent vectors

np.random.seed(345)

#_z = (np.random.rand(ngenerate, 100) * 2.) - 1.
_z = np.random.uniform(-1,1, [ngenerate, 100])

#k = -4.5
#g = 4.5


_z[:,0] = 2.
_z[:,1] = 0.

_z[:,66] = 5.



# Generate
z = graph.get_tensor_by_name('z:0')
G_z = graph.get_tensor_by_name('G_z:0')[:, :, 0]


_G_z = sess.run([G_z], {z: _z})

with open('/projects/580_waves_august2020/scripts/GAN_data/epenthesisGAN/epenthesis9403seed345_z1_2_z2_0z66_45.txt', 'w') as f:
	_z.tofile(f,sep="\n")


for i in range(ndisplay):
	scipy.io.wavfile.write('/projects/580_waves_august2020/scripts/GAN_data/epenthesisGAN/epenthesis9403seed345_z1_2_z2_0z66_45.wav',16000,_G_z[i].T)



