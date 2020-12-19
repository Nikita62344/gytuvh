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
        # Если оно имеет метку для меня( то есть бота)чтобф пришло к нам 
        if event.to_me:
            #неожиданно тест ловер - отпуск на нижний регистр
            text = event.text.lower()
            user_id = event.user_id
            print(text)
            if user_id in gamers:
                try:
                    otvet = int(text)
                except:
                    if text =='выйти':
                        del gamers[user_id]
                        send_message(user_id,"не надо, ну ладно :с",main_keyboard)    #<1
                        
                    send_message(user_id,"ты что написал глупый"),game_over_kayboard
                    continue
                if otvet > gamers[user_id]:
                    send_message(user_id,"не попал слишком много")
                elif otvet < gamers[user_id]:
                    send_message(user_id," не попал слишком мало")
                else:
                    send_message(user_id,"КРАСААААВААААА, Ты победил", main_keyboard)
                    del gamers[user_id]
            else:
                if text == 'START'.lower():   
                    send_message(user_id,"Добро пожаловать",main_keyboard)  # <===
                    
                elif text == 'Об авторе'.lower():   
                    send_message(user_id,"Мой создатель Пенин Никита",back_keyboard)
                elif text == 'Сделать пожертвование'.lower():   
                    send_message(user_id,"Платежка еще не подключена",back_keyboard)
                elif text == 'Го каточку'.lower():
                    from random import randint
                    gamers[user_id] = randint(1,9000)
                    send_message(user_id,"ну давай давай угадай")
                elif text == 'узнать погоду'.lower():   
                    send_message(user_id,"ясно понял  ",back_keyboard)
                else:
                    send_message(user_id,"и что дальше",main_keyboard)
