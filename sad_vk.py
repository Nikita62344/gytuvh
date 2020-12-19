import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard  # <===
key = "c8c1d98882d596055db31e73984b55ded8593af20aaca05c3c78990fc0984e999ef6020faec50a7958799"
# Авторизуемся как сообщество
vk = vk_api.VkApi(token=key)

def send_message(user_id, message, keyboard = None):  # <===
                from random import randint
                vk.method('messages.send',#принимает  в качестве агрумента
                          {'user_id': user_id,#id пользователя
                           "random_id":randint(1,1000) ,#он поймет что это не повтор сообщения 
                           'message': message,#сообщение
                           'keyboard':keyboard.get_keyboard() if keyboard else None,}  # <===отправка клавиатуры
                          )
#клавиатура бота
start_keyboard = VkKeyboard(one_time = True)  # <===
start_keyboard.add_button('START')
start_keyboard.add_line()
start_keyboard.add_button('NOT START')

main_keyboard = VkKeyboard(one_time = True)  # <===
main_keyboard.add_button('Об авторе')
main_keyboard.add_button('Сделать пожертвование')
main_keyboard.add_line()
main_keyboard.add_button('Го каточку')

main_keyboard.add_button('интересно сегодня ливень?')

back_keyboard = VkKeyboard(one_time = True)
back_keyboard.add_button('Назад')
game_over_keyboard = VkKeyboard(one_time = True)    #<1=====
game_over_keyboard.add_button('выйти')
game_over_keyboard.add_line()
game_over_keyboard.add_button('ну попробуй(просто введи число)')

gamers={}
# Работа с сообщениями
longpoll = VkLongPoll(vk)
# Основной цикл
for event in longpoll.listen():
    # Если пришло новое сообщение
    if event.type == VkEventType.MESSAGE_NEW:
        # Если оно имеет метку для меня( то есть бота)
        if event.to_me:
            text = event.text.lower()
            user_id = event.user_id
            print(text)
            if user_id in gamers:
                try:
                    otvet = int(text)
                except:
                    if text == 'выйти':
                        del gamers[user_id]
                        send_message(user_id,"ну ладно :с",main_keyboard)    #<1=====
                    else:
                        send_message(user_id,"те чо игра надоела?",game_over_keyboard)

                    continue
                if otvet > gamers[user_id]:
                    send_message(user_id,"mnoga")
                elif otvet < gamers[user_id]:
                    send_message(user_id,"malo")
                else:
                    send_message(user_id,"Победил", main_keyboard)
                    del gamers[user_id]
            else:
                if text == 'START'.lower():
                    send_message(user_id,"Добро пожаловать",main_keyboard)
                    #asdasd
                elif text == 'Об авторе'.lower():
                    send_message(user_id,"Damir",back_keyboard)
                elif text == 'Сделать пожертвование'.lower():
                    send_message(user_id,"Выберите тип пожертвования",donat_keyboard)
                elif text == 'Сыграть в игру'.lower():
                    from random import randint
                    gamers[user_id] = randint(1,9000)
                    send_message(user_id,"угадывай")
                elif text == 'узнать погоду'.lower():
                    send_message(user_id,"ясно",back_keyboard)
                    # donat_keyboard.add_button('Помолиться за автора')
                    # donat_keyboard.add_line()
                    # donat_keyboard.add_button('Купить автору шаурму')
                    # donat_keyboard.add_line()
                    # donat_keyboard.add_button('Оплатить хостинг бота')
                    # donat_keyboard.add_line()
                    # donat_keyboard.add_button('Я передумал')
                elif text == 'Помолиться за автора'.lower():
                    send_message(user_id,"...🕯️...",main_keyboard)
                elif text == 'Купить автору шаурму'.lower():
                    send_message(user_id,"лучшая шаурма по мнению автора - в simple, возле Idea.",main_keyboard)
                elif text == 'Оплатить хостинг бота'.lower():
                    send_message(user_id,"текущая стоимость хостинга - $0.00, хостинг оплачен на следующие ████ лет.\n спасибо зазаботу",main_keyboard)
                elif text == 'Я передумал'.lower():
                    send_message(user_id,"подумай еще.",donat_keyboard)

                else:
                    send_message(user_id,"Продолжайте",main_keyboard)
