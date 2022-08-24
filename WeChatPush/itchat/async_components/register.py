import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="urf-8")
import logging, traceback, threading
import os
from datetime import datetime

try:
    import Queue
except ImportError:
    import queue as Queue  # type: ignore

from ..log import set_logging
from ..utils import test_connect
from ..storage import templates

logger = logging.getLogger('itchat')


def load_register(core):
    core.auto_login       = auto_login
    core.configured_reply = configured_reply
    core.msg_register     = msg_register
    core.run              = run


async def auto_login(self, hotReload=False, enableCmdQR=False, picDir=None, qrCallback=None, loginCallback=None, exitCallback=None,
                    statusStorageDir=str((os.path.dirname(os.path.split(os.path.realpath(__file__))[0])).replace('\\', '/')) + '/itchat.pkl'):
    if not test_connect():
        print(str(datetime.now().strftime('[%Y.%m.%d %H:%M:%S] ')) + '无法访问互联网或微信域名，程序停止运行。')
        sys.exit()
    self.useHotReload = hotReload
    self.hotReloadDir = statusStorageDir
    if hotReload:
        if await self.load_login_status(statusStorageDir,
                loginCallback=loginCallback, exitCallback=exitCallback):
            return
        await self.login(enableCmdQR=enableCmdQR, picDir=picDir, qrCallback=qrCallback, loginCallback=loginCallback, exitCallback=exitCallback)
        await self.dump_login_status(statusStorageDir)
    else:
        await self.login(enableCmdQR=enableCmdQR, picDir=picDir, qrCallback=qrCallback, loginCallback=loginCallback, exitCallback=exitCallback)

async def configured_reply(self):
    ''' determine the type of message and reply if its method is defined
        however, I use a strange way to determine whether a msg is from massive platform
        I haven't found a better solution here
        The main problem I'm worrying about is the mismatching of new friends added on phone
        If you have any good idea, pleeeease report an issue. I will be more than grateful.
    '''
    try:
        msg = self.msgList.get(timeout=1)
    except Queue.Empty:
        pass
    else:
        if isinstance(msg['User'], templates.User):
            replyFn = self.functionDict['FriendChat'].get(msg['Type'])
        elif isinstance(msg['User'], templates.MassivePlatform):
            replyFn = self.functionDict['MpChat'].get(msg['Type'])
        elif isinstance(msg['User'], templates.Chatroom):
            replyFn = self.functionDict['GroupChat'].get(msg['Type'])
        if replyFn is None:
            r = None
        else:
            try:
                r = replyFn(msg)
                if r is not None:
                    await self.send(r, msg.get('FromUserName'))
            except:
                logger.warning(traceback.format_exc())

def msg_register(self, msgType, isFriendChat=False, isGroupChat=False, isMpChat=False):
    ''' a decorator constructor
        return a specific decorator based on information given '''
    if not (isinstance(msgType, list) or isinstance(msgType, tuple)):
        msgType = [msgType]
    def _msg_register(fn):
        for _msgType in msgType:
            if isFriendChat:
                self.functionDict['FriendChat'][_msgType] = fn
            if isGroupChat:
                self.functionDict['GroupChat'][_msgType] = fn
            if isMpChat:
                self.functionDict['MpChat'][_msgType] = fn
            if not any((isFriendChat, isGroupChat, isMpChat)):
                self.functionDict['FriendChat'][_msgType] = fn
        return fn
    return _msg_register

async def run(self, debug=False, blockThread=True):
    print(str(datetime.now().strftime('[%Y.%m.%d %H:%M:%S] ')) + '登录成功，开始接收消息')
    if debug:
        set_logging(loggingLevel=logging.DEBUG)
    async def reply_fn():
        try:
            while self.alive:
                await self.configured_reply()
        except KeyboardInterrupt:
            if self.useHotReload:
                await self.dump_login_status()
            self.alive = False
            print(str(datetime.now().strftime('[%Y.%m.%d %H:%M:%S] ')) + '由于键盘输入^C（ctrl+C），程序强制停止运行')
    if blockThread:
        await reply_fn()
    else:
        replyThread = threading.Thread(target=reply_fn)
        replyThread.setDaemon(True)
        replyThread.start()
