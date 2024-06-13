# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier:   MulanPubL-2.0-or-later

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
def selfDestruct(task_id):
    """
    destroy agent system migration rpm.
    Args:
        task_id:

    Returns:

    """
    if '9' == int(str(get_mig_state(task_id))[1]):
        cmd = 'yum remove -y uos-sysmig-agent uos-sysmig-data'
        _, code = run_subprocess(cmd)
        if code != 0:
            migration_log.error("Migration is complete，Agent[{}]:Uninstall failed".format(get_local_ip()))
        else:
            migration_log.info("Migration is complete，Agent[{}]:Uninstall has been successful".format(get_local_ip()))
    migration_log.info("migration statues is not satisfied，Agent[{}]:It is not uninstalled for the time being. Please "
                       "check the task_info.task-data table and uninstall it after the migration is "
                       "successful.".format(get_local_ip()))
