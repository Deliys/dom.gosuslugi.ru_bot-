import requests #работа post/get запросами для получения данных с gosuslug
import json #работа с json (база пользователей)
#работа с телеграмом
import telebot 
from telebot import types
#вспомогательные библиотеки для ускорения работы
import math
import difflib
import numpy 

#импорот 
from pypo.data_list import regions_list_all
from pypo.data_list import citi_list_all
from pypo.data_list import street_list_all
from pypo.data_list import home_list_all

#-------------------------------------
#вынос лишних функция далее/назад в отдельные файлы 

import pypo.getdata as gd #импорт функция из файла getdata в pypo 
import pypo.change_write as cw 
import pypo.change_next as cn 

#change_write - вынес выбор в этот файл
from pypo.data_list import regions_list, vilage_list , citi_list, area_list ,street_list ,home_list
#-------------------------------------



bot = telebot.TeleBot('5335585579:AAFcNbUtWijoW4ghUvq_RWhn0N_OAboQL1s')


#открытие файла для временного сохранения данных для каждого пользователя
with open('file/database_user.json', 'r',encoding='utf-8') as fp:
	database_user = json.load(fp)
#открытие файла с формой json для запроса на госулуги
with open('file/regions.json', 'r',encoding='utf-8') as fp:
	regions = json.load(fp)



item_start =types.InlineKeyboardButton("в начало",callback_data='start_t')



while True:
	try:
		# Функция, обрабатывающая команду /start
		@bot.message_handler(commands=["start"])
		def start(m, res=False):
			bot.send_message(m.chat.id, 'Напишите "начать" для поиска управляющих и ресурсоснабжающих организаций поадресу')
		# Получение сообщений от юзера


		#----------------

		@bot.message_handler(content_types=["text"])

		def handle_text(message):
			#print(database_user)
			if (str(message.chat.id) in database_user) == False:
				database_user[str(message.chat.id)]= {
						"regions_numb":0,#номер страницы 
						"citi_numb":0,
						"adres":""
					}

				#print(database_user)

				with open('file/database_user.json', "w",encoding='utf-8') as file:
					json.dump(database_user, file, indent=4, ensure_ascii=False)

			if message.text == "начать":
				markup=types.InlineKeyboardMarkup()


				a=regions_list(regions,0)

				for i in a:
					item1=types.InlineKeyboardButton(i[0],callback_data=("regionCode " + i[1]))
					markup.add(item1)

				item1=types.InlineKeyboardButton("назад",callback_data='regions -')
				item3=types.InlineKeyboardButton("[0/"+str(int((len(regions)/8)))+"]",callback_data='chet')
				item2=types.InlineKeyboardButton("далее",callback_data='regions +')

				markup.add(item1,item3,item2)
				markup.add(item_start)
				
				bot.send_message(message.chat.id,'Выберите регион',reply_markup=markup)



		# Запускаем бота


		@bot.callback_query_handler(func=lambda call: True)
		def callback_worker(call):
			try:



				if call.data.split()[0] == "regions": 
					cn.regions_next(bot , call ,database_user , regions)

				

				#район или город-------------------------------------------


				if call.data.split()[0] == "regionCode":
					database_user[str(call.message.chat.id)]["regions"]  = call.data.split()[1]
					markup=types.InlineKeyboardMarkup()
					item1=types.InlineKeyboardButton("Город",callback_data='citi')
					item2=types.InlineKeyboardButton("Район",callback_data='area')
					markup.add(item1,item2)

					bot.delete_message(str(call.message.chat.id), call.message.id)
					bot.send_message(str(call.message.chat.id),'Выберите город или район',reply_markup=markup)	
					
				

				#Район----------------------------------------------

				if call.data.split()[0]== "area":
					cn.area_next(bot,call,database_user)

				#населенный пункт -----------------------------------
				if call.data.split()[0] == 'areaCode':
					cw.areaCode_func(bot, call ,database_user)
					

				if call.data.split()[0]== "vilage":
					cn.vilage_next(bot,call,database_user)
									

				if call.data.split()[0] == 'vilageCode':
					cw.vilageCode_func(bot, call ,database_user)





				if call.data == "settlement_v +": 
					if int(int((len(database_user[str(call.message.chat.id)]["cashe"])/7))) >= (database_user[str(call.message.chat.id)]["streetCode_numb"] +1): 
						# эта страшная черуха сравнивает колво страниц с номером на которой ты уже находишь +1 
						# если листов больше ,то перебросит на следущий , если листов меньше , то кинет на лист первый(0)
						database_user[str(call.message.chat.id)]["streetCode_numb"] = database_user[str(call.message.chat.id)]["streetCode_numb"] +1
						 
						markup=types.InlineKeyboardMarkup()
						a=home_list(database_user[str(call.message.chat.id)]["cashe"],database_user[str(call.message.chat.id)]["streetCode_numb"])
						for i in a:
							item1=types.InlineKeyboardButton(i[0],callback_data=("settlementCode " + i[1]))
							markup.add(item1)

						item1=types.InlineKeyboardButton("назад",callback_data='settlement_v -')
						item3=types.InlineKeyboardButton("["+str(database_user[str(call.message.chat.id)]["streetCode_numb"])\
							+"/"+str(int((len(database_user[str(call.message.chat.id)]["cashe"])/7)))+"]",callback_data='chet')
						item2=types.InlineKeyboardButton("далее",callback_data='settlement_v +')

						markup.add(item1,item3,item2)
						markup.add(item_start)
						


						bot.delete_message(str(call.message.chat.id), call.message.id)
						bot.send_message(str(call.message.chat.id),'выберите Город из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)

					else:
						
						database_user[str(call.message.chat.id)]["streetCode_numb"] = 0
						markup=types.InlineKeyboardMarkup()


						a=home_list(database_user[str(call.message.chat.id)]["cashe"],0)
						for i in a:
							item1=types.InlineKeyboardButton(i[0],callback_data=("settlementCode " + i[1]))
							markup.add(item1)



						item1=types.InlineKeyboardButton("назад",callback_data='settlement_v -')
						item3=types.InlineKeyboardButton("["+str(database_user[str(call.message.chat.id)]["streetCode_numb"])\
							+"/"+str(int((len(database_user[str(call.message.chat.id)]["cashe"])/7)))+"]",callback_data='chet')
						item2=types.InlineKeyboardButton("далее",callback_data='settlement_v +')
						markup.add(item1,item3,item2)
						markup.add(item_start)
						bot.delete_message(str(call.message.chat.id), call.message.id)
						bot.send_message(str(call.message.chat.id),'выберите Город из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)

						


				if call.data == "settlement_v -": 
					print(2222222222222222222)
					if 0<= (database_user[str(call.message.chat.id)]["streetCode_numb"] -1): 
						# эта страшная черуха сравнивает колво страниц с номером на которой ты уже находишь +1 
						# если листов больше ,то перебросит на следущий , если листов меньше , то кинет на лист первый(0)
						database_user[str(call.message.chat.id)]["streetCode_numb"] = database_user[str(call.message.chat.id)]["streetCode_numb"] -1
						 
						markup=types.InlineKeyboardMarkup()
						a=home_list(database_user[str(call.message.chat.id)]["cashe"],database_user[str(call.message.chat.id)]["streetCode_numb"])
						for i in a:
							item1=types.InlineKeyboardButton(i[0],callback_data=("settlementCode " + i[1]))
							markup.add(item1)

						item1=types.InlineKeyboardButton("назад",callback_data='settlement_v -')
						item3=types.InlineKeyboardButton("["+str(database_user[str(call.message.chat.id)]["streetCode_numb"])\
							+"/"+str(int((len(database_user[str(call.message.chat.id)]["cashe"])/7)))+"]",callback_data='chet')
						item2=types.InlineKeyboardButton("далее",callback_data='settlement_v +')

						markup.add(item1,item3,item2)
						markup.add(item_start)

						bot.delete_message(str(call.message.chat.id), call.message.id)
						bot.send_message(str(call.message.chat.id),'выберите Город из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)



					else:

						
						database_user[str(call.message.chat.id)]["streetCode_numb"] = int((len(database_user[str(call.message.chat.id)]["cashe"])/7))
						markup=types.InlineKeyboardMarkup()


						a=home_list(database_user[str(call.message.chat.id)]["cashe"],int((len(database_user[str(call.message.chat.id)]["cashe"])/7)))
						for i in a:
							item1=types.InlineKeyboardButton(i[0],callback_data=("settlementCode " + i[1]))
							markup.add(item1)



						item1=types.InlineKeyboardButton("назад",callback_data='settlement_v -')
						item3=types.InlineKeyboardButton("["+str(database_user[str(call.message.chat.id)]["streetCode_numb"])\
							+"/"+str(int((len(database_user[str(call.message.chat.id)]["cashe"])/7)))+"]",callback_data='chet')
						item2=types.InlineKeyboardButton("далее",callback_data='settlement_v +')
						markup.add(item1,item3,item2)
						markup.add(item_start)
						bot.delete_message(str(call.message.chat.id), call.message.id)
						bot.send_message(str(call.message.chat.id),'выберите Город из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)




				if call.data == "settlement +": 
					if int(int((len(database_user[str(call.message.chat.id)]["cashe"])/7))) >= (database_user[str(call.message.chat.id)]["settlement_numb"] +1): 
						# эта страшная черуха сравнивает колво страниц с номером на которой ты уже находишь +1 
						# если листов больше ,то перебросит на следущий , если листов меньше , то кинет на лист первый(0)
						database_user[str(call.message.chat.id)]["settlement_numb"] = database_user[str(call.message.chat.id)]["settlement_numb"] +1
						 
						markup=types.InlineKeyboardMarkup()
						a=area_list(database_user[str(call.message.chat.id)]["cashe"],database_user[str(call.message.chat.id)]["settlement_numb"])
						for i in a:
							item1=types.InlineKeyboardButton(i[0],callback_data=("settlementCode " + i[1]))
							markup.add(item1)

						item1=types.InlineKeyboardButton("назад",callback_data='settlement -')
						item3=types.InlineKeyboardButton("["+str(database_user[str(call.message.chat.id)]["settlement_numb"])\
							+"/"+str(int((len(database_user[str(call.message.chat.id)]["cashe"])/7)))+"]",callback_data='chet')
						item2=types.InlineKeyboardButton("далее",callback_data='settlement +')

						markup.add(item1,item3,item2)
						markup.add(item_start)
						


						bot.delete_message(str(call.message.chat.id), call.message.id)
						bot.send_message(str(call.message.chat.id),'выберите Город из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)

					else:
						
						database_user[str(call.message.chat.id)]["settlement_numb"] = 0
						markup=types.InlineKeyboardMarkup()


						a=area_list(database_user[str(call.message.chat.id)]["cashe"],0)
						for i in a:
							item1=types.InlineKeyboardButton(i[0],callback_data=("settlementCode " + i[1]))
							markup.add(item1)



						item1=types.InlineKeyboardButton("назад",callback_data='settlement -')
						item3=types.InlineKeyboardButton("["+str(database_user[str(call.message.chat.id)]["settlement_numb"])\
							+"/"+str(int((len(database_user[str(call.message.chat.id)]["cashe"])/7)))+"]",callback_data='chet')
						item2=types.InlineKeyboardButton("далее",callback_data='settlement +')
						markup.add(item1,item3,item2)
						markup.add(item_start)
						bot.delete_message(str(call.message.chat.id), call.message.id)
						bot.send_message(str(call.message.chat.id),'выберите Город из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)

						


				if call.data == "settlement -": 
					if 0<= (database_user[str(call.message.chat.id)]["settlement_numb"] -1): 
						# эта страшная черуха сравнивает колво страниц с номером на которой ты уже находишь +1 
						# если листов больше ,то перебросит на следущий , если листов меньше , то кинет на лист первый(0)
						database_user[str(call.message.chat.id)]["settlement_numb"] = database_user[str(call.message.chat.id)]["settlement_numb"] -1
						 
						markup=types.InlineKeyboardMarkup()
						a=area_list(database_user[str(call.message.chat.id)]["cashe"],database_user[str(call.message.chat.id)]["settlement_numb"])
						for i in a:
							item1=types.InlineKeyboardButton(i[0],callback_data=("settlementCode " + i[1]))
							markup.add(item1)

						item1=types.InlineKeyboardButton("назад",callback_data='settlement -')
						item3=types.InlineKeyboardButton("["+str(database_user[str(call.message.chat.id)]["settlement_numb"])\
							+"/"+str(int((len(database_user[str(call.message.chat.id)]["cashe"])/7)))+"]",callback_data='chet')
						item2=types.InlineKeyboardButton("далее",callback_data='settlement +')

						markup.add(item1,item3,item2)
						markup.add(item_start)
						


						bot.delete_message(str(call.message.chat.id), call.message.id)
						bot.send_message(str(call.message.chat.id),'выберите Город из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)



					else:

						
						database_user[str(call.message.chat.id)]["settlement_numb"] = int((len(database_user[str(call.message.chat.id)]["cashe"])/7))
						markup=types.InlineKeyboardMarkup()


						a=area_list(database_user[str(call.message.chat.id)]["cashe"],int((len(database_user[str(call.message.chat.id)]["cashe"])/7)))
						for i in a:
							item1=types.InlineKeyboardButton(i[0],callback_data=("settlementCode " + i[1]))
							markup.add(item1)



						item1=types.InlineKeyboardButton("назад",callback_data='settlement -')
						item3=types.InlineKeyboardButton("["+str(database_user[str(call.message.chat.id)]["settlement_numb"])\
							+"/"+str(int((len(database_user[str(call.message.chat.id)]["cashe"])/7)))+"]",callback_data='chet')
						item2=types.InlineKeyboardButton("далее",callback_data='settlement +')
						markup.add(item1,item3,item2)
						markup.add(item_start)
						bot.delete_message(str(call.message.chat.id), call.message.id)
						bot.send_message(str(call.message.chat.id),'выберите Город из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)



				#сельский домик ееееееееееее ----------------------

				if call.data.split()[0] == 'settlementCode':
					cw.settlementCode_func(bot, call ,database_user)

				#сельский адрес ----------------------------------


				#город-------------------------------------------

				if call.data.split()[0]== "citi":
					cn.citi_next(bot,call,database_user)

						
				#улицы-------------------------------------------

				if call.data.split()[0] == 'citiCode':
					cw.citiCode_func(bot, call,database_user)

				if call.data == "street -": 
					if 0< (database_user[str(call.message.chat.id)]["street_numb"] -1): 
						# эта страшная черуха сравнивает колво страниц с номером на которой ты уже находишь +1 
						# если листов больше ,то перебросит на следущий , если листов меньше , то кинет на лист первый(0)
						database_user[str(call.message.chat.id)]["street_numb"] = database_user[str(call.message.chat.id)]["street_numb"] -1
						 
						markup=types.InlineKeyboardMarkup()
						a=street_list(database_user[str(call.message.chat.id)]["cashe"],database_user[str(call.message.chat.id)]["street_numb"])
						for i in a:
							item1=types.InlineKeyboardButton(i[0],callback_data=("streetCode " + i[1]))
							markup.add(item1)

						item1=types.InlineKeyboardButton("назад",callback_data='street -')
						item3=types.InlineKeyboardButton("["+str(database_user[str(call.message.chat.id)]["street_numb"])\
							+"/"+str(int((len(database_user[str(call.message.chat.id)]["cashe"])/20)))+"]",callback_data='chet')
						item2=types.InlineKeyboardButton("далее",callback_data='street +')

						markup.add(item1,item3,item2)
						markup.add(item_start)
						


						bot.delete_message(str(call.message.chat.id), call.message.id)
						bot.send_message(str(call.message.chat.id),'выберите субъект из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)

						
					else:

						database_user[str(call.message.chat.id)]["street_numb"] = int((len(database_user[str(call.message.chat.id)]["cashe"]))/20)
						 
						markup=types.InlineKeyboardMarkup()
						a=street_list(database_user[str(call.message.chat.id)]["cashe"],database_user[str(call.message.chat.id)]["street_numb"])
						for i in a:
							item1=types.InlineKeyboardButton(i[0],callback_data=("streetCode " + i[1]))
							markup.add(item1)

						item1=types.InlineKeyboardButton("назад",callback_data='street -')
						item3=types.InlineKeyboardButton("["+str(database_user[str(call.message.chat.id)]["street_numb"])\
							+"/"+str(int((len(database_user[str(call.message.chat.id)]["cashe"])/20)))+"]",callback_data='chet')
						item2=types.InlineKeyboardButton("далее",callback_data='street +')
						markup.add(item1,item3,item2)
						markup.add(item_start)
						bot.delete_message(str(call.message.chat.id), call.message.id)
						bot.send_message(str(call.message.chat.id),'выберите субъект из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)	
				if call.data == "street +": 
					if int(int((len(database_user[str(call.message.chat.id)]["cashe"])/20))) >= (database_user[str(call.message.chat.id)]["street_numb"] +1): 
						# эта страшная черуха сравнивает колво страниц с номером на которой ты уже находишь +1 
						# если листов больше ,то перебросит на следущий , если листов меньше , то кинет на лист первый(0)
						database_user[str(call.message.chat.id)]["street_numb"] = database_user[str(call.message.chat.id)]["street_numb"] +1
						 
						markup=types.InlineKeyboardMarkup()
						a=street_list(database_user[str(call.message.chat.id)]["cashe"],database_user[str(call.message.chat.id)]["street_numb"])
						for i in a:
							item1=types.InlineKeyboardButton(i[0],callback_data=("streetCode " + i[1]))
							markup.add(item1)

						item1=types.InlineKeyboardButton("назад",callback_data='street -')
						item3=types.InlineKeyboardButton("["+str(database_user[str(call.message.chat.id)]["street_numb"])\
							+"/"+str(int((len(database_user[str(call.message.chat.id)]["cashe"])/20)))+"]",callback_data='chet')
						item2=types.InlineKeyboardButton("далее",callback_data='street +')

						markup.add(item1,item3,item2)
						markup.add(item_start)
						

						bot.delete_message(str(call.message.chat.id), call.message.id)
						bot.send_message(str(call.message.chat.id),'выберите субъект из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)

						
					else:

						database_user[str(call.message.chat.id)]["street_numb"] = 0
						 
						markup=types.InlineKeyboardMarkup()
						a=street_list(database_user[str(call.message.chat.id)]["cashe"],database_user[str(call.message.chat.id)]["street_numb"])
						for i in a:
							item1=types.InlineKeyboardButton(i[0],callback_data=("streetCode " + i[1]))
							markup.add(item1)

						item1=types.InlineKeyboardButton("назад",callback_data='street -')
						item3=types.InlineKeyboardButton("["+str(database_user[str(call.message.chat.id)]["street_numb"])\
							+"/"+str(int((len(database_user[str(call.message.chat.id)]["cashe"])/20)))+"]",callback_data='chet')
						item2=types.InlineKeyboardButton("далее",callback_data='street +')
						markup.add(item1,item3,item2)
						markup.add(item_start)
						bot.delete_message(str(call.message.chat.id), call.message.id)
						bot.send_message(str(call.message.chat.id),'выберите субъект из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)	






				if call.data == "chet": 
					bot.answer_callback_query(call.id, "я просто счетчик , не тыкай на меня позязя)", show_alert=True)


				if call.data.split()[0] == 'streetCode':
					cw.streetCode_func(bot, call,database_user)

				if call.data == "home -": 
					if 0<= (database_user[str(call.message.chat.id)]["home_numb"] -1): 
						# эта страшная черуха сравнивает колво страниц с номером на которой ты уже находишь +1 
						# если листов больше ,то перебросит на следущий , если листов меньше , то кинет на лист первый(0)
						database_user[str(call.message.chat.id)]["home_numb"] = database_user[str(call.message.chat.id)]["home_numb"] -1
						 
						markup=types.InlineKeyboardMarkup()
						a=home_list(database_user[str(call.message.chat.id)]["cashe"],database_user[str(call.message.chat.id)]["home_numb"])
						for i in a:
							item1=types.InlineKeyboardButton(i[0],callback_data=("data " + i[1]))
							markup.add(item1)

						item1=types.InlineKeyboardButton("назад",callback_data='home -')
						item3=types.InlineKeyboardButton("["+str(database_user[str(call.message.chat.id)]["home_numb"])\
							+"/"+str(int((len(database_user[str(call.message.chat.id)]["cashe"])/7)))+"]",callback_data='chet')
						item2=types.InlineKeyboardButton("далее",callback_data='home +')

						markup.add(item1,item3,item2)
						markup.add(item_start)
						
						bot.delete_message(str(call.message.chat.id), call.message.id)
						bot.send_message(str(call.message.chat.id),'выберите субъект из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)

						
					else:

						database_user[str(call.message.chat.id)]["home_numb"] = int((len(database_user[str(call.message.chat.id)]["cashe"]))/25)
						 
						markup=types.InlineKeyboardMarkup()
						a=home_list(database_user[str(call.message.chat.id)]["cashe"],database_user[str(call.message.chat.id)]["home_numb"])
						for i in a:
							item1=types.InlineKeyboardButton(i[0],callback_data=("data " + i[1]))
							markup.add(item1)

						item1=types.InlineKeyboardButton("назад",callback_data='home -')
						item3=types.InlineKeyboardButton("["+str(database_user[str(call.message.chat.id)]["home_numb"])\
							+"/"+str(int((len(database_user[str(call.message.chat.id)]["cashe"])/25)))+"]",callback_data='chet')
						item2=types.InlineKeyboardButton("далее",callback_data='home +')
						markup.add(item1,item3,item2)
						markup.add(item_start)
						bot.delete_message(str(call.message.chat.id), call.message.id)
						bot.send_message(str(call.message.chat.id),'выберите субъект из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)	
				if call.data == "home +": 
					if int(int((len(database_user[str(call.message.chat.id)]["cashe"])/25))) >= (database_user[str(call.message.chat.id)]["home_numb"] +1): 
						# эта страшная черуха сравнивает колво страниц с номером на которой ты уже находишь +1 
						# если листов больше ,то перебросит на следущий , если листов меньше , то кинет на лист первый(0)
						database_user[str(call.message.chat.id)]["home_numb"] = database_user[str(call.message.chat.id)]["home_numb"] +1
						 
						markup=types.InlineKeyboardMarkup()
						a=home_list(database_user[str(call.message.chat.id)]["cashe"],database_user[str(call.message.chat.id)]["home_numb"])
						for i in a:
							item1=types.InlineKeyboardButton(i[0],callback_data=("data " + i[1]))
							markup.add(item1)

						item1=types.InlineKeyboardButton("назад",callback_data='home -')
						item3=types.InlineKeyboardButton("["+str(database_user[str(call.message.chat.id)]["home_numb"])\
							+"/"+str(int((len(database_user[str(call.message.chat.id)]["cashe"])/25)))+"]",callback_data='chet')
						item2=types.InlineKeyboardButton("далее",callback_data='home +')

						markup.add(item1,item3,item2)
						markup.add(item_start)
						


						bot.delete_message(str(call.message.chat.id), call.message.id)
						bot.send_message(str(call.message.chat.id),'выберите субъект из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)

						
					else:

						database_user[str(call.message.chat.id)]["home_numb"] = 0
						 
						markup=types.InlineKeyboardMarkup()
						a=home_list(database_user[str(call.message.chat.id)]["cashe"],database_user[str(call.message.chat.id)]["home_numb"])
						for i in a:
							item1=types.InlineKeyboardButton(i[0],callback_data=("data " + i[1]))
							markup.add(item1)

						item1=types.InlineKeyboardButton("назад",callback_data='home -')
						item3=types.InlineKeyboardButton("["+str(database_user[str(call.message.chat.id)]["home_numb"])\
							+"/"+str(int((len(database_user[str(call.message.chat.id)]["cashe"])/25)))+"]",callback_data='chet')
						item2=types.InlineKeyboardButton("далее",callback_data='home +')
						markup.add(item1,item3,item2)
						markup.add(item_start)
						bot.delete_message(str(call.message.chat.id), call.message.id)
						bot.send_message(str(call.message.chat.id),'выберите субъект из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)	




				if call.data.split()[0] == 'data_text':
					text =  gd.get_compuni(\
						database_user[str(call.message.chat.id)]["regions"],\
						database_user[str(call.message.chat.id)]["citi"],\
						database_user[str(call.message.chat.id)]["street"],\
						database_user[str(call.message.chat.id)]["home"],\
						)

					bot.send_message(str(call.message.chat.id),text)	

				if call.data.split()[0] == 'data_vilage_text':
					text =  gd.get_compuni_vilage(\
						database_user[str(call.message.chat.id)]["regions"],\
						database_user[str(call.message.chat.id)]["area"],
						database_user[str(call.message.chat.id)]["settlementCode"],
						database_user[str(call.message.chat.id)]["streetCode"],call.data.split()[1]


						)
					bot.send_message(str(call.message.chat.id),text)	


				if call.data.split()[0] == 'data':
					markup=types.InlineKeyboardMarkup()
					item1=types.InlineKeyboardButton("верно",callback_data="data_text")
					markup.add(item1)
					markup.add(item_start)
					cw.get_adres_text(call,database_user)
					database_user[str(call.message.chat.id)]["home"]  = call.data.split()[1]
					text = database_user[str(call.message.chat.id)]["adres"]
					bot.send_message(str(call.message.chat.id),text,reply_markup=markup)	

				if call.data.split()[0] == 'data_vilage':
					markup=types.InlineKeyboardMarkup()
					item1=types.InlineKeyboardButton("верно",callback_data="data_vilage_text")
					markup.add(item1)
					markup.add(item_start)


					cw.get_adres_text(call,database_user)
					database_user[str(call.message.chat.id)]["home"]  = call.data.split()[1]
					text = database_user[str(call.message.chat.id)]["adres"]
					bot.send_message(str(call.message.chat.id),text,reply_markup=markup)	

				if call.data == "start_t": 
					markup=types.InlineKeyboardMarkup()
					a=regions_list(regions,0)
					for i in a:
						item1=types.InlineKeyboardButton(i[0],callback_data=("regionCode " + i[1]))
						markup.add(item1)
					item1=types.InlineKeyboardButton("назад",callback_data='regions -')
					item3=types.InlineKeyboardButton("[0/"+str(int((len(regions)/8)))+"]",callback_data='chet')
					item2=types.InlineKeyboardButton("далее",callback_data='regions +')

					markup.add(item1,item3,item2)
					markup.add(item_start)
					database_user[str(call.message.chat.id)]= {
						"regions_numb":0,#номер страницы 
						"citi_numb":0,
						"adres":""
					}
					
					bot.send_message(str(call.message.chat.id),'Выберите регион',reply_markup=markup)
						
				if call.data == "chet": 
					bot.answer_callback_query(call.id, "я просто счетчик , не тыкай на меня позязя)", show_alert=True)

				if call.data == "delete": 
					bot.delete_message(str(call.message.chat.id), call.message.id)

			except Exception as e:
				database_user[int(call.message.chat.id)]= {
						"regions_numb":0,#номер страницы 
						"citi_numb":0,
						"adres":""
					}
				bot.send_message(str(call.message.chat.id),'Сожалею , но случилась ошибка . Чтобы продолжить напишите "начать"')
				print(e)

			with open('file/database_user.json', "w",encoding='utf-8') as file:
				json.dump(database_user, file, indent=4, ensure_ascii=False)
		bot.polling(none_stop=True, interval=0)
	except Exception as e:
		pass
