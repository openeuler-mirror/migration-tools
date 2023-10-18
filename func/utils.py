# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier:   MulanPubL-2.0-or-later
import json


def list_to_json(k_list, v_list):
    res = dict(zip(k_list, v_list))
    res = json.dumps(res)
    return json.dumps(res)


def message_progress(message):
    with open('/var/tmp/uos-migration/.progress', 'w') as fp:
        fp.write(message)
        fp.close()


def message_state(message):
    with open('/var/tmp/uos-migration/.state', 'w') as fp:
        fp.write(message)
        fp.close()
