# 若程序正在后台运行，则更改配置后实时生效

# 是否将消息通知与通话邀请分开推送
# 若此项不为false，则需要消息接收以及FarPush两个软件，第一个用来接收消息通知，第二个用来接收通话邀请
# 好处是可以将FarPush的通知声设置为电话铃声，起到强提醒的作用
separate_push = 'false'

# 只能填写其中一个，不然会出错(好像也可以同时使用
# 消息接收设置的别名
chat_alias = ''
# WirePusher里面获取的id
wire_id = ''

# FarPush设置的regID，若separate_push为false则无需填写
# 若separate_push不为false而此项未填写，则强制使用消息接收来接收通话邀请
VoIP_regID = ''

# 消息推送黑名单,可以是好友昵称或原群名，不是好友备注或群备注，理论上可以按照格式无限添加
# 例如blacklist = ['相亲相爱一家人', '法外狂徒张三', '...']
blacklist = ['blacklist']

# 消息接收的接口
# 旧接口，腾讯云，服务器在北京，延时低，无推送量限制，2023年2月起失效
chat_interface = 'https://tdtt.top/send'
# 新接口，Cloudflare平台，服务器在美国，延时高，日总推送量5万条，理论永久有效
#chat_interface = 'https://send.tdtt.top'

# FarPush的接口
VoIP_interface = 'http://119.3.139.212:9090/PushWeChatMes'
