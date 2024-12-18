from mitmproxy import http, ctx
import json
import os

about_completed = False
params_completed = False
world_completed = False

def response(flow: http.HTTPFlow) -> None:
    if flow.response and flow.response.content:
        #print(vars(flow.request))
        #print(flow.request.path)
        if '/ext/dragonsong/event/about_v2' in flow.request.path:
            print('about_v2', flow.request.path)
            about_v2_raw = flow.response.content.decode("utf-8")
            about_v2 = json.loads(about_v2_raw)
            with open("/root/.mitmproxy/wardragons/about_v2.txt", "w") as file:
                json.dump(about_v2, file)
            os.chmod("/root/.mitmproxy/wardragons/about_v2.txt", 0o744)
            about_completed = True
        if '/dragons/event/current' in flow.request.path:
            print('params', flow.request.path)
            params = flow.response.content.decode("utf-8")
            #print(params)
            with open("/root/.mitmproxy/wardragons/params.txt", "w") as file:
                file.write(params)
            os.chmod("/root/.mitmproxy/wardragons/params.txt", 0o744)
            params_completed = True
        if '/ext/dragonsong/world/get_params' in flow.request.path:
            print('world_params', flow.request.path)
            world_params_raw = flow.response.content.decode("utf-8")
            world_params = json.loads(world_params_raw)
            #print(world_params)
            with open("/root/.mitmproxy/wardragons/world_params.txt", "w") as file:
                json.dump(world_params, file)
            os.chmod("/root/.mitmproxy/wardragons/world_params.txt", 0o744)
            world_completed = True


if about_completed is True and params_completed is True and world_completed is True:
    ctx.master.shutdown()
