import sys, io
sys.setdefaultencoding("utf-8")
import os, platform
import random

VERSION = '1.5.0.dev'

BASE_URL = 'http://login.weixin.qq.com'
OS = platform.system()  # Windows, Linux, Darwin
DIR = os.getcwd()
DEFAULT_QR = str((os.path.dirname(os.path.split(os.path.realpath(__file__))[0])).replace('\\', '/')) + '/QR.png'
TIMEOUT = (10, 60)

USER_AGENTS = ['Mozilla/5.0 (Macintosh) AppleWebKit/34.7 (KHTML, like Gecko) Firefox/47.0 Safari/174.10',
'Mozilla/5.0 (Macintosh) AppleWebKit/3.11 (KHTML, like Gecko) Edge/16.11712 Safari/196.49',
'Mozilla/4.0 (Macintosh) AppleWebKit/83.67 (KHTML, like Gecko) Edge/15.12545 Safari/268.27',
'Mozilla/5.0 (Macintosh) AppleWebKit/30.98 (KHTML, like Gecko) Edge/17.18242 Safari/146.9',
'Mozilla/5.0 (Macintosh) AppleWebKit/62.91 (KHTML, like Gecko) Chrome/70.3.2466.421 Safari/192.97',
'Mozilla/4.0 (Macintosh) AppleWebKit/57.78 (KHTML, like Gecko) Firefox/61.0 Safari/501.68',
'Mozilla/4.0 (Macintosh) AppleWebKit/58.18 (KHTML, like Gecko) Firefox/35.0 Safari/485.55',
'Mozilla/5.0 (Macintosh) AppleWebKit/6.27 (KHTML, like Gecko) Firefox/21.0 Safari/271.4',
'Mozilla/5.0 (Macintosh) AppleWebKit/51.95 (KHTML, like Gecko) Edge/17.12531 Safari/367.29',
'Mozilla/4.0 (Macintosh) AppleWebKit/18.68 (KHTML, like Gecko) Firefox/48.0 Safari/421.53',
'Mozilla/4.0 (Macintosh) AppleWebKit/28.84 (KHTML, like Gecko) Firefox/29.0 Safari/136.63',
'Mozilla/5.0 (Macintosh) AppleWebKit/61.93 (KHTML, like Gecko) Chrome/57.2.3680.398 Safari/269.71',
'Mozilla/4.0 (Macintosh) AppleWebKit/95.83 (KHTML, like Gecko) Edge/13.19782 Safari/193.98',
'Mozilla/4.0 (Macintosh) AppleWebKit/24.16 (KHTML, like Gecko) Edge/18.12330 Safari/341.70',
'Mozilla/5.0 (Macintosh) AppleWebKit/40.97 (KHTML, like Gecko) Firefox/42.0 Safari/471.16',
'Mozilla/4.0 (Macintosh) AppleWebKit/100.84 (KHTML, like Gecko) Edge/16.15933 Safari/579.17',
'Mozilla/5.0 (Macintosh) AppleWebKit/18.21 (KHTML, like Gecko) Edge/14.10534 Safari/474.75',
'Mozilla/5.0 (Macintosh) AppleWebKit/51.28 (KHTML, like Gecko) Chrome/69.2.1396.378 Safari/526.95',
'Mozilla/4.0 (Macintosh) AppleWebKit/87.19 (KHTML, like Gecko) Firefox/62.0 Safari/534.24',
'Mozilla/4.0 (Macintosh) AppleWebKit/10.87 (KHTML, like Gecko) Chrome/59.2.4082.388 Safari/498.12',
'Mozilla/4.0 (Macintosh) AppleWebKit/76.18 (KHTML, like Gecko) Firefox/63.0 Safari/463.66',
'Mozilla/5.0 (Macintosh) AppleWebKit/15.52 (KHTML, like Gecko) Firefox/29.0 Safari/462.75',
'Mozilla/4.0 (Macintosh) AppleWebKit/61.12 (KHTML, like Gecko) Firefox/38.0 Safari/502.18',
'Mozilla/5.0 (Macintosh) AppleWebKit/93.6 (KHTML, like Gecko) Chrome/61.1.1684.296 Safari/452.10',
'Mozilla/4.0 (Macintosh) AppleWebKit/0.94 (KHTML, like Gecko) Firefox/53.0 Safari/398.3',
'Mozilla/4.0 (Macintosh) AppleWebKit/10.2 (KHTML, like Gecko) Firefox/48.0 Safari/556.73',
'Mozilla/4.0 (Macintosh) AppleWebKit/57.84 (KHTML, like Gecko) Firefox/32.0 Safari/221.6',
'Mozilla/4.0 (Macintosh) AppleWebKit/23.10 (KHTML, like Gecko) Edge/15.12439 Safari/549.84',
'Mozilla/4.0 (Macintosh) AppleWebKit/17.40 (KHTML, like Gecko) Firefox/28.0 Safari/308.50',
'Mozilla/4.0 (Macintosh) AppleWebKit/73.2 (KHTML, like Gecko) Chrome/71.2.4787.263 Safari/383.99',
'Mozilla/4.0 (Macintosh) AppleWebKit/78.41 (KHTML, like Gecko) Firefox/46.0 Safari/195.2',
'Mozilla/4.0 (Macintosh) AppleWebKit/91.11 (KHTML, like Gecko) Chrome/50.3.3098.136 Safari/393.3',
'Mozilla/5.0 (Macintosh) AppleWebKit/38.94 (KHTML, like Gecko) Chrome/56.1.3412.293 Safari/312.68',
'Mozilla/5.0 (Macintosh) AppleWebKit/40.87 (KHTML, like Gecko) Firefox/37.0 Safari/165.22',
'Mozilla/5.0 (Macintosh) AppleWebKit/88.79 (KHTML, like Gecko) Chrome/60.2.3895.335 Safari/219.84',
'Mozilla/5.0 (Macintosh) AppleWebKit/2.64 (KHTML, like Gecko) Chrome/54.1.3625.443 Safari/441.43',
'Mozilla/5.0 (Macintosh) AppleWebKit/64.45 (KHTML, like Gecko) Firefox/47.0 Safari/492.73',
'Mozilla/4.0 (Macintosh) AppleWebKit/77.21 (KHTML, like Gecko) Edge/16.16271 Safari/501.59',
'Mozilla/4.0 (Macintosh) AppleWebKit/36.14 (KHTML, like Gecko) Edge/13.13427 Safari/586.53',
'Mozilla/4.0 (Macintosh) AppleWebKit/88.83 (KHTML, like Gecko) Firefox/48.0 Safari/555.47',
'Mozilla/5.0 (Macintosh) AppleWebKit/71.96 (KHTML, like Gecko) Firefox/58.0 Safari/566.39',
'Mozilla/5.0 (Macintosh) AppleWebKit/8.71 (KHTML, like Gecko) Firefox/34.0 Safari/243.86',
'Mozilla/4.0 (Macintosh) AppleWebKit/48.37 (KHTML, like Gecko) Firefox/45.0 Safari/595.27',
'Mozilla/4.0 (Macintosh) AppleWebKit/30.75 (KHTML, like Gecko) Firefox/25.0 Safari/309.21',
'Mozilla/4.0 (Macintosh) AppleWebKit/72.88 (KHTML, like Gecko) Firefox/47.0 Safari/324.38',
'Mozilla/4.0 (Macintosh) AppleWebKit/74.87 (KHTML, like Gecko) Firefox/62.0 Safari/225.33',
'Mozilla/4.0 (Macintosh) AppleWebKit/24.21 (KHTML, like Gecko) Edge/14.15212 Safari/587.76',
'Mozilla/4.0 (Macintosh) AppleWebKit/68.31 (KHTML, like Gecko) Edge/16.10058 Safari/440.26',
'Mozilla/4.0 (Macintosh) AppleWebKit/45.95 (KHTML, like Gecko) Firefox/42.0 Safari/592.69',
'Mozilla/5.0 (Macintosh) AppleWebKit/13.17 (KHTML, like Gecko) Chrome/72.1.1015.395 Safari/270.59']

USER_AGENT = random.choice(USER_AGENTS)

UOS_PATCH_CLIENT_VERSION = '2.0.0'
UOS_PATCH_EXTSPAM = 'Go8FCIkFEokFCggwMDAwMDAwMRAGGvAESySibk50w5Wb3uTl2c2h64jVVrV7gNs06GFlWplHQbY/5FfiO++1yH4ykCyNPWKXmco+wfQzK5R98D3so7rJ5LmGFvBLjGceleySrc3SOf2Pc1gVehzJgODeS0lDL3/I/0S2SSE98YgKleq6Uqx6ndTy9yaL9qFxJL7eiA/R3SEfTaW1SBoSITIu+EEkXff+Pv8NHOk7N57rcGk1w0ZzRrQDkXTOXFN2iHYIzAAZPIOY45Lsh+A4slpgnDiaOvRtlQYCt97nmPLuTipOJ8Qc5pM7ZsOsAPPrCQL7nK0I7aPrFDF0q4ziUUKettzW8MrAaiVfmbD1/VkmLNVqqZVvBCtRblXb5FHmtS8FxnqCzYP4WFvz3T0TcrOqwLX1M/DQvcHaGGw0B0y4bZMs7lVScGBFxMj3vbFi2SRKbKhaitxHfYHAOAa0X7/MSS0RNAjdwoyGHeOepXOKY+h3iHeqCvgOH6LOifdHf/1aaZNwSkGotYnYScW8Yx63LnSwba7+hESrtPa/huRmB9KWvMCKbDThL/nne14hnL277EDCSocPu3rOSYjuB9gKSOdVmWsj9Dxb/iZIe+S6AiG29Esm+/eUacSba0k8wn5HhHg9d4tIcixrxveflc8vi2/wNQGVFNsGO6tB5WF0xf/plngOvQ1/ivGV/C1Qpdhzznh0ExAVJ6dwzNg7qIEBaw+BzTJTUuRcPk92Sn6QDn2Pu3mpONaEumacjW4w6ipPnPw+g2TfywJjeEcpSZaP4Q3YV5HG8D6UjWA4GSkBKculWpdCMadx0usMomsSS/74QgpYqcPkmamB4nVv1JxczYITIqItIKjD35IGKAUwAA=='

# if show self send mes
SELF_MES = False
