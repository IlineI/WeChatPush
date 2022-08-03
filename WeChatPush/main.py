import itchat.content
import requests
import re
from requests.packages import urllib3
from datetime import datetime

urllib3.disable_warnings()

@itchat.msg_register([itchat.content.TEXT, itchat.content.FRIENDS, itchat.content.MUSICSHARE,
                        itchat.content.UNDEFINED, itchat.content.PICTURE, itchat.content.RECORDING,
                        itchat.content.ATTACHMENT, itchat.content.VIDEO, itchat.content.CARD,
                        itchat.content.EMOTICON, itchat.content.VOIP, itchat.content.WEBSHARE,
                        itchat.content.LOCATIONSHARE, itchat.content.CHATHISTORY, itchat.content.SHARING,
                        itchat.content.SERVICENOTIFICATION, itchat.content.TRANSFER, itchat.content.MAP,
                        itchat.content.REDENVELOPE, itchat.content.MINIPROGRAM], isFriendChat=True, isGroupChat=True)


def simple_reply(msg):
    config = open(os.path.split(os.path.realpath(__file__))[0] + '/config.txt', 'r', encoding='utf-8')
    for line in config:
        if (re.findall(r'^separate_push = \'(.*?)\'', line)) != []:
            separate_push = str(''.join(re.findall(r'^separate_push = \'(.*?)\'', line)))
        elif (re.findall(r'^chat_alias = \'(.*?)\'', line)) != []:
            chat_alias = str(''.join(re.findall(r'^chat_alias = \'(.*?)\'', line)))
        elif (re.findall(r'^VoIP_alias = \'(.*?)\'', line)) != []:
            VoIP_alias = str(''.join(re.findall(r'^VoIP_alias = \'(.*?)\'', line)))
        elif (''.join(re.findall(r'^blacklist = \[(.*?)\]', line))) != '':
            blacklist = '[' + str(''.join(re.findall(r'^blacklist = \[(.*?)\]', line))) + ']'
        elif (re.findall(r'^interface = \'(.*?)\'', line)) != []:
            interface = str(''.join(re.findall(r'^interface = \'(.*?)\'', line)))
    config.close()
    if msg.get('NickName') not in blacklist:
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
            itchat.content.VOIP: '[通话邀请]请及时打开微信查看',
            itchat.content.ATTACHMENT: '[文件]' + str(msg.get('Text')),
            itchat.content.CARD: '[名片]' + str(msg.get('Text')),
            itchat.content.MUSICSHARE: '[音乐]' + str(msg.get('Text')),
            itchat.content.SERVICENOTIFICATION: str(msg.get('Text')),
            itchat.content.MAP: '[位置分享]' + str(msg.get('Text')),
            itchat.content.WEBSHARE: '[链接]' + str(msg.get('Text')),
            itchat.content.MINIPROGRAM: '[小程序]' + str(msg.get('Text')),
            itchat.content.UNDEFINED: '[未知消息类型]: MsgType=' + str(msg.get('Text')) }.get(msg['Type'])
        voip_alias = VoIP_alias if separate_push != 'false' and VoIP_alias != '' else chat_alias
        alias = voip_alias if msg.get('Type') == 'Voip' else chat_alias
        requests.get(str(interface), params={'title': '微信 ' + str(msg.get('Name')), 'content': str(typesymbol), 'alias': str(alias)}, verify=False)
        typesymbol = '[未知卡片消息]: AppMsgType=' + str(msg.get('Text')) if msg.get('Type') == 'Sharing' else typesymbol
        print(datetime.now().strftime('%Y.%m.%d %H:%M:%S') + ' ' + str(msg.get('Name')) + ': ' + str(typesymbol))

if __name__ == '__main__':
    itchat.check_login()
    itchat.auto_login(hotReload=True, enableCmdQR=2)
    itchat.run()
