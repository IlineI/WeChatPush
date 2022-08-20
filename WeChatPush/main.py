import itchat.content
import requests
import importlib
import time
import os
from requests.packages import urllib3
from datetime import datetime
from multiprocessing import Pool

try:
    import config
except:
    print(str(datetime.now().strftime('[%Y.%m.%d %H:%M:%S] ')) + '配置获取异常,请检查配置文件是否存在/权限是否正确/语法是否有误')
    print('程序终止运行')
    os._exit(0)

shield_mode = str(config.shield_mode)
whitelist = str(config.whitelist)
blacklist = str(config.blacklist)

urllib3.disable_warnings()


def config_update():
    while 1:
        try:
            importlib.reload(config)
        except:
            print(str(datetime.now().strftime('[%Y.%m.%d %H:%M:%S] ')) + '配置获取异常,请检查配置文件是否存在/权限是否正确/语法是否有误')
            print('程序终止运行')
            break
        global shield_mode,whitelist,blacklist
        shield_mode_update = '0'
        if str(config.shield_mode) != shield_mode:
            if int(config.shield_mode):
                print(str(datetime.now().strftime('[%Y.%m.%d %H:%M:%S] ')) + '切换为白名单模式：群聊' + str(config.whitelist) + '以及非群聊的消息将会推送')
            else:
                print(str(datetime.now().strftime('[%Y.%m.%d %H:%M:%S] ')) + '切换为黑名单模式：' + str(config.blacklist) + '的消息将不会推送')
            shield_mode = str(config.shield_mode)
            shield_mode_update = '1'
        if int(shield_mode_update):
            whitelist = str(config.whitelist)
            blacklist = str(config.blacklist)
        else:
            if str(config.whitelist) != whitelist and int(config.shield_mode):
                print(str(datetime.now().strftime('[%Y.%m.%d %H:%M:%S] ')) + '白名单更改：群聊' + str(config.whitelist) + '以及非群聊的消息将会推送')
                whitelist = str(config.whitelist)
            elif str(config.blacklist) != blacklist and not int(config.shield_mode):
                print(str(datetime.now().strftime('[%Y.%m.%d %H:%M:%S] ')) + '黑名单更改：' + str(config.blacklist) + '的消息将不会推送')
                blacklist = str(config.blacklist)
        time.sleep(1)


def forcequit(msg):
    os._exit(0)


def data_send(url, **kwargs):
    for i in range(1, 5):
        try:
            response = requests.post(url, data=kwargs, timeout=5, verify=False)
            if response.status_code > 299:
                raise RuntimeError
        except:
            if str(i) == '4':
                print(str(datetime.now().strftime('[%Y.%m.%d %H:%M:%S] ')) + '连续三次向接口发送数据超时/失败，可能是网络问题或接口失效，终止发送')
                break
            print(str(datetime.now().strftime('[%Y.%m.%d %H:%M:%S] ')) + '向接口发送数据超时/失败，第' + str(i) + '次重试')
        else:
            print(str(datetime.now().strftime('[%Y.%m.%d %H:%M:%S] ')) + '成功向接口发送数据↑')
            break


@itchat.msg_register([itchat.content.EMOTICON, itchat.content.VOIP, itchat.content.WEBSHARE, itchat.content.TEXT,
                        itchat.content.ATTACHMENT, itchat.content.VIDEO, itchat.content.CARD, itchat.content.SPLITTHEBILL,
                        itchat.content.FRIENDS, itchat.content.MUSICSHARE, itchat.content.UNDEFINED, itchat.content.PICTURE,
                        itchat.content.RECORDING, itchat.content.SERVICENOTIFICATION, itchat.content.TRANSFER, itchat.content.MAP,
                        itchat.content.LOCATIONSHARE, itchat.content.CHATHISTORY, itchat.content.SHARING, itchat.content.REDENVELOPE,
                        itchat.content.MINIPROGRAM, itchat.content.SYSTEMNOTIFICATION], isFriendChat=True, isGroupChat=True)
def simple_reply(msg):
    if int(config.shield_mode):
        if not int(msg.get('ChatRoom')) or str(msg.get('NickName')) in list(config.whitelist): # 白名单模式，白名单群消息放行
            notify = True
    else: # 黑名单模式，放行未加入黑名单的消息
        notify = False if str(msg.get('NickName')) in list(config.blacklist) else True
    if notify and not int(msg.get('NotifyCloseContact')):
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
            itchat.content.EMOTICON: '[动画表情]',
            itchat.content.SPLITTHEBILL: '[群收款]',
            itchat.content.SHARING: '[未知卡片消息]',
            itchat.content.UNDEFINED: '[未知消息类型]',
            itchat.content.VOIP: '[通话邀请]请及时打开微信查看',
            itchat.content.SYSTEMNOTIFICATION: '[系统通知]',
            itchat.content.ATTACHMENT: '[文件]' + str(msg.get('Text')),
            itchat.content.CARD: '[名片]' + str(msg.get('Text')),
            itchat.content.MUSICSHARE: '[音乐]' + str(msg.get('Text')),
            itchat.content.SERVICENOTIFICATION: str(msg.get('Text')),
            itchat.content.MAP: '[位置分享]' + str(msg.get('Text')),
            itchat.content.WEBSHARE: '[链接]' + str(msg.get('Text')),
            itchat.content.MINIPROGRAM: '[小程序]' + str(msg.get('Text')) }.get(msg['Type'])
        Name = str(msg.get('Name')) if str(msg.get('ChatRoom')) == '0' else '群聊 ' + str(msg.get('ChatRoomName'))
        if int(msg.get('ChatRoom')):
            typesymbol = str(msg.get('Name')) + ': ' + str(typesymbol)
        if str(msg.get('Type')) == str(itchat.content.SHARING):
            print('[未知卡片消息，请在github上提交issue]: AppMsgType=' + str(msg.get('Text')))
        elif str(msg.get('Type')) == str(itchat.content.UNDEFINED):
            print('[未知消息类型，请在github上提交issue]: MsgType=' + str(msg.get('Text')))
        else:
            print(str(Name) + ': ' + str(typesymbol))
        if str(msg.get('Type')) == str(itchat.content.VOIP):
            if str(config.VoIP_push) == '1' and str(config.tdtt_alias) != '':
                data_send(str(config.tdtt_interface), title='微信 ' + str(Name), content=str(typesymbol), alias=str(config.tdtt_alias))
            elif str(config.VoIP_push) == '2' and str(config.FarPush_regID) != '':
                data_send(str(config.FarPush_interface), title='微信 ' + str(Name), content=str(typesymbol), regID=str(config.FarPush_regID), phone=str(config.FarPush_Phone_Type), through='0')
            elif str(config.VoIP_push) == '3' and str(config.WirePusher_ID) != '':
                data_send(str(config.WirePusher_interface), title='微信 ' + str(Name), message=str(typesymbol), id=str(config.WirePusher_ID), type='WeChat_VoIP', action='weixin://')
            else:
                print(str(datetime.now().strftime('[%Y.%m.%d %H:%M:%S] ')) + '配置有误，请更改配置')
        else:
            if str(config.chat_push) == '1' and str(config.tdtt_alias) != '':
                data_send(str(config.tdtt_interface), title='微信 ' + str(Name), content=str(typesymbol), alias=str(config.tdtt_alias))
            elif str(config.chat_push) == '2' and str(config.FarPush_regID) != '':
                data_send(str(config.FarPush_interface), title='微信 ' + str(Name), content=str(typesymbol), regID=str(config.FarPush_regID), phone=str(config.FarPush_Phone_Type), through='0')
            elif str(config.chat_push) == '3' and str(config.WirePusher_ID) != '':
                data_send(str(config.WirePusher_interface), title='微信 ' + str(Name), message=str(typesymbol), id=str(config.WirePusher_ID), type='WeChat_chat', action='weixin://')
            else:
                print(str(datetime.now().strftime('[%Y.%m.%d %H:%M:%S] ')) + '配置有误，请更改配置')


if __name__ == '__main__':
    itchat.check_login()
    itchat.auto_login(hotReload=True, enableCmdQR=2)
    if int(config.shield_mode):
        print(str(datetime.now().strftime('[%Y.%m.%d %H:%M:%S] ')) + '白名单模式：群聊' + str(config.whitelist) + '以及非群聊的消息将会推送')
    else:
        print(str(datetime.now().strftime('[%Y.%m.%d %H:%M:%S] ')) + '黑名单模式：' + str(config.blacklist) + '的消息将不会推送')
    pool = Pool(processes=1)
    pool.apply_async(config_update, callback=forcequit)
    pool.close()
    itchat.run()
