import requests
from requests.packages import urllib3
from datetime import datetime
import re
import itchat.content

# 你的消息接收别名
# 例如aliasname = 'line'
aliasname = '推送别名'
# 你的消息推送黑名单,可为群名或者好友名，理论上可以按照格式无限添加
# 例如blacklist = ["相亲相爱一家人","法外狂徒张三","..."]
blacklist = ["black1", "balck2", "balck3"]
#消息推送接口
#旧接口，腾讯云，服务器在北京，延时低，无推送量限制，2023年2月起失效
interface = 'https://tdtt.top/send'
#新接口，Cloudflare平台，服务器在美国，延时高，日总推送量5万条，理论永久有效
#interface = 'https://send.tdtt.top'

urllib3.disable_warnings()

@itchat.msg_register([itchat.content.TEXT, itchat.content.FRIENDS, itchat.content.MUSICSHARE, itchat.content.UNDEFINED, itchat.content.PICTURE,
                        itchat.content.RECORDING, itchat.content.ATTACHMENT, itchat.content.VIDEO, itchat.content.CARD, itchat.content.EMOTICON,
                        itchat.content.VOIP, itchat.content.WEBSHARE, itchat.content.LOCATIONSHARE, itchat.content.CHATHISTORY, itchat.content.SHARING,
                        itchat.content.TRANSFER, itchat.content.REDENVELOPE, itchat.content.MINIPROGRAM, itchat.content.MAP], isFriendChat=True, isGroupChat=True)


def simple_reply(msg):
    name = msg.user.nickName if msg.user.remarkName == '' else msg.user.remarkName
    if name not in blacklist:
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
            itchat.content.VOIP: '[通话邀请] 请及时打开微信',
            itchat.content.ATTACHMENT: '[文件]' + str(msg.get('Text')),
            itchat.content.CARD: '[好友名片]' + str(msg.get('Text')),
            itchat.content.MUSICSHARE: '[音乐]' + str(msg.get('Text')),
            itchat.content.MAP: '[位置分享]' + str(''.join(re.findall(r'poiname="(.*?)" poiid', str(msg.get('OriContent'))))),
            itchat.content.WEBSHARE: '[链接]' + str(msg.get('Text')),
            itchat.content.MINIPROGRAM: '[小程序]' + str(msg.get('Text')),
            itchat.content.SHARING: '[未知卡片消息]: AppMsgType=' + str(msg.get('Text')),
            itchat.content.UNDEFINED: '[未知消息类型]: MsgType=' + str(msg.get('Text')) }.get(msg['Type'])
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' ' + str(name) + ': ' + str(typesymbol))
        requests.get(str(interface), params={'title': '微信 ' + str(name), 'content': str(typesymbol), 'alias': str(aliasname)}, verify=False)

if __name__ == '__main__':
    itchat.check_login()
    itchat.auto_login(hotReload=True, enableCmdQR=2)
    itchat.run()
