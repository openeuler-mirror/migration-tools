import os

def is_number(s):
    '''
        应用场景：rpm包匹配
        功    能：判断某个字符是否为数字
        输入参数：s-字符变量
        返 回 值：True-字符为数字；False-字符非数字
    '''

    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False

def gen_pkg_version(pkg):
    key = len(pkg)+1
    cmd = 'rpm -qa %s' %(pkg)
    for line in os.popen(cmd):
        if is_number(line.replace('\n', '')[key]):
            rpm_info = line.replace('\n', '').rsplit('.', 1)[0].rsplit('-', 2)
            version = rpm_info[1]+'-'+rpm_info[2]
            return version

    return False

def dataplaceholder_replace(template, report, replace_str):
    '''按照前后端接口（json格式）替换检测报告中数据占位符 "dataPlaceholder"
        参数：
            template    检测报告模板
            report      检测报告名
            replace_str json格式数据
        返回：
            report 检测报告(html)
    '''

    dataplaceholder = 'dataPlaceholder'
    fp = open(report, mode='w')
    for line in open(template, mode='r'):
        if 'dataPlaceholder' in line:
            line = line.replace(dataplaceholder, replace_str)
        fp.write(line)

    fp.close()
    return report

def main():
    template_name = 'templat.html'
    html_name = 'report.html'
    jsonstr = 'test string'
    dataplaceholder_replace(template_name, html_name, jsonstr)

if __name__ == "__main__":
    main()

