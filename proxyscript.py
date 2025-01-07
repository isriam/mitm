from mitmproxy import http, ctx
import json
import os
import re

class SavePackets:
    def __init__(self):
        self.counter = 0

    def response(self, flow: http.HTTPFlow):
        if flow.response and flow.response.content:
            #print(vars(flow.request))
            #print(flow.request.path)
            if '/ext/dragonsong/event/about_v2' in flow.request.path:
                print('about_v2', flow.request.path)
                about_v2_raw = flow.response.content.decode("utf-8")
                about_v2 = json.loads(about_v2_raw)
                parsed = re.search(r'(?P<player_id>player_id=)(?P<pgid>[a-zA-Z0-9]+)', flow.request.path, re.M)
                pgid = parsed.group(2)
                with open(f"/root/.mitmproxy/wardragons/about_v2.txt", "w") as file:
                    json.dump(about_v2, file)
                os.chmod("/root/.mitmproxy/wardragons/about_v2.txt", 0o744)
                about_completed = True
                self.counter += 1
            if '/dragons/event/current' in flow.request.path:
                print('params', flow.request.path)
                params = flow.response.content.decode("utf-8")
                parsed = re.search(r'(?P<player_id>player_id=)(?P<pgid>[a-zA-Z0-9]+)', flow.request.path, re.M)
                pgid = parsed.group(2)
                with open(f"/root/.mitmproxy/wardragons/params.txt" , "w") as file:
                    file.write(params)
                os.chmod("/root/.mitmproxy/wardragons/params.txt", 0o744)
                params_completed = True
                self.counter += 1
            #if '/ext/dragonsong/world/get_params' in flow.request.path:
            #    print('world_params', flow.request.path)
            #    world_params_raw = flow.response.content.decode("utf-8")
            #    world_params = json.loads(world_params_raw)
            #    parsed = re.search(r'(?P<player_id>player_id=)(?P<pgid>[a-zA-Z0-9]+)', flow.request.path, re.M)
            #    pgid = parsed.group(2)
            #    with open(f"/root/.mitmproxy/wardragons/world_params.txt", "w") as file:
            #        json.dump(world_params, file)
            #    os.chmod("/root/.mitmproxy/wardragons/world_params.txt", 0o744)
            #    world_completed = True

    def check_and_exit(self):
        if self.counter >= 2:
            ctx.log.info("Target packet count reached. Shutting down mitmproxy.")
            ctx.master.shutdown()


addons = [SavePackets]