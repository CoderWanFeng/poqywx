# -*- coding: UTF-8 -*-
'''
@Author  ：B站/抖音/微博/小红书/公众号，都叫：程序员晚枫
@WeChat     ：CoderWanFeng
@Blog      ：www.python-office.com
@Date    ：2023/2/20 20:33 
@Description     ：
'''

import requests
import hashlib
import base64


class QYWeChat:

    def __init__(self, key):
        self.key = key
        self.wxurl = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=' + key

    def send_file(self, file_name, file_path):
        """
        自动发送文件
        :param file_name: 发送的文件名字，用于在企业微信上展示的
        :param file_path: 本地实际文件路径
        """
        po_file_reader = open(file_path, 'rb')
        files = {'files': (file_name, po_file_reader, 'application/octet-stream', {'Expires': '0'})}
        po_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key=' + self.key + '&type=file'
        poqywx_res = requests.post(po_url, files=files).json()
        # 把文件上送至企业微信服务器，生成media_id
        if poqywx_res['media_id'] is not None:
            send_json = {
                "msgtype": "file",
                "file": {
                    "media_id": poqywx_res['media_id']
                }
            }
            requests.post(send_url=self.wxurl, json=send_json)

    def send_message(self, content='', mentioned_list=[], mentioned_mobile_list=[]):
        """
        自动发送文字消息
        :param content: 文字内容
        :param mentioned_list: (不是必填项)userid的列表，提醒群中的指定成员(@某个成员)，@all表示提醒所有人，如果开发者获取不到userid，可以使用mentioned_mobile_list
        :param mentioned_mobile_list:(不是必填项)手机号列表，提醒手机号对应的群成员(@某个成员)，@all表示提醒所有人
        """
        po_data = {
            "msgtype": "text",
            "text": {
                "content": content,
                "mentioned_list": mentioned_list,
                "mentioned_mobile_list": mentioned_mobile_list
            }
        }
        po_res = requests.post(self.wxurl, json=po_data).json()
        print(po_res)

    def send_img(self, file_name):
        """
        自动发送图片
        :param file_name: 图片文件的路径
        """
        po_png = file_name
        with open(po_png, "rb") as f:
            md = hashlib.md5(f.read())
            res1 = md.hexdigest()
        with open(po_png, "rb") as f:
            base64_data = base64.b64encode(f.read())
        po_im_json = {
            "msgtype": "image",
            "image": {
                "base64": str(base64_data, 'utf-8'),
                "md5": res1
            }
        }
        requests.post(self.wxurl, json=po_im_json)
