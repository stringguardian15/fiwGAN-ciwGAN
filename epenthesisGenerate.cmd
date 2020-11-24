executable = /projects/580_waves_august2020/scripts/GAN_data/epenthesisGAN/epenthesisGenerate.sh
getenv = True
error      = /projects/580_waves_august2020/scripts/GAN_data/epenthesisGAN/generateError.txt
log        = /projects/580_waves_august2020/scripts/GAN_data/epenthesisGAN/generateLog.txt
notification = complete
request_memory = 4*1024
request_GPUs = 1
requirements = (machine == "patas-gn2.ling.washington.edu")
queue