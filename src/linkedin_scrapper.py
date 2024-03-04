import base64


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
    rep, rf = '', 0
    count = 0
    for job in job_items:
        # if count % 3 == 0:
        #     bot.send_message(
        #         message.chat.id, 'Sir, do you like me to send you more?')

        #     cont = False

        #     @bot.message_handler(commands=['yes', 'no'])
        #     def proceed_job_alerts(bot, message):
        #         global cont
        #         text = message.text.lower()
        #         false_count = 0
        #         while True:
        #             if text[:3] == 'yes' or text[:4] == 'yeah':
        #                 bot.reply_to(
        #                     message, 'Thank you, sir. I will keep sending you more right now.')
        #                 cont = True
        #                 return
        #             elif text[:2] == 'no' or text[:3] == 'nah':
        #                 bot.reply_to(
        #                     message, 'Thank you, sir. I will stop now.')
        #                 cont = False
        #                 return
        #             else:
        #                 if (false_count == 2):
        #                     bot.reply_to(
        #                         message, 'I still didn\'t get that, sir. But I will count that as a no and stop now.')
        #                     cont = False
        #                     return
        #                 bot.reply_to(
        #                     message, 'I didn\'t get that, sir. Please type \'yes\' or \'no\'.')
        #                 false_count += 1
        #     if cont == False:
        #         return
        text = ''
        link = job[-1][10:]
        text += f'<a href=\'{link}\'>{job[0]}</a>\n' + \
            f'<strong>{job[1]}</strong>\n'
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
