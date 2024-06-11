#!/usr/bin/env python3
# coding=utf-8

from sysmig_agent.migrationTools.utils.pygrok import pygrok


class ContentParser():
    @staticmethod
    def parse_sysctl_content(content):
        """
        """
        pattern = '^%{DATA:key}[=]%{SPACE}%{GREEDYDATA:value}'
        grok = pygrok.Grok(pattern)

        stored_dict = {}
        for line in content:
            match_line = grok.match(line)
            if match_line is None or match_line == {}:
                continue
            key = match_line['key'].strip()
            value = match_line['value'].strip()
            ## key 不重复时,直接保存
            if not key in stored_dict.keys():
                stored_dict[key] = value
            ## key 重复时, value 需要追加
            else:
                stored_value = stored_dict[key]
                ##  重复时,第一次不是个列表,要改成列表
                if not isinstance(stored_value, list):
                    stored_dict[key] = [stored_value, value]
                ## 第三个及以后重复值追加列表即可
                else:
                    stored_dict[key].append(value)
        return stored_dict

    @staticmethod
    def parse_system_service_content(content):
        stored_dict = []
        ## 第一行为表头,不需要解析
        for line in content[1:]:
            pattern = '^%{DATA:unit}\\s+%{DATA:load}\\s+%{DATA:active}\\s+%{DATA:sub}\\s+%{GREEDYDATA:description}$'
            grok = pygrok.Grok(pattern)
            match_line = grok.match(line)
            if match_line is None or match_line == {}:
                continue
            # "not found" line start with "*", need parse
            if match_line['unit'].strip() == '●':
                pattern = '^[●]\\s+%{DATA:unit}\\s+%{DATA:load}\\s+%{DATA:active}\\s+%{DATA:sub}\\s+%{GREEDYDATA:description}$'
                grok = pygrok.Grok(pattern)
                match_line = grok.match(line)
            if match_line is None or match_line == {}:
                continue
            stored_dict.append(match_line)
        return stored_dict
