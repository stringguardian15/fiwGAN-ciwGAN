executable = epenthesisGenerate.sh
getenv = True
error      = generateError.txt
log        = generateLog.txt
notification = complete
request_memory = 4*1024
request_GPUs = 1
requirements = (machine == "patas-gn2.ling.washington.edu")
queue
