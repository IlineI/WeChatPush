import itchat.content
import requests
import importlib
import re
import os
import urllib.request
from urllib.request import quote, unquote
from requests.packages import urllib3
from datetime import datetime

try:
    import config
except:
    print('配置文件异常,请检查配置文件是否存在或语法是否有问题')
    print('程序终止运行')
    os._exit(0)

urllib3.disable_warnings()

def data_send(url, **kwargs):
    try:
        response = requests.post(url, data=kwargs, timeout=5, verify=False)
        if response.status_code > 299:
            raise RuntimeError
    except:
        for i in range(1, 4):
            print('向接口发送数据超时/失败，第' + str(i) + '次重试')
            try:
                response = requests.post(url, data=kwargs, timeout=5, verify=False)
                if response.status_code > 299:
                    raise RuntimeError
            except:
                if str(i) == '3':
                    print('连续三次向接口发送数据超时/失败，可能是网络问题或接口失效，终止发送')
                continue
            else:
                print('成功向接口发送数据↓')
                break
    else:
        print('成功向接口发送数据')


@itchat.msg_register([itchat.content.EMOTICON, itchat.content.VOIP, itchat.content.WEBSHARE, itchat.content.TEXT,
                        itchat.content.ATTACHMENT, itchat.content.VIDEO, itchat.content.CARD, itchat.content.SPLITTHEBILL,
                        itchat.content.FRIENDS, itchat.content.MUSICSHARE, itchat.content.UNDEFINED, itchat.content.PICTURE,
                        itchat.content.RECORDING, itchat.content.SERVICENOTIFICATION, itchat.content.TRANSFER, itchat.content.MAP,
                        itchat.content.LOCATIONSHARE, itchat.content.CHATHISTORY, itchat.content.SHARING, itchat.content.REDENVELOPE,
                        itchat.content.MINIPROGRAM, itchat.content.SYSTEMNOTIFICATION], isFriendChat=True, isGroupChat=True)
def simple_reply(msg):
    try:
        importlib.reload(config)
    except:
        print('配置文件读取异常,请检查配置文件是否存在或语法是否有问题')
        print('程序终止运行')
        os._exit(0)
    if str(msg.get('NickName')) not in config.blacklist:
        typesymbol = {
            itchat.content.TEXT: str(msg.get('Text')),
            itchat.content.FRIENDS: '好友请求',
            itchat.content.PICTURE: '[图片]',
            itchat.content.RECORDING: '[语音]',
            itchat.content.VIDEO: '[视频]',
            itchat.content.LOCATIONSHARE: '[共享实时位置]',
            itchat.content.CHATHISTORY: '[聊天记录]',
            itchat.content.TRANSFER: '[转账]',
            itchat.content.REDENVELOPE: '[红包]',
            itchat.content.SHARING: '[分享]',
            itchat.content.EMOTICON: '[动画表情]',
            itchat.content.SPLITTHEBILL: '[群收款]',
            itchat.content.VOIP: '[通话邀请]请及时打开微信查看',
            itchat.content.SYSTEMNOTIFICATION: '[系统通知]',
            itchat.content.ATTACHMENT: '[文件]' + str(msg.get('Text')),
            itchat.content.CARD: '[名片]' + str(msg.get('Text')),
            itchat.content.MUSICSHARE: '[音乐]' + str(msg.get('Text')),
            itchat.content.SERVICENOTIFICATION: str(msg.get('Text')),
            itchat.content.MAP: '[位置分享]' + str(msg.get('Text')),
            itchat.content.WEBSHARE: '[链接]' + str(msg.get('Text')),
            itchat.content.MINIPROGRAM: '[小程序]' + str(msg.get('Text')),
            itchat.content.UNDEFINED: '[未知消息类型]: MsgType=' + str(msg.get('Text')) }.get(msg['Type'])
        Name = msg.get('Name') if msg.get('ChatRoom') == 0 else '群聊 ' + msg.get('ChatRoomName')
        typesymbol = str(typesymbol) if msg.get('ChatRoom') == 0 else str(msg.get('Name')) + ': ' + str(typesymbol)
        url ='https://wirepusher.com/send?id='+str(wire_id)+'&title=微信'+str(Name)+'&message='+str(typesymbol)+'&type=WeChat'+'&action=weixin://'
        url = quote(url, safe=";/?:@&=+$,", encoding="utf-8")
        if msg.get('Type') == 'Voip':
            if separate_push != 'false' and VoIP_regID != '':
                data_send(str(config.VoIP_interface), title='微信 ' + str(Name), content=str(typesymbol), regID=str(config.VoIP_regID), phone='0', through='0')
            else:
                if str(chat_alias):
                    data_send(str(config.chat_interface), title='微信 ' + str(Name), content=str(typesymbol), alias=str(config.chat_alias))
                elif str(wire_id):
                    requests.post(url)
        else:
            if str(chat_alias):
                data_send(str(config.chat_interface), title='微信 ' + str(Name), content=str(typesymbol), alias=str(config.chat_alias))
            elif str(wire_id):
                requests.post(url)
        typesymbol = '[未知卡片消息]: AppMsgType=' + str(msg.get('Text')) if msg.get('Type') == 'Sharing' else typesymbol
        print(datetime.now().strftime('%Y.%m.%d %H:%M:%S') + ' ' + str(Name) + ': ' + str(typesymbol))

if __name__ == '__main__':
    itchat.check_login()
    itchat.auto_login(hotReload=True, enableCmdQR=2)
    itchat.run()
