#!/usr/bin/env python3
import json
from html.parser import HTMLParser
import re
from waitress import serve
from flask import Flask, request, abort, render_template

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def callback():
    if request.method == "POST":
        output = []
        refill_form = ''
        if 'application/json' in request.content_type:
            command = ''
            body = request.get_json()
        else:
            command = request.form['txt']
            body = {"events": [{"type": "web", "message": {"type": "text", "text": command},
                                "source": {"type": "group", "groupId": 0, "userId": 0}}]}
        if request.form:
            # print('form exists')
            print('Web Request!')
            print(request.headers)
            if command.startswith('/'):
                if '/linux' in command:
                    print('sneaky!')
                    print(command, body)
                    output = 'Sneaky!'
                else:
                    reply_token, group_id = 0, 0
                    print(body)
                    output = admincmds(body, reply_token, group_id)
            else:
                output = cmds(body)
            refill_form = request.form['txt']
            print('output', output)
            return render_template("bot.html", content=output, default=refill_form, help=help, search=search)#, adminhelp=help2)
        else:
            print("not request.form")
    if request.method == "GET":
        return render_template("bot.html", help=help, search=search)#, adminhelp=help2)
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

def main(c_num, c_type, params, about_v2, world_params, total):
    from chestpredictor2 import ChestPredictor
    spin_type_title = c_type_dict.get(c_type, 'gold')
    # params = /dragons/event/current?
    # about_v2 = /ext/dragonsong/event/about_v2?
    # world params = /ext/dragonsong/world/get_params?

    params = xml_parser(params)

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
                cp = ChestPredictor(params=params, about=about_v2, world_params=world_params)

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
        cp = ChestPredictor(params=params, about=about_v2, world_params=world_params)

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
    return out


if __name__ == "__main__":
    c_type_dict = {'gold': 'GOLD CHEST', 'silver': 'SILVER CHEST', 'bronze': 'BRONZE CHEST',
                   'draconic': 'DRACONIC CHEST', 'sigil': 'SUPER SIGIL CHEST', 'platinum': 'PLATINUM CHEST',
                   'relic': 'RELIC CHEST', 'atlas': 'ATLAS CHEST', 'glory': 'ATLAS BADGE CHEST', 'special': 'SPECIAL CHEST',
                   'all': 'all'}
    c_num = 20
    c_type = 'all'
    total = False


    with open('~/.mitmproxy/wardragons/about_v2.txt', 'r') as file:
        about_v2 = json.load(file)

    with open('~/.mitmproxy/wardragons/params.txt', 'r') as file:
        params = file.read()

    with open('~/.mitmproxy/wardragons/world_params.txt', 'r') as file:
        world_params = json.load(file)

    serve(app, host='0.0.0.0', port=5000)
    main(c_num, c_type, params, about_v2, world_params, total)
