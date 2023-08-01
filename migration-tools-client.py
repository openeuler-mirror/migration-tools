import os
import json

from func import check


mods = {
        'check_storage': check.check_storage,
        'check_os': check.check_os,
        }

def check_methods():
    if request.method == 'POST':
        data = request.get_data()
        migration.info(data)
        json_data = json.loads(data)
        mod = mods.get(json_data['mod'])
        if mod:
            response_str = mod(data)
            return response_str


@app.route('/check_storage', methods=['GET', 'POST'])
def mt_check_storage():
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')


@app.route('/check_os', methods=['GET', 'POST'])
def mt_check_os():
    mod = check_methods()
    if mod:
        return Response(mod, content_type='application/json')


if __name__ == '__main__':
    app.config["JSON_AS_ASCII"] = False
    uos_sysmig_conf = json.loads(getSysMigConf())
    ip = json.loads(uos_sysmig_conf).get('agentip').strip()[1:-1]
    port = int(json.loads(uos_sysmig_conf).get('agentport').strip()[1:-1])
    app.run(debug=True, host=ip, port=port)
