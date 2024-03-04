def proceed(message, bot, return_func, *args, **kwargs):
    text = message.text.lower()
    for i in range(3):
        if text[:2] == 'ye':
            bot.reply_to(
                message, 'Thank you, sir. I will keep sending you more right now.')
            return_func(bot, message, *args, **kwargs)
            return
        elif text[:2] == 'no' or text[:3] == 'nah':
            bot.reply_to(
                message, 'Thank you, sir. I will stop now.')
            return
        else:
            if i == 2:
                bot.reply_to(
                    message, 'I still didn\'t get that, sir. But I will count that as a no and stop now.')
                cont = False
                return
            bot.reply_to(
                message, 'I didn\'t get that, sir. Please type \'yes\' or \'no\'.')
