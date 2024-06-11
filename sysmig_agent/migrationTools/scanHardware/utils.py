#!/usr/bin/python3
# -*- coding: utf-8 -*-

from os import pathconf
import pylspci
import json
from sysmig_agent.migrationTools.utils.config import PathConf


def get_pci_list() -> list:
    ''' 获取 pylspci 提供的列表
    '''
    return pylspci.parsers.SimpleParser().run()


def int_id_to_hex(int_id: int) -> str:
    ''' 十进制转十六进制。获得整数的 16 进制值（字符串表示）
    
    Args:
        int_id: 要转换整数
    
    Returns:
        长度为 4 的 16 进制值的字符串
    '''
    hex_id = hex(int_id)[2:]
    if len(hex_id) == 3:
        hex_id = hex_id + '0'
    return hex_id


def get_hex_id(name_with_id: pylspci.fields.NameWithID) -> str:
    ''' 获取设备 id 的 16 进制值（字符串表示）
    
    Args:
        name_with_id: 包含了一个设备的名称和 id 的实例
    
    Returns:
        长度为 4 的 16 进制值的字符串
    '''
    int_id = name_with_id.as_dict().get('id')
    if int_id == None:  # 若为空，直接返回
        return ''
    hex_id = hex(int_id)[2:]
    if len(hex_id) == 3:  # 否则判断补全一下
        hex_id = hex_id + '0'
    return hex_id


def get_parsed_pci_list(pci_list: list) -> list:
    ''' 获取解析后的 pci 设备列表
    
    Args:
        pci_list: pylspci.parsers.SimpleParser() 生成的 pci 设备列表
    
    Returns:
        一个二维列表，是根据需求解析后的设备列表。每一行是一个设备，每行的内容依次为：
        vendor id、device id、svid、ssid、设备类型id、设备厂商名、设备名、subsystem 厂商名、subsystem_device 名、设备类型名
    '''
    parsed_list = []

    for pci_item in pci_list:
        item = []
        # vendor 十六进制字符串 id
        item.append(get_hex_id(pci_item.vendor))
        # device id
        item.append(get_hex_id(pci_item.device))
        # svid
        item.append(get_hex_id(pci_item.subsystem_vendor))
        # ssid
        item.append(get_hex_id(pci_item.subsystem_device))
        # device class id
        item.append(int_id_to_hex(pci_item.cls.id))
        # device vendor name
        item.append(pci_item.vendor.name)
        # device name
        item.append(pci_item.device.name)
        # subsystem_vendor name
        item.append(pci_item.subsystem_vendor.name)
        # subsystem_device name
        item.append(pci_item.subsystem_device.name)
        # device class name
        item.append(pci_item.cls.name)

        parsed_list.append(item)

    return parsed_list


def get_supported_device_list() -> list:
    ''' 获取支持的设备列表
    
    读取 openEuler 提供的 json ，解析之，返回
    
    Returns:
        包含了支持的硬件信息的 list
    '''
    openEuelr_compat_list_file = open(
        PathConf.data_path +
        "/hardware-compatibility/compat_card_zh-83d1f0c07421a630f599f3608c60269f420e0f16.json",
        mode='r')
    oe_json_str = openEuelr_compat_list_file.read()
    json_obj = json.loads(oe_json_str, parse_int=str)
    
    ut_compat_list_file = open(
        PathConf.data_path +
        "/hardware-compatibility/ut_compat_hardwares.json",
        mode='r')
    ut_json_str = ut_compat_list_file.read()
    ut_json_obj = json.loads(ut_json_str, parse_int=str)
    
    for obj in ut_json_obj:
        json_obj.append(obj)
    
    for obj in json_obj:
        obj["vendorID"] = obj.get("vendorID")[0:4]
        obj["deviceID"] = obj.get("deviceID")[0:4]
        obj["svID"] = obj.get("svID")[0:4]
        obj["ssID"] = obj.get("ssID")[0:4]
        
    return json_obj


def get_compatability_list(pci_list: list, supported_device_list: list,
                           with_column_title: bool) -> list:

    parsed_list = []

    if with_column_title:
        column_title = ["vendorID", "deviceID", "svID", "ssID", "device class ID", "vendor name", "device name",\
                 "subsystem_vendor name", "subsystem_device name", "device class name", "compatability"]
        parsed_list.append(column_title)

    for pci_item in pci_list:
        item = []
        # vendor 十六进制字符串 id
        item.append(get_hex_id(pci_item.vendor))
        # device id
        item.append(get_hex_id(pci_item.device))
        # svid
        item.append(get_hex_id(pci_item.subsystem_vendor))
        # ssid
        item.append(get_hex_id(pci_item.subsystem_device))
        # device class id
        item.append(int_id_to_hex(pci_item.cls.id))
        # device vendor name
        item.append(pci_item.vendor.name)
        # device name
        item.append(pci_item.device.name)
        # subsystem_vendor name
        item.append(pci_item.subsystem_vendor.name)
        # subsystem_device name
        item.append(pci_item.subsystem_device.name)
        # device class name
        item.append(pci_item.cls.name)

        current_device_vendor_device_id = get_hex_id(
            pci_item.vendor) + get_hex_id(pci_item.device)
        current_device_all_id = get_hex_id(pci_item.vendor) + get_hex_id(pci_item.device) + \
                                get_hex_id(pci_item.subsystem_vendor) + get_hex_id(pci_item.subsystem_device)

        compatability = "Need Check"

        for dev in supported_device_list:
            if current_device_vendor_device_id == dev.get(
                    "vendorID") + dev.get("deviceID"):
                compatability = "Need Check"
            if current_device_all_id == dev.get("vendorID") + dev.get(
                    "deviceID") + dev.get("svID") + dev.get("ssID"):
                compatability = "Compatible"

        item.append(compatability)
        parsed_list.append(item)

    return parsed_list
