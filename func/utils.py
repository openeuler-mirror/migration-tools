import json

def list_to_json(keylist, valuelist):
    res = dict(zip(keylist, valuelist))
    res = json.dumps(res)
    return json.dumps(res)


# 检测进度
def messageProgress(message):
    with open('/var/tmp/uos-migration/.progress','w') as fp:
        fp.write(message)
        fp.close()


def messageState(message):
    with open('/var/tmp/uos-migration/.state','w') as fp:
        fp.write(message)
        fp.close()