#!/bin/sh
source /home2/begus/env36/bin/activate
export CUDA_VISIBLE_DEVICES="0"
/opt/python/gpu/python-3.6/bin/python3  /projects/580_waves_august2020/scripts/GAN_data/epenthesisGAN/epenthesisGenerate.py