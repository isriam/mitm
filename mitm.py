from mitmproxy.options import Options
from mitmproxy.proxy.config import ProxyConfig
from mitmproxy.proxy.server import ProxyServer
from mitmproxy.tools.dump import DumpMaster
import os, sys, re, datetime, json

class Addon(object):
def __init__(self):
    pass

def request(self, flow):
    # examine request here
    if flow.request.host == 'testserver.net':
        flow.request.host = 'mynewserver.com'
        print('New try ---> Bypassing.')

def response(self, flow):
    # examine response here
    pass


if __name__ == "__main__":

options = Options(listen_host='0.0.0.0', listen_port=8080, certs=['*=mitmproxy.pem'])
m = DumpMaster(options, with_termlog=False, with_dumper=False)
config = ProxyConfig(options)

m.server = ProxyServer(config)
m.addons.add(Addon())

try:
    print('Redirection active.')
    m.run()
except KeyboardInterrupt:
    m.shutdown()