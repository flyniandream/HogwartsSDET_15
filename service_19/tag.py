#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import datetime
import json

import requests


class Tag:
    #对获取token进行改造：初始化，只需要初始化一次
    def __init__(self):
        self.token = self.get_token()

    #第一步：获取token
    #PO中通常不加断言。这里token一旦读取不成功，后面的测试用例都不用跑了，可以加上
    def get_token(self):
        corpid = 'ww7539928d5dbb5657'
        corpsecret = 'N6KyzHa8tx5zw07kQDjYqcSd8ePSzNeVBpG60VrUyS0'
        r = requests.get('https://qyapi.weixin.qq.com/cgi-bin/gettoken',
                         params={'corpid': corpid, 'corpsecret': corpsecret},
                         )
        print("token:\n" + json.dumps(r.json(), indent=2))
        assert r.status_code == 200
        assert r.json()['errcode'] == 0

        token = r.json()['access_token']
        return token


    '''
    def add(self):
        r = requests.post("https://qyapi.weixin.qq.com/cgi-bin/externalcontact/add_corp_tag",
                          params={'access_token': self.token},
                          json={
                              "group_name": "test1",
                              "tag": [{"name": "TAG1"},
                                      {"name": "TAG2"},
                                      {"name": "TAG3"}, ]
                          }
                          )
        print(json.dumps(r.json(), indent=2))
        return r
        '''
    #判断元素是否存在（其实是find_group_id_by_name）
    def find_group_id_by_name(self,group_name):
        # 如果查询出要删除的元素存在，返回group_id
        for group in self.list().json()["tag_group"]:
            if group_name in group["group_name"]:
                return group["group_id"]
        # 如果查询出要删除的元素不存在，返回空
        print("group name not in group")
        #todo:如果group_id是空，也会类似False
        return ""

    #删除前判断group_id是否存在
    def is_group_id_exist(self, group_id):
        for group in self.list().json()["tag_group"]:
            if group_id in group["group_id"]:
                return True
        print("group id not in group")
        return False

    #对add进行封装
    def add(self, group_name, tag, **kwargs):
        r = requests.post("https://qyapi.weixin.qq.com/cgi-bin/externalcontact/add_corp_tag",
                          params={'access_token': self.token},
                          json={"group_name":group_name,
                                "tag":tag,
                                **kwargs}
                          )
        print(json.dumps(r.json(), indent=2))
        return r
    #[add之前进行清理（逻辑判断）]直接加上去，加上去之前进行一些清理工作
    def add_and_detect(self, group_name, tag, **kwargs):
        r = self.add(group_name, tag, **kwargs)
        # 如果删除的元素已经存在，可以去查它是否真的存在，怎么查呢？一是取出group_name，用in，第二种方式用jsonpath
        if r.json()["errcode"] == 40071:
            group_id = self.find_group_id_by_name(group_name)
            if not group_id:#如果没找到（为空），那么返回报错"group name not in group"；说明接口有问题，向研发反馈
                #return False #add时
                return ""     #delete时
            # 否则继续执行下述操作：先删除再添加
            self.delete_group(group_id)
            self.add(group_name, tag, **kwargs)

        result = self.find_group_id_by_name(group_name)
        if not result:
            print("add not success!")
        #return True #add时
        return result



    def list(self):
        r = requests.post('https://qyapi.weixin.qq.com/cgi-bin/externalcontact/get_corp_tag_list',
                          params={"access_token": self.token},
                          json={
                              "tag_id": []
                          }
                          )
        print(json.dumps(r.json(), indent=2))
        return r

    #编辑->更新
    def update(self, id, tag_name):
        r = requests.post('https://qyapi.weixin.qq.com/cgi-bin/externalcontact/edit_corp_tag',
                          params={"access_token": self.token},
                          json={'id': id,
                                'name': tag_name
                                }
                          )
        print(json.dumps(r.json(), indent=2))
        return r


    '''
    #封装数据之前：删除标签组和删除标签放在一起
    #删除tag_id之前查询它是否存在
    #如果正常：成功
    # {
    #     "errcode": 0,
    #     "errmsg": "ok"
    # }
    #如果异常：失败
    def delete(self):
        r = requests.post("https://qyapi.weixin.qq.com/cgi-bin/externalcontact/del_corp_tag",
                          params={"access_token": self.token},
                          #如果有一个标签不存在，那么删除都不能成功
                          json={'group_id':['etXjFsDQAAMACBzaW2nEHF3_dDzU409A']
                              # ,'tag_id': ['etXjFsDQAATHtTIQUBJtF17hctpQl4Gg']


                                }
                          )
        print(json.dumps(r.json(),indent=2))
        return r
    '''
    #封装delete：第1种情况：删除标签组
    def delete_group(self, group_id):
        r = requests.post("https://qyapi.weixin.qq.com/cgi-bin/externalcontact/del_corp_tag",
                          params={"access_token": self.token},
                          #如果有一个标签不存在，那么删除都不能成功
                          json={'group_id':group_id
                                }
                          )
        print(json.dumps(r.json(),indent=2))
        return r
    # 封装delete：第2种情况：删除标签
    def delete_tag(self,tag_id):
        r = requests.post("https://qyapi.weixin.qq.com/cgi-bin/externalcontact/del_corp_tag",
                          params={"access_token": self.token},
                          json={'tag_id': tag_id
                                }
                          )
        print(json.dumps(r.json(), indent=2))
        return r

    #"errcode": 40068,"errmsg": "invalid tagid:删除时不存在输入的tagid
    #删除之前进行判断操作
    def delete_and_detect_group(self, group_ids):
        deleted_group_ids = []
        r = self.delete_group(group_ids)
        if r.json()["errcode"] == 40068:
            #如果标签不存在，就添加一个标签，将它的group_id存储进来
            for group_id in group_ids:
                if not self.is_group_id_exist(group_id):
                    group_id_tmp = self.add_and_detect(group_name="test1", tag=[{"name":"123"}])
                    deleted_group_ids.append(group_id_tmp)
                #如果标签存在，就将它存入标签组
                else:
                    deleted_group_ids.append(group_id)
            r = self.delete_group(deleted_group_ids)
        return r


