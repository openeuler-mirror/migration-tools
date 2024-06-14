
def dataplaceholder_replace(template, report, replace_str):
    '''按照前后端接口（json格式）替换检测报告中数据占位符 "dataPlaceholder"
        参数：
            template    检测报告模板
            report      检测报告名
            replace_str json格式数据
        返回：
            report 检测报告(html)
    '''
    dataplaceholder = '"dataPlaceholder"'
    fp = open(report, mode='w')
    for line in open(template, mode='r'):
        num += 1
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

