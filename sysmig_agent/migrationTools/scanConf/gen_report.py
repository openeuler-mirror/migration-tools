import json
import os
import platform

from sysmig_agent.migrationTools.utils.config import PathConf
from sysmig_agent.migrationTools.utils.logger import Logger
import sysmig_agent.migrationTools.utils.html as html

logger = Logger(__name__)


def gen_compat_report(changed_conf_dir, original_conf_dir):
    data = gen_conf_data(changed_conf_dir, original_conf_dir)

    html_context = 'utmt_report_mode="scanconfig"; utmt_report_data=`' +\
            f'{data}' + '`;'

    report_dir = PathConf.report_dir
    datafile_dir = os.path.join(report_dir, 'datafile')
    report_name = f"conf_info_report_{PathConf.timestamp}"
    html_data_path = os.path.join(datafile_dir, f"{report_name}.js")
    if not os.path.exists(datafile_dir):
        os.makedirs(datafile_dir, exist_ok=True)
    html.copy_html_resource()
    ## 生成json文件, 用于前端调试
    json_path = os.path.join(datafile_dir, f"{report_name}.json")
    with open(json_path, 'w') as f:
        f.write(data)
    logger.debug(f"json_path: {json_path}")

    with open(html_data_path, "w") as file:
        html_context = html_context.replace(r'\\t', r'\t')
        html_context = html_context.replace(r'\t', r'\\t')
        html_context = html_context.replace(r'\x', r'\\x')
        file.write(html_context)

    html_context = html.gen_html_template(html_data_path)
    html_name = f"conf_info_report_{PathConf.timestamp}.html"
    html_path = os.path.join(report_dir, html_name)
    with open(html_path, "w") as file:
        file.write(str(html_context))

    logger.info(f"report has been generated: {html_path}.")


def gen_conf_data(changed_conf_dir, original_conf_dir):
    data = {}
    target_OS = "UnionTech OS Server 20"
    current_OS = platform.linux_distribution(
    )[0] + " " + platform.linux_distribution()[1]
    data.update({
        'newOS':
        f"{target_OS}",
        'oldOS':
        f"{current_OS}",
        'arch':
        f'{PathConf.arch}',
        'desc':
        f"""Information about {current_OS} and {target_OS} system configuration compatibility"""
    })

    data_table = gen_data_table(changed_conf_dir, original_conf_dir)
    data.update(data_table)

    return json.dumps(data)


def gen_data_table(changed_conf_dir, original_conf_dir):
    """
    生成 数据页面中的 dataTable 值
    """
    data = {'dataTable': []}
    sysctl_a_data = gen_sysctl_a_data(changed_conf_dir, original_conf_dir)
    data['dataTable'].append(sysctl_a_data)

    systemctl_a_data = gen_systemctl_a_data(changed_conf_dir,
                                            original_conf_dir)
    data['dataTable'].append(systemctl_a_data)

    return data


def get_json_content(dirname, name):
    file = os.path.join(dirname, name)
    data = json.load(open(file))
    if data is None:
        data = {}
    return data


def gen_sysctl_a_data(changed_conf_dir, original_conf_dir):
    element = {"name": 'system configure', 'item': []}
    changed_data = get_json_content(changed_conf_dir, "sysctl_a.json")
    original_data = get_json_content(original_conf_dir, "sysctl_a.json")

    for key in changed_data:
        res = 'different'
        if key in original_data:
            ## 默认结论 改变
            if changed_data[key] == original_data[key]:
                ## sysctl 项 一致 后, 结论为 没有改变
                res = 'same'

            element['item'].append({
                'oldVal': f'{key} = {changed_data[key]}',
                'newVal': f'{key} = {original_data[key]}',
                'res': res
            })
        else:
            element['item'].append({
                'oldVal': f'{key} = {changed_data[key]}',
                'newVal': '',
                'res': res
            })
    for key in original_data:
        res = 'different'
        if key not in changed_data:
            element['item'].append({
                'oldVal': "",
                'newVal': f'{key} = {original_data[key]}',
                'res': res
            })
    element['item'].sort(key=lambda x: x['res'])
    return element


def gen_systemctl_a_data(changed_conf_dir, original_conf_dir):
    element = {"name": 'system service', 'item': []}
    changed_data = get_json_content(changed_conf_dir, "systemctl_a.json")
    original_data = get_json_content(original_conf_dir, "systemctl_a.json")

    c_units = [items["unit"] for items in changed_data]
    o_units = [items['unit'] for items in original_data]

    for c_service_item in changed_data:
        c_unit = c_service_item['unit']
        c_active = c_service_item['active']
        # 默认结论为 改变
        res = 'different'
        if c_unit in ("●", "LOAD", 'ACTIVE', 'SUB', "To"):
            continue

        for o_service_item in original_data:
            o_unit = o_service_item['unit']
            o_active = o_service_item['active']
            if o_unit in ("●", "LOAD", 'ACTIVE', 'SUB', "To"):
                continue
            ## 左边行和右边行都有 ,对比
            if c_unit == o_unit:
                if c_active == o_active:
                    ## service 项中的 unit 和 active 一致, 结论为 未改变
                    res = 'same'
                else:
                    pass
                element['item'].append({
                    'oldVal': f'{c_unit} = {c_active}',
                    'newVal': f'{o_unit} = {o_active}',
                    'res': res
                })
        ## 左边行有, 右边行没有, 对比
        if c_unit in c_units and c_unit not in o_units:
            element['item'].append({
                'oldVal': f"{c_unit} = {c_active}",
                'newVal': '',
                'res': res
            })
    ## 左边行没有 , 右边行有, 对比
    for o_service_item in original_data:
        o_unit = o_service_item['unit']
        o_active = o_service_item['active']
        # 默认结论为 新增
        res = 'different'
        if o_unit in ("●", "LOAD", 'ACTIVE', 'SUB', "To"):
            continue
        if o_unit in o_units and o_unit not in c_units:
            element['item'].append({
                'oldVal': "",
                'newVal': f'{o_unit} = {o_active}',
                'res': res
            })
    element['item'].sort(key=lambda x: x['res'])
    return element
