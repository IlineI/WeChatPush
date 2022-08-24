# 是否启用协程（异步），0为禁用，其他数为启用，更改后需要重新运行程序
# 如果你不了解协程的作用，保持禁用即可
async_components = '0'


# 以下所有配置更改后实时生效

# 可选将普通消息与通话邀请分开推送
# 好处是可以将接收通话邀请的APP的通知声设置为电话铃声，起到强提醒的作用
# 特例：WirePusher因为支持多通知类别，所以可以实现单应用设置双通知声

# 选择推送途径，1为消息接收，2为FarPush，3为WirePusher
# 其中，1仅支持MiPush，2支持多种推送方式，3仅支持FCM但点击通知后会跳转至微信
# 普通消息推送途径
chat_push = '1'
# 通话邀请推送途径
VoIP_push = '1'

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

# 免打扰的消息不会通知，此外，你还可以设置黑名单/白名单来屏蔽某些不是免打扰消息的通知
# 新设置免打扰的群聊必须要重新登录一次才会生效（是重新登录微信而不是重新运行程序）
# 这是itchat的问题，私聊不受此限制，114514年内会修复这个BUG

# 选择黑名单模式/白名单模式，0为黑名单模式，其他数为白名单模式
# 黑名单模式可以屏蔽在黑名单内的私聊或群聊消息
# 白名单模式可以屏蔽所有不在白名单的群聊消息，非群聊消息不受影响
shield_mode = '0'

# 黑名单模式，可以是好友昵称或原群名，不是好友备注或群备注，可以无限添加
# 名字用英文单引号引起来，名字之间用英文逗号隔开
blacklist = ['blacklist1', 'blacklist2']
# 白名单模式，可以是原群名，不是群备注，可以无限添加
# 名字用英文单引号引起来，名字之间用英文逗号隔开
whitelist = ['whitelist1', 'whitelist2']

# 消息接收的接口
# 旧接口，腾讯云，服务器在北京，延时低，无推送量限制，2023年2月起失效
tdtt_interface = 'http://43.138.103.64:7890'
# 新接口，Cloudflare平台，服务器在美国，延时高，日总推送量5万条，理论永久有效
#tdtt_interface = 'https://send.tdtt.top'

# FarPush的接口
FarPush_interface = 'http://119.3.139.212:9090/PushWeChatMes'

#WirePusher的接口
WirePusher_interface = 'https://wirepusher.com/send'
