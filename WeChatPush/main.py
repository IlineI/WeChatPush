import itchat.content
import requests
import importlib
import time
import os
from requests.packages import urllib3
from datetime import datetime
from multiprocessing import Pool, Manager


def config_update(value):
    while 1:
        try:
            importlib.reload(config)
        except:
            print(str(datetime.now().strftime('[%Y.%m.%d %H:%M:%S] ')) + '配置获取异常,请检查配置文件是否存在/权限是否正确/语法是否有误')
            print('程序终止运行')
            break
        shield_mode_update = '0'
        newcfg = {'chat_push': str(config.chat_push), 'VoIP_push': str(config.VoIP_push),
                    'tdtt_alias': str(config.tdtt_alias), 'FarPush_regID': str(config.FarPush_regID),
                    'WirePusher_ID': str(config.WirePusher_ID), 'FarPush_Phone_Type': str(config.FarPush_Phone_Type),
                    'shield_mode': str(config.shield_mode), 'blacklist': list(config.blacklist),
                    'whitelist': list(config.whitelist), 'tdtt_interface': str(config.tdtt_interface), 
                    'FarPush_interface': str(config.FarPush_interface), 'WirePusher_interface': str(config.WirePusher_interface)}
        for a in value.keys():
            if str(a) == 'shield_mode':
                if newcfg.get('shield_mode') != value.get('shield_mode'):
                    if int(newcfg.get('shield_mode')):
                        print(str(datetime.now().strftime('[%Y.%m.%d %H:%M:%S] ')) + '切换为白名单模式：群聊' + str(newcfg.get('whitelist')) + '以及非群聊的消息将会推送')
                    else:
                        print(str(datetime.now().strftime('[%Y.%m.%d %H:%M:%S] ')) + '切换为黑名单模式：' + str(newcfg.get('blacklist')) + '的消息将不会推送')
                    shield_mode_update = '1'
            elif str(a) == 'whitelist':
                if not int(shield_mode_update) and newcfg.get(a) != value.get(a) and int(newcfg.get('shield_mode')):
                    print(str(datetime.now().strftime('[%Y.%m.%d %H:%M:%S] ')) + '白名单更改：群聊' + str(newcfg.get(a)) + '以及非群聊的消息将会推送')
            elif str(a) == 'blacklist':
                if not int(shield_mode_update) and newcfg.get(a) != value.get(a) and not int(newcfg.get('shield_mode')):
                    print(str(datetime.now().strftime('[%Y.%m.%d %H:%M:%S] ')) + '黑名单更改：' + str(newcfg.get(a)) + '的消息将不会推送')
            elif str(value.get(a)) != str(newcfg.get(a)):
                print(str(datetime.now().strftime('[%Y.%m.%d %H:%M:%S] ')) + a + '更改,新' + a + '值为' + newcfg.get(a))
        value.update(newcfg)
        time.sleep(1)


def forcequit(msg):
    print('发生错误，程序强制停止运行')
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
    notify = 0
    if int(value.get('shield_mode')):
        if not int(msg.get('ChatRoom')) or str(msg.get('NickName')) in list(value.get('whitelist')): # 白名单模式，白名单群消息放行
            notify = 1
    elif str(msg.get('NickName')) not in list(value.get('blacklist')):
        notify =  1
    if int(notify) and not int(msg.get('NotifyCloseContact')):
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
            if str(value.get('VoIP_push')) == '1' and str(value.get('tdtt_alias')) != '':
                data_send(str(value.get('tdtt_interface')), title='微信 ' + str(Name), content=str(typesymbol), alias=str(value.get('tdtt_alias')))
            elif str(value.get('VoIP_push')) == '2' and str(value.get('FarPush_regID')) != '':
                data_send(str(value.get('FarPush_interface')), title='微信 ' + str(Name), content=str(typesymbol), regID=str(value.get('FarPush_regID')), phone=str(value.get('FarPush_Phone_Type')), through='0')
            elif str(value.get('VoIP_push')) == '3' and str(value.get('WirePusher_ID')) != '':
                data_send(str(value.get('WirePusher_interface')), title='微信 ' + str(Name), message=str(typesymbol), id=str(value.get('WirePusher_ID')), type='WeChat_VoIP', action='weixin://')
            else:
                print(str(datetime.now().strftime('[%Y.%m.%d %H:%M:%S] ')) + '配置有误，请更改配置')
        else:
            if str(value.get('chat_push')) == '1' and str(value.get('tdtt_alias')) != '':
                data_send(str(value.get('tdtt_interface')), title='微信 ' + str(Name), content=str(typesymbol), alias=str(value.get('tdtt_alias')))
            elif str(value.get('chat_push')) == '2' and str(value.get('FarPush_regID')) != '':
                data_send(str(value.get('FarPush_interface')), title='微信 ' + str(Name), content=str(typesymbol), regID=str(value.get('FarPush_regID')), phone=str(value.get('FarPush_Phone_Type')), through='0')
            elif str(value.get('chat_push')) == '3' and str(value.get('WirePusher_ID')) != '':
                data_send(str(value.get('WirePusher_interface')), title='微信 ' + str(Name), message=str(typesymbol), id=str(value.get('WirePusher_ID')), type='WeChat_VoIP', action='weixin://')
            else:
                print(str(datetime.now().strftime('[%Y.%m.%d %H:%M:%S] ')) + '配置有误，请更改配置')


if __name__ == '__main__':
    try:
        import config
    except:
        print(str(datetime.now().strftime('[%Y.%m.%d %H:%M:%S] ')) + '配置获取异常,请检查配置文件是否存在/权限是否正确/语法是否有误')
        print('程序终止运行')
        os._exit(0)
    urllib3.disable_warnings()
    value = Manager().dict()
    value.update({'chat_push': str(config.chat_push), 'VoIP_push': str(config.VoIP_push),
                    'tdtt_alias': str(config.tdtt_alias), 'FarPush_regID': str(config.FarPush_regID),
                    'WirePusher_ID': str(config.WirePusher_ID), 'FarPush_Phone_Type': str(config.FarPush_Phone_Type),
                    'shield_mode': str(config.shield_mode), 'blacklist': list(config.blacklist),
                    'whitelist': list(config.whitelist), 'tdtt_interface': str(config.tdtt_interface), 
                    'FarPush_interface': str(config.FarPush_interface), 'WirePusher_interface': str(config.WirePusher_interface)})
    itchat.check_login()
    itchat.auto_login(hotReload=True, enableCmdQR=2)
    if int(value.get('shield_mode')):
        print(str(datetime.now().strftime('[%Y.%m.%d %H:%M:%S] ')) + '白名单模式：群聊' + str(value.get('whitelist')) + '以及非群聊的消息将会推送')
    else:
        print(str(datetime.now().strftime('[%Y.%m.%d %H:%M:%S] ')) + '黑名单模式：' + str(value.get('blacklist')) + '的消息将不会推送')
    pool = Pool(processes = 1)
    pool.apply_async(config_update, args=(value, ), callback=forcequit, error_callback=forcequit)
    pool.close()
    itchat.run()
