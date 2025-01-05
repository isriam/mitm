#!/usr/bin/env python3
import json
from html.parser import HTMLParser
import re
from waitress import serve
from flask import Flask, request, abort, render_template
import time
import os

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def callback():
    if request.method == "POST":
        if request.form:
            # print('form')
            form_dict = {}
            if request.form['txt']:
                print('form text')
                form_text = request.form['txt'].lower().split(' ')
                form_dict = {idx: ele for idx, ele in enumerate(form_text)}
                # print(form_dict)
            print(form_dict)
            chest_type = form_dict.get(0, 'gold')
            chest_num = form_dict.get(1, 10)
            total = form_dict.get(2, False)
            # print(chest_type, chest_num)
            output, pgid = main(type=chest_type, c_num=chest_num, total=total)
            form_output = '\n'.join(output)
            refill_form = request.form['txt']
            timers = creation_time(pgid)
            return render_template("bot.html", content=form_output, timers=timers, default=refill_form, help=help_text)
    else:
        # output = main()
        # form_output = '\n'.join(output)
        timers = creation_time(pgid='')
        return render_template("bot.html", timers=timers, help=help_text)
    return 'OK'
def xml_parser(data):
    class MyHTMLParser(HTMLParser):
        def handle_starttag(self, tag, attrs):
            self.wdtag = tag

        def handle_data(self, data):
            if not hasattr(self, 'wddata'):
                self.wddata = {}
            if not self.wdtag in self.wddata:
                self.wddata[self.wdtag] = []
            self.wddata[self.wdtag].append(data)

    # print(type(data))
    # print(data)

    parser = MyHTMLParser()
    parser.wdtag = None
    parser.wddata = {}

    parser.feed(data)
    wddata = {}
    # print(parser.wddata['script'])
    for scriptdata in parser.wddata['script']:
        # print('start' + str(scriptdata) + 'end')
        session = re.search(r'(?P<find_session>window.session_token = )"(?P<token>.*?)"', scriptdata, re.M)
        if session:
            if session.group(2):
                wddata.update({'session_token': session.group(2)})
            else:
                wddata.update({'session_token': '12345678901234567890D'})
        pgid = re.search(r'(?P<find_session>window.pgid = )(.*?".*?")', scriptdata, re.M)
        if pgid:
            wddata.update({'pgid': json.loads(pgid.group(2))})
        params = re.search(r'(?P<window>window.params_and_data = )(.*}})', scriptdata, re.M)
        # print(params)
        if params:
            # print('group 0', params.group(0))
            # print('group 1', params.group(1))
            # print('group 2', params.group(2))
            # wddata = json.loads(params.group(2))
            wddata.update({'params_and_data': json.loads(params.group(2))})
    # print(wddata)
    return wddata


def main(**kwargs):
    from chestpredictor2 import ChestPredictor
    chest_type = kwargs.get('type', 'gold')
    print(chest_type)
    c_num = int(kwargs.get('c_num', 10))
    print(c_num)
    total = kwargs.get('total', False)
    spin_type_title = c_type_dict.get(chest_type, 'GOLD CHEST')
    print(spin_type_title)
    # params = /dragons/event/current?
    # about_v2 = /ext/dragonsong/event/about_v2?
    # world params = /ext/dragonsong/world/get_params?

    with open(about_v2_path, 'r') as file:
        about_v2 = json.load(file)

    with open(params_path, 'r') as file:
        unparsed_params = file.read()

    # with open(world_params_path, 'r') as file:
        # world_params = json.load(file)

    params = xml_parser(unparsed_params)

    pgid = None
    for x in about_v2:
        for y in about_v2[x]["eventInfo"].get("earned_awards"):
            if 'QuestAwards-teamquest' in y:
                awards = y.split('-')
                pgid = awards[2]
                # print(pgid)

    out = []

    # print('drops', drops)
    drop_list = []
    event_drop_dict = {}
    print_space_dict = {'Atlas': 6, 'Common': 7, 'Rare': 9, 'Epic': 9, 'Legendary': 4, 'Mythic': 7}
    line_space_dict = {'Atlas': 6, 'Common': 1, 'Rare': 1, 'Epic': 1, 'Legendary': 1, 'Mythic': 1}
    # print(len(drops))
    if 'all' in spin_type_title:
        for x in c_type_dict:
            # print(x)
            spin_type_title = c_type_dict.get(x)
            if spin_type_title == 'all':
                break
            else:
                # print(spin_type_title)
                cp = ChestPredictor(params=params, about=about_v2)  # , world_params=world_params)

                drops = cp.getDrops(spin_type_title=spin_type_title, drop_count=c_num)
                for event in drops:
                    count = 1
                    # print('event', event)
                    event_name = event.get('event')
                    out.append(event_name)
                    out.append(event.get('spin_type'))
                    for drop in event.get('drops'):
                        # print(drop)
                        # print(event_count)
                        drop_type = drop.get('drop_type') if drop.get('drop_type') else 'Atlas'
                        drop_id = drop.get('drop_id')
                        friendly_name = drop.get('friendly_name') if drop.get('friendly_name') != '' else drop_id
                        drop_count = drop.get('drop_count')
                        drop_detail = drop.get('drop_detail')
                        seq = drop.get('seq')
                        credit_drop = drop.get('credit_drop')
                        print_spaces = print_space_dict.get(drop_type)
                        line_spaces = line_space_dict.get(drop_type)
                        drop_list.append([friendly_name, drop_count])
                        # print(drop_type, drop_id, friendly_name, drop_count, credit_drop)
                        if credit_drop:
                            # print(f"{count}. {drop_type}: {str(drop_count):>{print_spaces}s} {friendly_name} !Bonus!")
                            # out.append(f"{count}. Seq {seq} {drop_type} {str(drop_count):>{line_spaces}s} {friendly_name} **Bonus**")
                            out.append(f"Seq {seq}:{drop_type}:{friendly_name} (x{str(drop_count)}) **Bonus**")
                        else:
                            # print(f"{count}. {drop_type}: {str(drop_count):>{print_spaces}s} {friendly_name}")
                            # out.append(f"{count}. Seq {seq} {drop_type} {str(drop_count):>{line_spaces}s} {friendly_name}")
                            out.append(f"Seq {seq}:{drop_type}:{friendly_name} (x{str(drop_count)})")
                        count = count + 1
                    event_drop_dict.update({event_name: drop_list})
                    out.append('\r')
    else:
        cp = ChestPredictor(params=params, about=about_v2)  # , world_params=world_params)

        drops = cp.getDrops(spin_type_title=spin_type_title, drop_count=c_num)
        for event in drops:
            count = 1
            # print('event', event)
            event_name = event.get('event')
            out.append(event_name)
            out.append(event.get('spin_type'))
            for drop in event.get('drops'):
                # print(drop)
                # print(event_count)
                drop_type = drop.get('drop_type') if drop.get('drop_type') else 'Atlas'
                drop_id = drop.get('drop_id')
                friendly_name = drop.get('friendly_name') if drop.get('friendly_name') != '' else drop_id
                drop_count = drop.get('drop_count')
                drop_detail = drop.get('drop_detail')
                seq = drop.get('seq')
                credit_drop = drop.get('credit_drop')
                print_spaces = print_space_dict.get(drop_type)
                line_spaces = line_space_dict.get(drop_type)
                drop_list.append([friendly_name, drop_count])
                # print(drop_type, drop_id, friendly_name, drop_count, credit_drop)
                if credit_drop:
                    # print(f"{count}. {drop_type}: {str(drop_count):>{print_spaces}s} {friendly_name} !Bonus!")
                    # out.append(f"{count}. Seq {seq} {drop_type} {str(drop_count):>{line_spaces}s} {friendly_name} **Bonus**")
                    out.append(f"Seq {seq}:{drop_type}:{friendly_name} (x{str(drop_count)}) **Bonus**")
                else:
                    # print(f"{count}. {drop_type}: {str(drop_count):>{print_spaces}s} {friendly_name}")
                    # out.append(f"{count}. Seq {seq} {drop_type} {str(drop_count):>{line_spaces}s} {friendly_name}")
                    out.append(f"Seq {seq}:{drop_type}:{friendly_name} (x{str(drop_count)})")
                count = count + 1
            event_drop_dict.update({event_name: drop_list})
            out.append('\r')

    # build total list for each event
    if total:
        print('total')
        out = []
        total_dict = {}
        print(event_drop_dict)
        for event, drop_list in event_drop_dict.items():
            # print(event, drop_list)
            out.append(event)
            for x in drop_list:
                if x[0] in total_dict.keys():
                    total_dict[x[0]] = total_dict[x[0]] + int(x[1])
                else:
                    total_dict.update({x[0]: int(x[1])})
            for drop_type, friendly_name in total_dict.items():
                print(f"{drop_type} - {friendly_name}")
                out.append(f"{drop_type} - {friendly_name}")

    print('\n'.join(out))
    return out, pgid

def help():
    help=f"""
Step 1, download profile
Step 2, import profile
Step 3, enable profile

Step 1
a) set proxy in wifi settings 129.146.200.231 port 3124
b) in safari go to mitm.it/ and click visit this site
c) download ios certificate

Step 2
go to general - vpn and profiles - install mitmproxy certificate

Step 3
go to general - about - certificate trust settings - enable mitmproxy root cert"""
    return help


def creation_time(pgid=None):
    about_v2_creation_time = time.ctime(os.path.getmtime(about_v2_path))
    params_creation_time = time.ctime(os.path.getmtime(params_path))
    # world_params_creation_time = time.ctime(os.path.getmtime(world_params_path))
    times = f"""
about_v2_modified = {about_v2_creation_time} - {pgid}
params_modified = {params_creation_time} - {pgid}"""
    return times


if __name__ == "__main__":
    c_type_dict = {'gold': 'GOLD CHEST', 'silver': 'SILVER CHEST', 'bronze': 'BRONZE CHEST',
                   'draconic': 'DRACONIC CHEST', 'sigil': 'SUPER SIGIL CHEST', 'platinum': 'PLATINUM CHEST',
                   'relic': 'RELIC CHEST', 'special': 'SPECIAL CHEST',
                   'all': 'all'}  # 'atlas': 'ATLAS CHEST', 'glory': 'ATLAS BADGE CHEST'
    # c_num = 20
    # c_type = 'all'
    # total = False

    about_v2_path = '/home/ubuntu/.mitmproxy/wardragons/about_v2.txt'
    params_path = '/home/ubuntu/.mitmproxy/wardragons/params.txt'
    # world_params_path = '/home/ubuntu/.mitmproxy/wardragons/world_params.txt'

    help_text = help()

    print('serving')
    # print(about_v2_creation_time, params_creation_time, world_params_creation_time)
    serve(app, host='0.0.0.0', port=5443)

