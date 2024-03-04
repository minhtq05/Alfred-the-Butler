import requests
import json
from datetime import datetime
from msg_handlers import proceed


def list_contests(message, bot, ended=False, gym=False, data=None):
    if data == None:
        data = contests(ended, gym)

    if (num_contests := len(data)) == 0:
        bot.reply_to(message, 'Sir, there is no incomming contest.' if ended ==
                     False else 'Sir, something went wrong. I can\' find any contest in my database.\n Please fix me asap, sir.')
    
    else:
        bot.reply_to(message, f'You have {num_contests} incoming contest{'s' if len(data) > 1 else ''}, sir.')
        rep = ''
        count = 0
        for i, contest in enumerate(data):
            print(contest['name'])
            if count == 1:
                sent_msg = bot.send_message(
                    message.chat.id, 'Sir, do you like me to send you more?')
                bot.register_next_step_handler(
                    sent_msg, proceed, bot=bot, return_func=list_contests, ended=ended, gym=gym, data=data[i:])
                return
            text = f'<b>{contest['name']}</b> - {contest['type']}\n'
            text += f'<b>Time:</b> {datetime.fromtimestamp(contest['startTimeSeconds']).strftime('%d %b, %Y - %H:%M:%S')}\n'
            text += f'<b>Duration:</b> {int(contest["durationSeconds"]/60)} min\n'
            if contest['frozen'] == True:
                text += '<b>Warning: Contest is frozen.</b>\n'
            if len(rep) + len(text) > 4095:
                count += 1
                bot.send_message(message.chat.id, rep, parse_mode='HTML', disable_web_page_preview=True)
                rep = ''
            rep += text
        if rep != '':
            bot.send_message(message.chat.id, rep, parse_mode='HTML', disable_web_page_preview=True)


def contests(ended=False, gym=False):
    r = requests.get('https://codeforces.com/api/contest.list' +
                     ('?gym=true' if gym else ''))
    data = r.content.decode('utf-8')
    data = json.loads(data)['result']

    if ended:
        return data

    for i, contest in enumerate(data):
        if contest['phase'] == 'FINISHED':
            return data[:i]

    return data
