import os
import sys
import json


mods = {'check_storage': check_storage}

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


#if __name__ == '__main__':
    #app.run(debug=True, host=127.0.0.1, port='9999')
