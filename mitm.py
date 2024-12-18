#!/usr/bin/env python3
from mitmproxy.options import Options
from mitmproxy.proxy.config import ProxyConfig
from mitmproxy.proxy.server import ProxyServer
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


class ProxyMaster(DumpMaster):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        try:
            DumpMaster.run(self)
        except KeyboardInterrupt:
            self.shutdown()


if __name__ == "__main__":
    options = Options(listen_host='0.0.0.0', listen_port=3124, http2=True)
    config = ProxyConfig(options)
    master = ProxyMaster(options, with_termlog=False, with_dumper=False)
    master.server = ProxyServer(config)
    master.addons.add(Aboutv2())
    master.run()