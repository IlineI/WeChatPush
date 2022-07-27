import requests
import itchat
import itchat.content
import itchat.config
from requests.packages import urllib3

# 你的消息接收别名
# 例如aliasname = 'line'
aliasname = ''
@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    print(msg.user.nickName + " say : " + msg.text)
    urllib3.disable_warnings()
    requests.get('https://tdtt.top/send',params={'title': '%s' % (msg.user.nickName), 'content': '%s' % (msg.text), 'alias': '%s' % (aliasname)},verify=False)


@itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
def text_reply(msg):
    urllib3.disable_warnings()
    requests.get('https://tdtt.top/send',params={'title': '%s' % (msg.user.nickName), 'content': '%s' % (msg.text), 'alias': '%s' % (aliasname)},verify=False)

@itchat.msg_register(['Picture', 'Recording', 'Attachment', 'Video'])
def download_files(msg):
    urllib3.disable_warnings()
    #下载媒体文件，服务器硬盘够大可选
    # msg.download(msg.fileName)
    typeSymbol = {
        'Picture': '一张图片',
        'Recording': '一个音频',
        'Attachment': '一个文件',
        'Video': '一个视频', }.get(msg.type, 'fil')
    print(msg.user.nickName + " 发送了 " + typeSymbol)
    requests.get('https://tdtt.top/send',params={'title': '%s' % (msg.user.nickName), 'content': '发送了%s' % (typeSymbol), 'alias': '%s' % (aliasname)},verify=False)
    

if __name__ == '__main__':
    itchat.check_login()
    itchat.auto_login(hotReload=True,enableCmdQR=2)
    itchat.run()
