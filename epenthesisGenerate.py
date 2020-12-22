import tensorflow as tf
from IPython.display import display, Audio
import numpy as np
import PIL.Image
from IPython.display import display, Audio
import time as time
import scipy.io.wavfile
import argparse
import os
import sys


print('test std err stream', file=sys.stderr)
output_filename = 'epenthesis9403seed345' 

parser = argparse.ArgumentParser()
parser.add_argument('--model_dir')
parser.add_argument('--output_dir')

# allow optional arguments for all possible z values
z_max = 100
z_dict = {}
for i in range(z_max+1):
    parser.add_argument('--z'+str(i), type=float)

args = parser.parse_args()

if args.model_dir is not None:
    model_dir = args.model_dir
else:
    model_dir = '/projects/580_waves_august2020/scripts/GAN_data/epenthesisGAN/epenthesisGANfolder'

if args.output_dir is not None:
    output_dir = args.output_dir
else:
    output_dir = 'outputs'

# now check for any z values as args
for i in range(z_max+1):
    if getattr(args, 'z'+str(i)) is not None:
        z_dict[i] = getattr(args, 'z'+str(i))
        output_filename = output_filename+'_z'+str(i)+'_'+str(z_dict[i])

output_filename = os.path.join(output_dir, output_filename)

# Load the graph
tf.reset_default_graph()
#saver = tf.train.import_meta_graph('/projects/580_waves_august2020/scripts/GAN_data/epenthesisGAN/epenthesisGANfolder/infer/infer.meta')
saver = tf.train.import_meta_graph(os.path.join(model_dir, 'infer/infer.meta'))
graph = tf.get_default_graph()
sess = tf.InteractiveSession()
#saver.restore(sess, '/projects/580_waves_august2020/scripts/GAN_data/epenthesisGAN/epenthesisGANfolder/model.ckpt-9403')
saver.restore(sess, os.path.join(model_dir,'model.ckpt-9403'))


#ngenerate = 100
ndisplay = 950

ngenerate = 950


# Sample latent vectors

np.random.seed(345)

#_z = (np.random.rand(ngenerate, 100) * 2.) - 1.
_z = np.random.uniform(-1,1, [ngenerate, 100])

#k = -4.5
#g = 4.5

for key in z_dict.keys():
    _z[:key] = z_dict[key]

'''
_z[:,0] = 2.
_z[:,1] = 0.

_z[:,66] = 5.
'''



# Generate
z = graph.get_tensor_by_name('z:0')
G_z = graph.get_tensor_by_name('G_z:0')[:, :, 0]


_G_z = sess.run([G_z], {z: _z})
print('_G_z: '+str(_G_z), file=sys.stderr)

txt_output = output_filename+'.txt'
wav_output = output_filename+'.wav'

#with open('/projects/580_waves_august2020/scripts/GAN_data/epenthesisGAN/epenthesis9403seed345_z1_2_z2_0z66_45.txt', 'w') as f:
with open(txt_output, 'w') as f:
    _z.tofile(f,sep="\n")


print("check shape of tensor _G_z: "+str(G_z.get_shape()), file=sys.stderr)
for i in range(ndisplay):
    #scipy.io.wavfile.write('/projects/580_waves_august2020/scripts/GAN_data/epenthesisGAN/epenthesis9403seed345_z1_2_z2_0z66_45.wav',16000,_G_z[i].T)
    print('try writing to wav file at index: '+str(i), file=sys.stderr)
    try:
        scipy.io.wavfile.write(wav_output,6000,_G_z[i].T)
    except:
        print('writing to wav file failed at index: '+str(i), file=sys.stderr)



