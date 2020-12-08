#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import datetime

import pytest
import requests
from jsonpath import jsonpath

from service_19.tag import Tag

class TestTag:
    def setup_class(self):
        self.tag=Tag()

    #参数化
    @pytest.mark.parametrize("tag_id, tag_name",[
        ['etXjFsDQAA4hitDw15RONsolZHq2oO7A', 'tag1_new_'],
        ['etXjFsDQAA4hitDw15RONsolZHq2oO7A', 'tag1_new_中文'],
        ['etXjFsDQAA4hitDw15RONsolZHq2oO7A', 'tag1_new*%中文'],
    ])
    def test_tag_list1(self, tag_id, tag_name):
        tag_name_data = tag_name + str(datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
        tag = Tag()
        r = self.tag.list()
        r = self.tag.update(
            id=tag_id,
            tag_name=tag_name_data
        )
        r = self.tag.list()
        '''
        tags = [tag for group in r.json()['tag_group'] if group['group_name'] == group_name
                for tag in group['tag'] if tag['name'] == tag_name_data
                ] 
        assert tags != []
        '''
        assert jsonpath(r.json(), f"$..[?(@.name=='{tag_name_data}')]")[0]['name'] == tag_name_data

    def test_tag_list_fail(self):
        pass

    def test_list(self):
        self.tag.list()

    #问题记录1、如果errcode为40071，"UserTag Name Already Exist"，
    # 1）可以删除已有的tag(推荐)
    # 2）或者在已有的tag_name的基础上追加其他的tag_name
    def test_add_tag(self):
        #对add进行封装
        #todo:测试数据要放在数据文件中
        group_name = "test1"
        tag = [{"name": "TAG1"},
               {"name": "TAG2"},
               {"name": "TAG3"}, ]
        r = self.tag.add(group_name, tag)
        assert r.status_code == 200
        assert r.json()["errcode"] == 0
        # self.tag.add() 原始测试

    def test_add_and_detect(self):
        group_name = "test1"
        tag = [{"name": "TAG1"},
               {"name": "TAG2"},
               {"name": "TAG3"}, ]
        r = self.tag.add_and_detect(group_name, tag)
        assert r



    '''
    #问题记录2、如果errcode为40068，"invalid tagid"，
    #0）手动添加一个标签：
    #1）删除标签有问题；
    #2）再进行重试（重试次数：n）：a.添加一个接口；b.对新添加的接口再删除；c.查询删除是否成功；
    # 重试有几种实现方式：手动实现，借助pytest钩子（rerun插件）
    def test_delete(self):
        self.tag.delete()
    '''
    #封装delete：第1种情况：删除标签组
    def test_delete_group(self):
        self.tag.delete_group(['etXjFsDQAAFtarxdsDdE9DzmLYP42oZQ'])
    #封装delete：第2种情况：删除标签
    def test_delete_tag(self):
        self.tag.delete_tag(['etXjFsDQAAKIjldjEYWFKwWNvIdDFrkg'])

    def test_delete_and_detect_group(self):
        r = self.tag.delete_and_detect_group(["etXjFsDQAAfkqVAnTsn0F-jLyZ00wsbA"]) #输入test1的tag_id
        assert r.json()["errcode"] == 0