from nonebot.default_config import *

HOST = '0.0.0.0'
PORT = 8080
SUPERUSERS = {2967923486}
COMMAND_START = {'', '/', '!', '／', '！'}

# 这个参数是修改同一个 job 可以同时运行几个，如果要修改不同 job 应该要更改携程和线程的设置，这个之后研究
# APSCHEDULER_CONFIG = {
#     'apscheduler.job_defaults.max_instances': 3,
# }