# 若程序正在后台运行，则更改配置后实时生效

# 可选将普通消息与通话邀请分开推送
# 好处是可以将接收通话邀请的APP的通知声设置为电话铃声，起到强提醒的作用
# 特例：WirePusher因为支持多通知类别，所以可以实现单应用设置双通知声

# 选择推送途径，1为消息接收，2为FarPush，3为WirePusher
# 其中，1仅支持MiPush，2支持多种推送方式，3仅支持FCM但点击通知后会跳转至微信
# 普通消息推送途径
chat_push = '1'
# 通话邀请推送途径
VoIP_push = '1'
# 理论MiPush也支持点击通知跳转，但需要开发者在接口服务器中将extra.notify_effect设为3，并获取POST或GET的extra.web_uri参数
# 但目前1、2接口并没有适配，所以无法跳转

# 以下三项请根据上述两项的值选择性填写
# 消息接收设置的别名
tdtt_alias = ''
# FarPush设置的regID
FarPush_regID = ''
# WirePusher获取的ID
WirePusher_ID = ''

# 选择FarPush的推送服务
# 0为MiPush，1为OPPO Push，2为Huawei Push，4为腾讯推送
# 3为FCM，服务器暂未建立，无法使用
FarPush_Phone_Type = '0'

# 免打扰的消息不会通知，此外，你还可以设置黑名单来屏蔽某些不是免打扰的消息的通知
# 新设置免打扰的群聊必须要重新登录一次才会生效（是重新登录微信而不是重新运行程序）
# 这是itchat的问题，私聊不受此限制，404年内会修复这个bug
# 可以是好友昵称或原群名，不是好友备注或群备注，理论上可以按照格式无限添加
# 例如blacklist = ['相亲相爱一家人', '法外狂徒张三', '...']
blacklist = ['blacklist']

# 消息接收的接口
# 旧接口，腾讯云，服务器在北京，延时低，无推送量限制，2023年2月起失效
tdtt_interface = 'https://tdtt.top/send'
# 新接口，Cloudflare平台，服务器在美国，延时高，日总推送量5万条，理论永久有效
#tdtt_interface = 'https://send.tdtt.top'

# FarPush的接口
FarPush_interface = 'http://119.3.139.212:9090/PushWeChatMes'

#WirePusher的接口
WirePusher_interface = 'https://wirepusher.com/send'
