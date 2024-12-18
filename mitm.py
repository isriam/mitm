#!/usr/bin/env python3
from mitmproxy import proxy
from mitmproxy import options
from mitmproxy.tools.dump import DumpMaster
import json
import os


class Aboutv2:
    def __init__(self):
        complete = False

    def response(self, flow):
        if flow.response and flow.response.content:
            # print(vars(flow.request))
            # print(flow.request.path)
            if '/ext/dragonsong/event/about_v2' in flow.request.path:
                print('about_v2', flow.request.path)
                about_v2_raw = flow.response.content.decode("utf-8")
                about_v2 = json.loads(about_v2_raw)
                with open("/root/.mitmproxy/wardragons/about_v2.txt", "w") as file:
                    json.dump(about_v2, file)
                os.chmod("/root/.mitmproxy/wardragons/about_v2.txt", 0o744)
        pass


def start():
    myaddon = Aboutv2()
    opts = options.Options(listen_host='0.0.0.0', listen_port=3124)
    pconf = proxy.config.ProxyConfig(opts)
    m = DumpMaster(opts)
    m.addons.add(myaddon)

    try:
        m.run()
    except KeyboardInterrupt:
        m.shutdown()

start()