import base64
from msg_handlers import proceed


def linkedin_job_alert(service, jobs):
    message = service.users().messages().get(
        userId='me', id=jobs['id']).execute()
    data = message['payload']['parts'][0]['body']['data']
    data = base64.urlsafe_b64decode(data).decode('utf-8').split('\n')
    # print(data)
    jobs = [[]]
    next = 0
    if data != None:
        for i in range(4, len(data)):
            if next > 0:
                next -= 1
                continue
            elif data[i] == '':
                break
            jobs[-1].append(data[i])
            if data[i].startswith('View job'):
                next = 4
                jobs.append([])
    jobs.pop()
    # debug([job[0] for job in jobs])
    return jobs


def linkedin_list_jobs(bot, message, job_items):
    rep = ''
    count = 0
    for i, job in enumerate(job_items):
        if count == 3:
            sent_msg = bot.send_message(
                message.chat.id, 'Sir, do you like me to send you more?')
            bot.register_next_step_handler(
                sent_msg, proceed, bot=bot, return_func=linkedin_list_jobs, job_items=job_items[i:])
            return
        text = ''
        link = job[-1][10:]
        text += f'<a href=\'{link}\'>{job[0]}</a>\n' + \
            f'<b>{job[1]}</b>\n'
        for i in job[2:3]:
            text += f'{i}\n'
        # debug('text === ', text)
        if len(rep) + len(text) > 4095:
            count += 1
            bot.send_message(
                message.chat.id, rep, parse_mode='HTML', disable_web_page_preview=True)
            rep = ''
        rep += text
    if rep != '':
        bot.send_message(
            message.chat.id, rep, parse_mode='HTML', disable_web_page_preview=True)


# def proceed(message, bot, job_items):
#     text = message.text.lower()
#     for i in range(3):
#         if text[:2] == 'ye':
#             bot.reply_to(
#                 message, 'Thank you, sir. I will keep sending you more right now.')
#             linkedin_list_jobs(bot, message, job_items)
#             return
#         elif text[:2] == 'no' or text[:3] == 'nah':
#             bot.reply_to(
#                 message, 'Thank you, sir. I will stop now.')
#             return
#         else:
#             if i == 2:
#                 bot.reply_to(
#                     message, 'I still didn\'t get that, sir. But I will count that as a no and stop now.')
#                 cont = False
#                 return
#             bot.reply_to(
#                 message, 'I didn\'t get that, sir. Please type \'yes\' or \'no\'.')


# def proceed(message, bot, return_func, *args, **kwargs):
#     text = message.text.lower()
#     for i in range(3):
#         if text[:2] == 'ye':
#             bot.reply_to(
#                 message, 'Thank you, sir. I will keep sending you more right now.')
#             return_func(bot, message, *args, **kwargs)
#             return
#         elif text[:2] == 'no' or text[:3] == 'nah':
#             bot.reply_to(
#                 message, 'Thank you, sir. I will stop now.')
#             return
#         else:
#             if i == 2:
#                 bot.reply_to(
#                     message, 'I still didn\'t get that, sir. But I will count that as a no and stop now.')
#                 cont = False
#                 return
#             bot.reply_to(
#                 message, 'I didn\'t get that, sir. Please type \'yes\' or \'no\'.')
