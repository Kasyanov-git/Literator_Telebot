import telebot
from telebot import types
from fuzzywuzzy import process
import pandas as pd
import requests
from english_recomendation import SearchRecommendarion
df=pd.read_csv('1_labirint_eng_books_180.csv')
list_of_titles = list(df.agg('{0[title]} / '.format, axis=1)) + list(df.agg('{0[title]} / {0[author]}'.format, axis=1))
bot = telebot.TeleBot('5526049569:AAF1BCOJZoPrdDzviF27SKonHpMezwQtpL4')
    

@bot.message_handler(content_types=['text'])

def start(message):
    first_book, second_book, third_book = '','',''
    if message.text == '/start':
        bot.clear_step_handler(message)
        bot.send_message(message.from_user.id, text = f'Здравствуй, {message.from_user.first_name}!\n\nЧтобы я смогла посоветовать тебе книги, мне нужно узнать о твоих предпочтениях. Можешь написать ТОП-3 интересных книг, а я поищу что тебе подобрать!\U0001F4DA\n\n' +
        'Для начала, введи первое название самой потрясной книги, \nчтобы я вспомнила, \nчитала ли такую\U0001F4D6\n\n'+
        '(Продукт на этапе тест-версии и знаком только с 200 классическими произведениями. Не расстраивайтесь, если бот не найдёт вашу книгу, обновление с 10000 книг уже на подходе!)')
        bot.send_message(chat_id=923932902, text= f'\U0001F534{message.from_user.first_name} {message.from_user.last_name} {message.from_user.username} нажал старт!')
        bot.register_next_step_handler(message, get_first_book, first_book, second_book, third_book)
        

    elif message.text == '/search' or message.text == 'Погнали':
        bot.clear_step_handler(message)
        bot.send_message(message.from_user.id, f'Правила те же, {message.from_user.first_name}!\n\nЧтобы я смогла понять твои \nпредпочтения, назови мне \nТОП-3 своих книг!\U0001F4DA\n\nВведи название первой книги, а я вспомню, \nчитала ли такую\U0001F4D6')
        bot.send_message(chat_id=923932902, text= f'\U0001F534{message.from_user.first_name} {message.from_user.last_name} {message.from_user.username} нажал старт!')
        bot.register_next_step_handler(message, get_first_book, first_book, second_book, third_book)
        
    elif message.text == '/about':
        about_us(message)
    elif message.text == '/support':
        helping_us(message)
    elif message.text == '/feedback':
        commenting(message)
    else:
        bot.send_message(message.from_user.id, f'{message.from_user.first_name}!\n\nЧто-то случилось!\nПроверьте, не забыли ли вы нажать кнопку выше? Если нет, то это какая-то ошибка\U0001F440 \n\nПомни, если что-то пошло не по плану — кнопка меню слева от ввода сообщения!')
        bot.register_next_step_handler(message, start)
    
def get_first_book(message, first_book, second_book, third_book):
    bot.send_message(chat_id=923932902, text= f'\U000026AA Ищут {message.text}')
    try:
        rating_list_of_titles = process.extractOne(message.text, list_of_titles)
        # print(rating_list_of_titles)
        title = list(rating_list_of_titles)
        if message.text == '/start' or message.text == '/search' or message.text == '/about' or message.text == '/support' or message.text == '/feedback':
            start(message)
            return
        elif title[1] <= 86:
            bot.send_message(message.from_user.id, 'нет такой, введи другую')
            bot.register_next_step_handler(message, get_first_book, first_book, second_book, third_book)
        else:
            df1 = df[df['title'].str.contains(title[0].split(' /')[0])]
            print(df1)
            # first_book_title = str(df1.iloc[0][0])
            first_book_title = str(df.loc[df['title']==title[0].split(' /')[0]].index[0])
            markup = types.InlineKeyboardMarkup()
            yes_answer = types.InlineKeyboardButton('\U00002705', callback_data='1_y' + '<' + first_book_title + '|' + second_book + '>' + third_book+ '*#' )
            no_answer = types.InlineKeyboardButton('\U0000274C	', callback_data='1_n' + '<' + first_book_title + '|' + second_book + '>' + third_book + '*#')
            markup.add(yes_answer, no_answer)
            try:
                bot.send_photo(message.from_user.id, str(df1.iloc[0]['img']), caption='Это твоя книга? \nНазвание: ' + str(df1.iloc[0]['title']) + '\nАвтор: ' + str(df1.iloc[0]['author']), reply_markup=markup)
            except:
                bot.send_photo(message.from_user.id, "http://risovach.ru/upload/2015/12/mem/tvoe-vyrazhenie-lica_99422511_orig_.jpg", caption='Это твоя книга? \nНазвание: ' + str(df1.iloc[0]['title']) + '\nАвтор: ' + str(df1.iloc[0]['author']), reply_markup=markup)
    except:
        bot.send_message(message.from_user.id, 'Извини, не распознала. Можешь написать текстом?')
        bot.register_next_step_handler(message, get_first_book, first_book, second_book, third_book)

def get_second_book(message, first_book, second_book, third_book):
    bot.send_message(chat_id=923932902, text= f'\U000026AA Ищут {message.text}')
    try:
        rating_list_of_titles = process.extractOne(message.text, list_of_titles)
        title = list(rating_list_of_titles)
        if message.text == '/start' or message.text == '/search' or message.text == '/about' or message.text == '/support' or message.text == '/feedback':
            start(message)
            return
        elif title[1] <= 86:
            bot.send_message(message.from_user.id, 'нет такой, введи другую')
            bot.register_next_step_handler(message, get_second_book, first_book, second_book, third_book)
        else:
            df2 = df[df['title'].str.contains(title[0].split(' /')[0])]
            print(df2)
            # second_book_title = str(df2.iloc[0][0])
            second_book_title = str(df.loc[df['title']==title[0].split(' /')[0]].index[0])
            markup = types.InlineKeyboardMarkup()
            yes_answer = types.InlineKeyboardButton('\U00002705', callback_data='2_y' + '<' + first_book + '|' + second_book_title + '>' + third_book + '*#')
            no_answer = types.InlineKeyboardButton('\U0000274C', callback_data='2_n'+ '<' + first_book + '|' + second_book_title + '>' + third_book + '*#')
            markup.add(yes_answer, no_answer)
            try:
                bot.send_photo(message.from_user.id, str(df2.iloc[0]['img']), caption='Это твоя книга? \nНазвание: ' + str(df2.iloc[0]['title']) + '\nАвтор: ' + str(df2.iloc[0]['author']), reply_markup=markup)
            except:
                bot.send_photo(message.from_user.id, "http://risovach.ru/upload/2015/12/mem/tvoe-vyrazhenie-lica_99422511_orig_.jpg", caption='Это твоя книга? \nНазвание: ' + str(df2.iloc[0]['title']) + '\nАвтор: ' + str(df2.iloc[0]['author']), reply_markup=markup)
    except:
        bot.send_message(message.from_user.id, 'Извини, не распознала. Можешь написать текстом?')
        bot.register_next_step_handler(message, get_second_book, first_book, second_book, third_book)

def get_third_book(message, first_book, second_book, third_book):
    bot.send_message(chat_id=923932902, text= f'\U000026AA Ищут {message.text}')
    try:
        rating_list_of_titles = process.extractOne(message.text, list_of_titles)

        title = list(rating_list_of_titles)
        if message.text == '/start' or message.text == '/search' or message.text == '/about' or message.text == '/support' or message.text == '/feedback':
            start(message)
            return
        elif title[1] <= 86:
            bot.send_message(message.from_user.id, 'нет такой, введи другую')
            bot.register_next_step_handler(message, get_third_book, first_book, second_book, third_book)
        else:
            df3 = df[df['title'].str.contains(title[0].split(' /')[0])]
            print(df3)
            # third_book_title = str(df3.iloc[0][0])
            third_book_title = str(df.loc[df['title']==title[0].split(' /')[0]].index[0])
            markup = types.InlineKeyboardMarkup()
            yes_answer = types.InlineKeyboardButton('\U00002705', callback_data='3_y' + '<' + first_book + '|' + second_book + '>' + third_book_title + '*#')
            no_answer = types.InlineKeyboardButton('\U0000274C', callback_data='3_n'+ '<' + first_book + '|' + second_book + '>' + third_book_title + '*#')
            markup.add(yes_answer, no_answer)
            try:
                bot.send_photo(message.from_user.id, str(df3.iloc[0]['img']), caption='Это твоя книга? \nНазвание: ' + str(df3.iloc[0]['title']) + '\nАвтор: ' + str(df3.iloc[0]['author']), reply_markup=markup)
            except:
                bot.send_photo(message.from_user.id, "http://risovach.ru/upload/2015/12/mem/tvoe-vyrazhenie-lica_99422511_orig_.jpg", caption='Это твоя книга? \nНазвание: ' + str(df3.iloc[0]['title']) + '\nАвтор: ' + str(df3.iloc[0]['author']), reply_markup=markup)
    except:
        bot.send_message(message.from_user.id, 'Извини, не распознала. Можешь написать текстом?')
        bot.register_next_step_handler(message, get_third_book, first_book, second_book, third_book)

            
def search_book(message, first_book, second_book, third_book):
    try:
        markup = types.InlineKeyboardMarkup()
        go_recommend = types.InlineKeyboardButton('Искать рекомендации!', callback_data='g_r' + '<' + first_book + '|' + second_book + '>' + third_book + '*'+ '#' )
        change_book = types.InlineKeyboardButton('Изменить выбор', callback_data='c_b' + '<' + first_book + '|' + second_book + '>' + third_book + '*' + '#')
        markup.row(go_recommend)
        markup.row(change_book)
        bot.send_message(message.from_user.id, text= 'Выбранные книги \n\n'+'1. "'+ str(df.iloc[int(first_book)]['title']) + '", ' 
        + str(df.iloc[int(first_book)]['author']) + '\n2. "' + str(df.iloc[int(second_book)]['title']) + '", ' + str(df.iloc[int(second_book)]['author'])
        + '\n3. "' + str(df.iloc[int(third_book)]['title']) + '", ' + str(df.iloc[int(third_book)]['author']), reply_markup=markup)       
    except:
        try:
            markup = types.InlineKeyboardMarkup()
            go_recommend = types.InlineKeyboardButton('Искать рекомендации!', callback_data='g_r' + '<' + first_book + '|' + second_book + '>' + third_book + '*#' )
            add_book = types.InlineKeyboardButton('Хочу добавить ещё...', callback_data='a_b_3' + '<' + first_book + '|' + second_book + '>' + third_book  + '*#')
            change_book = types.InlineKeyboardButton('Изменить выбор', callback_data='c_b' + '<' + first_book + '|' + second_book + '>' + third_book  + '*#')
            markup.row(go_recommend)
            markup.row(add_book)
            markup.row(change_book)
            bot.send_message(message.from_user.id, text= 'Выбранные книги \n\n'+'1. "'+ str(df.iloc[int(first_book)]['title']) + '", ' 
            + str(df.iloc[int(first_book)]['author']) + '\n2. "' + str(df.iloc[int(second_book)]['title']) + '", ' + str(df.iloc[int(second_book)]['author']), reply_markup=markup)
        except:
            markup = types.InlineKeyboardMarkup()
            go_recommend = types.InlineKeyboardButton('Искать рекомендации!', callback_data='g_r' + '<' + first_book + '|' + second_book + '>' + third_book+ '*#' )
            add_book = types.InlineKeyboardButton('Хочу добавить ещё...', callback_data='a_b_2' + '<' + first_book + '|' + second_book + '>' + third_book + '*#')
            change_book = types.InlineKeyboardButton('Изменить выбор', callback_data='c_b' + '<' + first_book + '|' + second_book + '>' + third_book + '*#')
            markup.row(go_recommend)
            markup.row(add_book)
            markup.row(change_book)
            bot.send_message(message.from_user.id, text= 'Выбранные книги \n\n'+'1. "'+ str(df.iloc[int(first_book)]['title']) + '", ' 
                + str(df.iloc[int(first_book)]['author']), reply_markup=markup)

def recommend_books(message, first_book, second_book, third_book, number, good_job_count):
    if int(good_job_count) > 2:
        markup = types.InlineKeyboardMarkup()
        more_books = types.InlineKeyboardButton('Нужно больше книжек!', callback_data='u_b' + '<' + first_book + '|' + second_book + '>' + third_book + '*' + str(number-1) + '#' + '-1' )
        about_us = types.InlineKeyboardButton('Как ты работаешь?', callback_data='a_u' + '<|>*#')
        comment = types.InlineKeyboardButton('Оставить отзыв', callback_data='cmt' + '<|>*#')
        markup.row(more_books)
        markup.row(about_us)
        markup.row(comment)
        bot.send_message(message.from_user.id, text= 'Спасибо за уделённое время! Надеюсь, я порадовала тебя подборкой. \n\nВсе разделы можно найти в меню, слева от поля ввода сообщения \n\nХорошего дня!', reply_markup=markup)  
        bot.send_message(chat_id=923932902, text= f'\U0001F535{message.from_user.first_name} {message.from_user.last_name} {message.from_user.username} завершил поиск рекомендаций!')   
    else:
        await_user = bot.send_message(message.from_user.id, 'Пробегаюсь по полочкам, погоди секунду!')
        try: book_2 = df.iloc[int(second_book)]['title']
        except: book_2 = df.iloc[int(first_book)]['title']
        try: book_3 = df.iloc[int(third_book)]['title']
        except: book_3 = df.iloc[int(first_book)]['title']
        working_result = SearchRecommendarion(df.iloc[int(first_book)]['title'], book_2 , book_3 )
        print(number)
        df_result_1 = df[df['title'].str.contains(working_result[int(number)])]
        if str(df_result_1.iloc[0]['img']) == 'img':
            logo_1 = "http://risovach.ru/upload/2015/12/mem/tvoe-vyrazhenie-lica_99422511_orig_.jpg"
        else:
            logo_1 = str(df_result_1.iloc[0]['img'])
        markup = types.InlineKeyboardMarkup()
        like = types.InlineKeyboardButton('\U0001F44D', callback_data='u_b' + '<' + first_book + '|' + second_book + '>' + third_book + '*' + str(number) + '#' + str(good_job_count) )
        unknow = types.InlineKeyboardButton('\U0001F937', callback_data='u_b' + '<' + first_book + '|' + second_book + '>' + third_book  + '*' + str(number) + '#' + str(good_job_count))
        dislike = types.InlineKeyboardButton('\U0001F44E', callback_data='d_b' + '<' + first_book + '|' + second_book + '>' + third_book + '*' + str(number) + '#' + str(good_job_count))
        markup.add(like,unknow,dislike)
        bot.delete_message(message.from_user.id, await_user.message_id)
        bot.send_photo(message.from_user.id, logo_1 , caption= str(df_result_1.iloc[0]['title']) + '\n' + str(df_result_1.iloc[0]['author']) + '\n' + str(df_result_1.iloc[0]['url']), reply_markup=markup)

def about_us(message):
    markup = types.InlineKeyboardMarkup()
    about_us_more = types.InlineKeyboardButton('Что за похожести?', callback_data='a_u_m' + '<|>*#' )
    about_us_creators = types.InlineKeyboardButton('Кто тебя создал?', callback_data='a_u_c' + '<|>*#')
    help_us = types.InlineKeyboardButton('Чем я могу тебе помочь?', callback_data='h_u' + '<|>*#')
    markup.row(about_us_more)
    markup.row(about_us_creators)
    markup.row(help_us)
    bot.send_message(message.from_user.id, text= 'Я - алгоритм, написанный при помощи методов обработки естественного языка.' + 
            'Я читаю книжки, нахожу между ними “похожести” разного вида и сравниваю с книгами, которые я читала раньше.' + 
            'Это позволяет мне найти книжки, похожие между собой.', reply_markup=markup)

def helping_us(message):
    markup = types.InlineKeyboardMarkup()
    share_us = types.InlineKeyboardButton('Рассказать друзьям', callback_data='s_u' + '<|>*#' )
    donate_us = types.InlineKeyboardButton('Поддержать проект', callback_data='d_u' + '<|>*#')
    partnership = types.InlineKeyboardButton('Стать партнёром', callback_data='psh' + '<|>*#')
    markup.row(share_us)
    markup.row(donate_us)
    markup.row(partnership)
    bot.send_message(message.from_user.id, text= 'Самая классная помощь — поддержка и обратная связь! Чем больше я буду помогать другим, тем начитаннее стану \n\n' + 
            'Так же, сейчас я хочу стать быстрее и круче, и финансовая поддержка будет очень кстати! \n\n' + 
            'Если ты пишешь свои книги — мы можем стать партнёрами', reply_markup=markup)

def commenting(message):
    bot.send_message(message.from_user.id, text= 'Если у тебя остались впечатления от пользования сервисом, предлагаю перейти к полной форме обратной связи и помочь создателям доработать меня!'+
    '\n\nhttps://forms.gle/EYvWYtvmeJxMgXqt9 \n\nЕсли у тебя что-то срочное, или, наоборот, незначительное — можешь написать своё сообщение прямо здесь, под этим сообщением!')
    bot.register_next_step_handler(message, send_comment)

def partnershiping(message):
    bot.send_message(message.from_user.id, text= 'Если у тебя есть крутая идея нашего взаимодействия, напиши ниже свои любые контактные данные и тезисное описание своей идеи.\nИнформация отправится прямиком к моим создателям и они обязательно свяжутся с тобой!')
    bot.register_next_step_handler(message, send_partnership)

def send_partnership(message):
    if message.text == '/start' or message.text == '/search' or message.text == '/about' or message.text == '/support':
        start(message)
        return
    bot.send_message(chat_id=923932902, text= f'\U0001F7E2{message.from_user.first_name} {message.from_user.last_name} {message.from_user.username} написал ПРЕДЛОЖЕНИЕ ВЗАИМОДЕЙСТВИЯ!!!!:')
    bot.send_message(chat_id=923932902, text= message.text)
    bot.send_message(message.from_user.id, text= 'Отлично, всё получилось! \n\nС тобой свяжутся в ближейшее время. А пока, можешь воспользоваться меню — тем, слева от строчки ввода!')

def send_comment(message):
    if message.text == '/start' or message.text == '/search' or message.text == '/about' or message.text == '/support':
        start(message)
        return
    bot.send_message(chat_id=923932902, text= f'\U0001F7E1{message.from_user.first_name} {message.from_user.last_name} {message.from_user.username} написал ОБРАТНУЮ СВЯЗЬ!!!:')
    bot.send_message(chat_id=923932902, text= message.text)
    bot.send_message(message.from_user.id, text= 'Спасибо за информацию! Уверена, она поможет мне стать лучше. Все разделы можно найти в меню слева от строчки ввода!')



@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    bot.clear_step_handler(call)
    bot.answer_callback_query(callback_query_id=call.from_user.id , text='')
    button_name = call.data.split('<')[0]

    first_book = call.data.split('<')[1]
    first_book = first_book.split('|')[0]

    second_book = call.data.split('|')[1]
    second_book = second_book.split('>')[0]

    third_book = call.data.split('>')[1]
    third_book = third_book.split('*')[0]

    number = call.data.split('*')[1]
    number = number.split('#')[0]

    good_job_count = call.data.split('#')[1]
    if button_name == "1_y" or button_name == "2_y" or button_name == "3_y":
        try:
            search_book(call, first_book, second_book, third_book)  
        except:
            bot.clear_step_handler(call)
            bot.send_message(call.from_user.id, 'Ой, кажется книги кончились! \n\n      Если чувствуешь усталость от поиска, то всегда можешь воспользоваться кнопкой меню — она слева от поля ввода!\n\n     Если хочешь продолжить, то напиши, пожалуйста, название интересующей книги')
            bot.register_next_step_handler(call, get_first_book, first_book, second_book, third_book)

    if button_name == "1_n":
        bot.send_message(call.from_user.id, 'Поищем ещё, пока что введи заново')
        bot.register_next_step_handler(call, get_first_book, first_book, second_book, third_book)

    if button_name == "2_n":
        bot.send_message(call.from_user.id, 'Поищем ещё, пока что введи заново')
        bot.register_next_step_handler(call, get_second_book, first_book, second_book, third_book)
    
    elif button_name == "3_n":
        bot.send_message(call.from_user.id, 'Поищем ещё, пока что введи заново')
        bot.register_next_step_handler(call, get_third_book, first_book, second_book, third_book)

    if button_name == 'a_b_1':
        bot.send_message(call.from_user.id, 'Напиши название первой книги')
        try:
            bot.register_next_step_handler(call, get_first_book, first_book, second_book, third_book)      
        except:
            bot.send_message(call.from_user.id, 'Извини, не распознала. Можешь написать текстом?')
            # bot.register_next_step_handler(call, start)  

    if button_name == 'a_b_2':
        bot.send_message(call.from_user.id, 'Напиши название второй книги')
        bot.register_next_step_handler(call, get_second_book, first_book, second_book, third_book)

    if button_name == 'a_b_3':
        bot.send_message(call.from_user.id, 'Напиши название третей книги')
        bot.register_next_step_handler(call, get_third_book, first_book, second_book, third_book)

    if button_name == 'g_r':
        good_job_count = 0
        bot.send_message(call.from_user.id, text= 'Твоя подборка сейчас будет готова! \nПожалуйста оцени, что я предложила \n\n\U0001F44Dчитал(а), понравилось\n\U0001F937не читал(а), что-то новенькое\n\U0001F44Eчитал(а), неинтересно')
        number = 0
        recommend_books(call, first_book, second_book, third_book, number, good_job_count)
        
   
    if button_name == 'd_b':
        bot.delete_message(call.from_user.id, call.message.message_id)
        num = int(number) + 1
        recommend_books(call, first_book, second_book, third_book, num, good_job_count)    
    
    # if button_name == 'l_b':
    #     bot.delete_message(call.from_user.id, call.message.message_id)
    #     num = int(number) + 1
    #     recommend_books(call, first_book, second_book, third_book, num, good_job_count)   

    if button_name == 'u_b':
        print(number)
        good_job_count = int(good_job_count) + 1
        num = int(number) + 1
        recommend_books(call, first_book, second_book, third_book, num, good_job_count)    

    if button_name == 'a_u':   
        about_us(call)

    if button_name == 'a_u_m':
        markup = types.InlineKeyboardMarkup()
        about_us_creators = types.InlineKeyboardButton('Кто тебя создал?', callback_data='a_u_c' + '<|>*#')
        help_us = types.InlineKeyboardButton('Чем я могу тебе помочь?', callback_data='h_u' + '<|>*#')
        markup.row(about_us_creators)
        markup.row(help_us)
        bot.send_message(call.from_user.id, text= 'Когда ты вводишь свои любимые книжки, я сравниваю их тексты сначала между собой, а потом с другими книгами, которые я уже читала.' + 
                         'Я нахожу твои: стилистику написания, паттерны героев, сюжетную линию, динамичность событий и нравится ли тебе много описаний.' +
                        ' Чем больше у меня данных для сравнения, тем точнее критерий сравнения.', reply_markup=markup)

    if button_name == 'a_u_c':
        markup = types.InlineKeyboardMarkup()
        help_us = types.InlineKeyboardButton('Чем я могу тебе помочь?', callback_data='h_u' + '<|>*#')
        comment = types.InlineKeyboardButton('Дать обратную связь', callback_data='cmt' + '<|>*#')
        markup.row(help_us)
        markup.row(comment)
        bot.send_message(call.from_user.id, text= 'Меня обучают студенты donstux.com Анастасия и Никита. \n\n' + 
                        'Они очень стараются, и, сейчас, работают над пополнением моей базы знаний, а так же тестированием новых методов работы!\n\n' +
                        'Ребята хотят, чтобы я стала мегаудобной и моя точность была более 90%', reply_markup=markup)

    if button_name == 'd_u':
        markup = types.InlineKeyboardMarkup()
        comment = types.InlineKeyboardButton('Дать обратную связь', callback_data='cmt' + '<|>*#')
        markup.row(comment)
        bot.send_message(call.from_user.id, text= 'Поддержка сейчас — \nэто не просто донат \U0001FAF6 \n\n' + 
                        'Ваше внимание и поддержка подтвержают нужность этого проекта; побуждает нас, как творцов, к его развитию.\n\n' +
                        'Поэтому, финансовая поддержка — всецело ваша личная добровольная прерогатива, способная внести свою лепту в будущее этого проекта\n\n ' +
                        'Никита Андреевич К. Сбербанк \n' +
                        '4276520720587761', reply_markup=markup)                
    
    if button_name == 'h_u':
        helping_us(call)

    if button_name == 'cmt':
        commenting(call)
    if button_name == 'psh':
        partnershiping(call)
    
    if button_name == 's_u':
        bot.send_message(call.from_user.id, text= 'Перешли это сообщение своим друзьям!')
        bot.send_message(call.from_user.id, text= 'Всем привет! Я — Литератор, бот, который точно знает, какую книжку ты прочтёшь с удовольствием! \n\nЗаходи ко мне, проверь свою проницательность'+
        '\n\n@Lit_book_bot\n\n' + f'Между прочим, @{call.from_user.username} уже знает, что почитать!')
        bot.send_message(call.from_user.id, text= 'Спасибо за помощь! \nВсё, что нужно, найдёшь в меню')

    
    
    

    bot.edit_message_reply_markup(call.from_user.id, call.message.message_id)

    if button_name == 'c_b':
        
        markup = types.InlineKeyboardMarkup()
        change_first = types.InlineKeyboardButton(text = str(df.iloc[int(first_book)]['title']), callback_data='e_b_1' + '<' + first_book + '|' + second_book + '>' + third_book + '*#')
        go_back = types.InlineKeyboardButton(text = 'Назад >>', callback_data='1_y' + '<' + first_book + '|' + second_book + '>' + third_book + '*#')
        try:
            change_second = types.InlineKeyboardButton(text = str(df.iloc[int(second_book)]['title']), callback_data='e_b_2' + '<' + first_book + '|' + second_book + '>' + third_book + '*#')
            change_third = types.InlineKeyboardButton(text = str(df.iloc[int(third_book)]['title']), callback_data='e_b_3' + '<' + first_book + '|' + second_book + '>' + third_book + '*#')
            markup.row(change_first)
            markup.row(change_second)
            markup.row(change_third)
            markup.row(go_back)
        except:
            try:
                change_second = types.InlineKeyboardButton(text = str(df.iloc[int(second_book)]['title']), callback_data='e_b_2' + '<' + first_book + '|' + second_book + '>' + third_book + '*#')
                markup.row(change_first)
                markup.row(change_second)
                markup.row(go_back)
            except:
                markup.row(change_first)
                markup.row(go_back)
        bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text='Что изменим? \n\n')
        bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=markup)
        # bot.send_message(call.from_user.id, text= 'Что изменим? \n\n', reply_markup=markup)


    if button_name == 'e_b_1':
        markup = types.InlineKeyboardMarkup()
        edit_first = types.InlineKeyboardButton(text = 'Изменить', callback_data='a_b_1' + '<' + first_book + '|' + second_book + '>' + third_book + '*#')
        delete_first = types.InlineKeyboardButton(text = 'Удалить', callback_data='1_y' + '<' + second_book + '|' + third_book + '>' + '' + '*#')
        go_back = types.InlineKeyboardButton(text = 'Назад >>', callback_data='c_b' + '<' + first_book + '|' + second_book + '>' + third_book + '*#')
        markup.add(edit_first, delete_first, go_back)
        bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=str(df.iloc[int(first_book)]['title']))
        bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=markup)

    if button_name == 'e_b_2':
        markup = types.InlineKeyboardMarkup()
        edit_first = types.InlineKeyboardButton(text = 'Изменить', callback_data='a_b_2' + '<' + first_book + '|' + second_book + '>' + third_book + '*#')
        delete_first = types.InlineKeyboardButton(text = 'Удалить', callback_data='2_y' + '<' + first_book + '|' + third_book + '>' + '' + '*#')
        go_back = types.InlineKeyboardButton(text = 'Назад >>', callback_data='c_b' + '<' + first_book + '|' + second_book + '>' + third_book + '*#')
        markup.add(edit_first, delete_first, go_back)
        bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=str(df.iloc[int(second_book)]['title']))
        bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=markup)
    
    if button_name == 'e_b_3':
        markup = types.InlineKeyboardMarkup()
        edit_first = types.InlineKeyboardButton(text = 'Изменить', callback_data='a_b_3' + '<' + first_book + '|' + second_book + '>' + third_book + '*#')
        delete_first = types.InlineKeyboardButton(text = 'Удалить', callback_data='3_y' + '<' + first_book + '|' + second_book + '>' + '' + '*#')
        go_back = types.InlineKeyboardButton(text = 'Назад >>', callback_data='c_b' + '<' + first_book + '|' + second_book + '>' + third_book + '*#')
        markup.add(edit_first, delete_first, go_back)
        bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=str(df.iloc[int(third_book)]['title']))
        bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=markup)
bot.polling(none_stop=True, interval=0)
