import requests
import json
import telebot
from telebot import types
import math

import pypo.getdata as gd #импорт функция из файла getdata в pypo 
bot = telebot.TeleBot('5225585818:AAGSLsqeM02iZ5JwvEuocZmK9X4P2vlP6eE')


with open('database_user.json', 'r',encoding='utf-8') as fp:
	database_user = json.load(fp)



with open('regions.json', 'r',encoding='utf-8') as fp:
	regions = json.load(fp)


item_start =types.InlineKeyboardButton("в начало",callback_data='start_t')


"""
функции с приставкой _list отвечают за вытаскивание из полученых данных
названия например городов и строки-кода для следущего запроса
"""

def regions_list(list,numb):
	#возращает 4 элемента из списка регионов 
	a = []

	b = 0#счетчик для обрезки по 4
	c = []#подсписок
	for i in list:

		if b<8:
			c.append([i["offName"] +' '+ i["shortName"], i["aoGuid"]])
			b=b+1
		
		else:
			a.append(c)
			c = []
			c.append([i["offName"] +' '+ i["shortName"], i["aoGuid"]])
			b = 1
	if len(c)!=0:#защита от того что последняя страница окажется не полной
		a.append(c)

	print(numb)
	if numb == 0 :
		a[numb].insert(0,['Хакасия Республика', '8d3f1d35-f0f4-41b5-b5b7-e7cadf3e7bd7'])

	return(a[numb])

def vilage_list(list,numb):
	#возращает 4 элемента из списка регионов 
	a = []

	b = 0#счетчик для обрезки по 4
	c = []#подсписок
	for i in list:

		if b<4:
			c.append([i["formalName"] , i["aoGuid"]])
			b=b+1
		
		else:
			a.append(c)
			c = []
			c.append([i["formalName"] , i["aoGuid"]])
			b = 1
	if len(c)!=0:#защита от того что последняя страница окажется не полной
		a.append(c)
	return(a[numb])

def citi_list(list,numb):
	#возращает 4 элемента из списка регионов 
	a = []

	b = 0#счетчик для обрезки по 4
	c = []#подсписок
	for i in list:

		if b<4:
			c.append([i["formalName"] , i["aoGuid"]])
			b=b+1
		
		else:
			a.append(c)
			c = []
			c.append([i["formalName"] , i["aoGuid"]])
			b = 1
	if len(c)!=0:#защита от того что последняя страница окажется не полной
		a.append(c)
	return(a[numb])

def area_list(list,numb):
	#возращает 4 элемента из списка регионов 
	#print(list)
	a = []

	b = 0#счетчик для обрезки по 4
	c = []#подсписок
	for i in list:

		if b<4:
			c.append([i["formalName"] , i["aoGuid"]])
			b=b+1
		
		else:
			a.append(c)
			c = []
			c.append([i["formalName"] , i["aoGuid"]])
			b = 1
	if len(c)!=0:#защита от того что последняя страница окажется не полной
		a.append(c)

	#print(numb)

	return(a[numb])
def street_list(list,numb):
	#возращает 4 элемента из списка регионов 
	a = []

	b = 0#счетчик для обрезки по 4
	c = []#подсписок
	for i in list:

		if b<7:
			c.append([i["formalName"] , i["aoGuid"]])
			b=b+1
		
		else:
			a.append(c)
			c = []
			c.append([i["formalName"] , i["aoGuid"]])
			b = 1
	if len(c)!=0:#защита от того что последняя страница окажется не полной
		a.append(c)

	#print(numb)


	return(a[numb])


def home_list(list,numb):
	#возращает 4 элемента из списка регионов 
	a = []

	b = 0#счетчик для обрезки по 4
	c = []#подсписок
	for i in list:

		if b<7:
			c.append([i["formattedAddress"].split(",")[-1] , i["houseGuid"]])
			b=b+1
		
		else:
			a.append(c)
			c = []
			c.append([i["formattedAddress"].split(",")[-1] , i["houseGuid"]])
			b = 1
	if len(c)!=0:#защита от того что последняя страница окажется не полной
		a.append(c)

	print(numb)


	return(a[numb])







# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
def start(m, res=False):
	bot.send_message(m.chat.id, 'Напишите "начать" для поиска управляющих и ресурсоснабжающих организаций поадресу')
# Получение сообщений от юзера


#----------------

@bot.message_handler(content_types=["text"])

def handle_text(message):
	#print(database_user)
	if (int(message.chat.id) in database_user) == False:
		database_user[int(message.chat.id)]= {
				"regions_numb":0,#номер страницы 
				"citi_numb":0,
				"adres":""
			}

		#print(database_user)

		with open("database_user.json", "w",encoding='utf-8') as file:
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
		
		bot.send_message(message.chat.id,'выберите субъект из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)




	else:
		bot.send_message(message.chat.id, 'Вы написали: ' + message.text)
# Запускаем бота


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
	try:



		if call.data == "regions -": 
			if 0<= (database_user[str(call.message.chat.id)]["regions_numb"] -1): 
				# это функция сравнивает колво страниц с номером на которой ты уже находишь +1 
				# если листов больше ,то перебросит на следущий , если листов меньше , то кинет на лист первый(0)
				database_user[str(call.message.chat.id)]["regions_numb"] = database_user[str(call.message.chat.id)]["regions_numb"] -1
				 
				markup=types.InlineKeyboardMarkup()
				a=regions_list(regions,database_user[str(call.message.chat.id)]["regions_numb"])
				for i in a:
					item1=types.InlineKeyboardButton(i[0],callback_data=("regionCode " + i[1]))
					markup.add(item1)

				item1=types.InlineKeyboardButton("назад",callback_data='regions -')
				item3=types.InlineKeyboardButton("["+str(database_user[str(call.message.chat.id)]["regions_numb"])\
					+"/"+str(int((len(regions)/8)))+"]",callback_data='chet')
				item2=types.InlineKeyboardButton("далее",callback_data='regions +')

				markup.add(item1,item3,item2)
				markup.add(item_start)
				


				bot.delete_message(str(call.message.chat.id), call.message.id)
				bot.send_message(str(call.message.chat.id),'выберите субъект из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)

				
			else:

				database_user[str(call.message.chat.id)]["regions_numb"] = int((len(regions)/8))
				 
				markup=types.InlineKeyboardMarkup()
				a=regions_list(regions,database_user[str(call.message.chat.id)]["regions_numb"])
				for i in a:
					item1=types.InlineKeyboardButton(i[0],callback_data=("regionCode " + i[1]))
					markup.add(item1)

				item1=types.InlineKeyboardButton("назад",callback_data='regions -')
				item3=types.InlineKeyboardButton("["+str(database_user[str(call.message.chat.id)]["regions_numb"])\
					+"/"+str(int((len(regions)/8)))+"]",callback_data='chet')
				item2=types.InlineKeyboardButton("далее",callback_data='regions +')
				markup.add(item1,item3,item2)
				markup.add(item_start)
				bot.delete_message(str(call.message.chat.id), call.message.id)
				bot.send_message(str(call.message.chat.id),'выберите субъект из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)	
		if call.data == "regions +": 
			if int(int((len(regions)/8))) >= (database_user[str(call.message.chat.id)]["regions_numb"] +1): 
				# эта страшная черуха сравнивает колво страниц с номером на которой ты уже находишь +1 
				# если листов больше ,то перебросит на следущий , если листов меньше , то кинет на лист первый(0)
				database_user[str(call.message.chat.id)]["regions_numb"] = database_user[str(call.message.chat.id)]["regions_numb"] +1
				 
				markup=types.InlineKeyboardMarkup()
				a=regions_list(regions,database_user[str(call.message.chat.id)]["regions_numb"])
				for i in a:

					item1=types.InlineKeyboardButton(i[0],callback_data=("regionCode " + i[1]))
					markup.add(item1)

				item1=types.InlineKeyboardButton("назад",callback_data='regions -')
				item3=types.InlineKeyboardButton("["+str(database_user[str(call.message.chat.id)]["regions_numb"])\
					+"/"+str(int((len(regions)/8)))+"]",callback_data='chet')
				item2=types.InlineKeyboardButton("далее",callback_data='regions +')

				markup.add(item1,item3,item2)
				markup.add(item_start)
				


				bot.delete_message(str(call.message.chat.id), call.message.id)
				bot.send_message(str(call.message.chat.id),'выберите субъект из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)

				
			else:

				database_user[str(call.message.chat.id)]["regions_numb"] = 0
				 
				markup=types.InlineKeyboardMarkup()
				a=regions_list(regions,database_user[str(call.message.chat.id)]["regions_numb"])
				for i in a:

					item1=types.InlineKeyboardButton(i[0],callback_data=("regionCode " + i[1] + " "+i[0]))
					markup.add(item1)

				item1=types.InlineKeyboardButton("назад",callback_data='regions -')
				item3=types.InlineKeyboardButton("["+str(database_user[str(call.message.chat.id)]["regions_numb"])\
					+"/"+str(int((len(regions)/8)))+"]",callback_data='chet')
				item2=types.InlineKeyboardButton("далее",callback_data='regions +')
				markup.add(item1,item3,item2)
				markup.add(item_start)
				bot.delete_message(str(call.message.chat.id), call.message.id)
				bot.send_message(str(call.message.chat.id),'выберите субъект из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)		

		#район или город-------------------------------------------


		if call.data.split()[0] == "regionCode":
			database_user[str(call.message.chat.id)]["regions"]  = call.data.split()[1]
			database_user[str(call.message.chat.id)]["adres"]  = call.data.split()[2]
			print(database_user)
			markup=types.InlineKeyboardMarkup()
			item1=types.InlineKeyboardButton("Город",callback_data='citi')
			item2=types.InlineKeyboardButton("Район",callback_data='area')
			markup.add(item1,item2)

			bot.delete_message(str(call.message.chat.id), call.message.id)
			bot.send_message(str(call.message.chat.id),'выберите Город или Район',reply_markup=markup)	
			
		

		#Район----------------------------------------------

		if call.data== "area":
			database_user[str(call.message.chat.id)]["cashe"] =  gd.get_area(database_user[str(call.message.chat.id)]["regions"])
			database_user[str(call.message.chat.id)]["area_numb"] = 0
			markup=types.InlineKeyboardMarkup()


			a=area_list(database_user[str(call.message.chat.id)]["cashe"],0)
			for i in a:
				item1=types.InlineKeyboardButton(i[0],callback_data=("areaCode " + i[1]))
				markup.add(item1)



			item1=types.InlineKeyboardButton("назад",callback_data='area -')
			item3=types.InlineKeyboardButton("["+str(database_user[str(call.message.chat.id)]["area_numb"])\
				+"/"+str(int((len(database_user[str(call.message.chat.id)]["cashe"])/4)))+"]",callback_data='chet')
			item2=types.InlineKeyboardButton("далее",callback_data='area +')
			markup.add(item1,item3,item2)
			markup.add(item_start)
			bot.delete_message(str(call.message.chat.id), call.message.id)
			bot.send_message(str(call.message.chat.id),'выберите Район из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)
			





		if call.data == "area +": 
			if int(int((len(database_user[str(call.message.chat.id)]["cashe"])/4))) > (database_user[str(call.message.chat.id)]["area_numb"] +1): 
				# эта страшная черуха сравнивает колво страниц с номером на которой ты уже находишь +1 
				# если листов больше ,то перебросит на следущий , если листов меньше , то кинет на лист первый(0)
				database_user[str(call.message.chat.id)]["area_numb"] = database_user[str(call.message.chat.id)]["area_numb"] +1
				 
				markup=types.InlineKeyboardMarkup()
				a=area_list(database_user[str(call.message.chat.id)]["cashe"],database_user[str(call.message.chat.id)]["area_numb"])
				for i in a:
					item1=types.InlineKeyboardButton(i[0],callback_data=("areaCode " + i[1]))
					markup.add(item1)

				item1=types.InlineKeyboardButton("назад",callback_data='area -')
				item3=types.InlineKeyboardButton("["+str(database_user[str(call.message.chat.id)]["area_numb"])\
					+"/"+str(int((len(database_user[str(call.message.chat.id)]["cashe"])/4)))+"]",callback_data='chet')
				item2=types.InlineKeyboardButton("далее",callback_data='area +')

				markup.add(item1,item3,item2)
				markup.add(item_start)
				


				bot.delete_message(str(call.message.chat.id), call.message.id)
				bot.send_message(str(call.message.chat.id),'выберите Район из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)

			else:
				
				database_user[str(call.message.chat.id)]["area_numb"] = 0
				markup=types.InlineKeyboardMarkup()


				a=area_list(database_user[str(call.message.chat.id)]["cashe"],0)
				for i in a:
					item1=types.InlineKeyboardButton(i[0],callback_data=("areaCode " + i[1]))
					markup.add(item1)



				item1=types.InlineKeyboardButton("назад",callback_data='area -')
				item3=types.InlineKeyboardButton("["+str(database_user[str(call.message.chat.id)]["area_numb"])\
					+"/"+str(int((len(database_user[str(call.message.chat.id)]["cashe"])/4)))+"]",callback_data='chet')
				item2=types.InlineKeyboardButton("далее",callback_data='area +')
				markup.add(item1,item3,item2)
				markup.add(item_start)
				bot.delete_message(str(call.message.chat.id), call.message.id)
				bot.send_message(str(call.message.chat.id),'выберите Район из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)

				


		if call.data == "area -": 
			if 0<= (database_user[str(call.message.chat.id)]["area_numb"] -1): 
				# эта страшная черуха сравнивает колво страниц с номером на которой ты уже находишь +1 
				# если листов больше ,то перебросит на следущий , если листов меньше , то кинет на лист первый(0)
				database_user[str(call.message.chat.id)]["area_numb"] = database_user[str(call.message.chat.id)]["area_numb"] -1
				 
				markup=types.InlineKeyboardMarkup()
				a=area_list(database_user[str(call.message.chat.id)]["cashe"],database_user[str(call.message.chat.id)]["area_numb"])
				for i in a:
					item1=types.InlineKeyboardButton(i[0],callback_data=("areaCode " + i[1]))
					markup.add(item1)

				item1=types.InlineKeyboardButton("назад",callback_data='area -')
				item3=types.InlineKeyboardButton("["+str(database_user[str(call.message.chat.id)]["area_numb"])\
					+"/"+str(int((len(database_user[str(call.message.chat.id)]["cashe"])/4)))+"]",callback_data='chet')
				item2=types.InlineKeyboardButton("далее",callback_data='area +')

				markup.add(item1,item3,item2)
				markup.add(item_start)
				


				bot.delete_message(str(call.message.chat.id), call.message.id)
				bot.send_message(str(call.message.chat.id),'выберите Район из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)



			else:

				
				database_user[str(call.message.chat.id)]["area_numb"] = int((len(database_user[str(call.message.chat.id)]["cashe"])/4))
				markup=types.InlineKeyboardMarkup()


				a=area_list(database_user[str(call.message.chat.id)]["cashe"],int((len(database_user[str(call.message.chat.id)]["cashe"])/4)))
				for i in a:
					item1=types.InlineKeyboardButton(i[0],callback_data=("areaCode " + i[1]))
					markup.add(item1)



				item1=types.InlineKeyboardButton("назад",callback_data='area -')
				item3=types.InlineKeyboardButton("["+str(database_user[str(call.message.chat.id)]["area_numb"])\
					+"/"+str(int((len(database_user[str(call.message.chat.id)]["cashe"])/4)))+"]",callback_data='chet')
				item2=types.InlineKeyboardButton("далее",callback_data='area +')
				markup.add(item1,item3,item2)
				markup.add(item_start)
				bot.delete_message(str(call.message.chat.id), call.message.id)
				bot.send_message(str(call.message.chat.id),'выберите Район из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)



		#населенный пункт -----------------------------------
		if call.data.split()[0] == 'areaCode':
			

			database_user[str(call.message.chat.id)]["area"]  = call.data.split()[1]
			database_user[str(call.message.chat.id)]["cashe"] =  gd.get_vilage(\
				database_user[str(call.message.chat.id)]["regions"],\
				database_user[str(call.message.chat.id)]["area"]
				)
			markup=types.InlineKeyboardMarkup()
			a=vilage_list(database_user[str(call.message.chat.id)]["cashe"],0)
			for i in a:
				item1=types.InlineKeyboardButton(i[0],callback_data=("vilageCode " + i[1]))
				markup.add(item1)

			database_user[str(call.message.chat.id)]["vilage_numb"] = 0

			item1=types.InlineKeyboardButton("назад",callback_data='vilage -')
			item3=types.InlineKeyboardButton("["+str(database_user[str(call.message.chat.id)]["area_numb"])\
				+"/"+str(int((len(database_user[str(call.message.chat.id)]["cashe"])/7)))+"]",callback_data='chet')
			item2=types.InlineKeyboardButton("далее",callback_data='vilage +')
			markup.add(item1,item3,item2)
			markup.add(item_start)
			bot.delete_message(str(call.message.chat.id), call.message.id)
			bot.send_message(str(call.message.chat.id),'выберите улицу из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)
		if call.data== "vilage":
			database_user[str(call.message.chat.id)]["cashe"] =  gd.get_vilages(database_user[str(call.message.chat.id)]["regions"])
			database_user[str(call.message.chat.id)]["vilage_numb"] = 0
			markup=types.InlineKeyboardMarkup()


			a=area_list(database_user[str(call.message.chat.id)]["cashe"],0)
			for i in a:
				item1=types.InlineKeyboardButton(i[0],callback_data=("vilageCode " + i[1]))
				markup.add(item1)



			item1=types.InlineKeyboardButton("назад",callback_data='vilage -')
			item3=types.InlineKeyboardButton("["+str(database_user[str(call.message.chat.id)]["vilage_numb"])\
				+"/"+str(int((len(database_user[str(call.message.chat.id)]["cashe"])/4)))+"]",callback_data='chet')
			item2=types.InlineKeyboardButton("далее",callback_data='vilage +')
			markup.add(item1,item3,item2)
			markup.add(item_start)
			bot.delete_message(str(call.message.chat.id), call.message.id)
			bot.send_message(str(call.message.chat.id),'выберите Город из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)
			





		if call.data == "vilage +": 
			if int(int((len(database_user[str(call.message.chat.id)]["cashe"])/4))) > (database_user[str(call.message.chat.id)]["vilage_numb"] +1): 
				# эта страшная черуха сравнивает колво страниц с номером на которой ты уже находишь +1 
				# если листов больше ,то перебросит на следущий , если листов меньше , то кинет на лист первый(0)
				database_user[str(call.message.chat.id)]["vilage_numb"] = database_user[str(call.message.chat.id)]["vilage_numb"] +1
				 
				markup=types.InlineKeyboardMarkup()
				a=area_list(database_user[str(call.message.chat.id)]["cashe"],database_user[str(call.message.chat.id)]["vilage_numb"])
				for i in a:
					item1=types.InlineKeyboardButton(i[0],callback_data=("vilageCode " + i[1]))
					markup.add(item1)

				item1=types.InlineKeyboardButton("назад",callback_data='vilage -')
				item3=types.InlineKeyboardButton("["+str(database_user[str(call.message.chat.id)]["vilage_numb"])\
					+"/"+str(int((len(database_user[str(call.message.chat.id)]["cashe"])/4)))+"]",callback_data='chet')
				item2=types.InlineKeyboardButton("далее",callback_data='vilage +')

				markup.add(item1,item3,item2)
				markup.add(item_start)
				


				bot.delete_message(str(call.message.chat.id), call.message.id)
				bot.send_message(str(call.message.chat.id),'выберите Город из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)

			else:
				
				database_user[str(call.message.chat.id)]["vilage_numb"] = 0
				markup=types.InlineKeyboardMarkup()


				a=area_list(database_user[str(call.message.chat.id)]["cashe"],0)
				for i in a:
					item1=types.InlineKeyboardButton(i[0],callback_data=("vilageCode " + i[1]))
					markup.add(item1)



				item1=types.InlineKeyboardButton("назад",callback_data='vilage -')
				item3=types.InlineKeyboardButton("["+str(database_user[str(call.message.chat.id)]["vilage_numb"])\
					+"/"+str(int((len(database_user[str(call.message.chat.id)]["cashe"])/4)))+"]",callback_data='chet')
				item2=types.InlineKeyboardButton("далее",callback_data='vilage +')
				markup.add(item1,item3,item2)
				markup.add(item_start)
				bot.delete_message(str(call.message.chat.id), call.message.id)
				bot.send_message(str(call.message.chat.id),'выберите Город из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)

				


		if call.data == "vilage -": 
			if 0<= (database_user[str(call.message.chat.id)]["vilage_numb"] -1): 
				# эта страшная черуха сравнивает колво страниц с номером на которой ты уже находишь +1 
				# если листов больше ,то перебросит на следущий , если листов меньше , то кинет на лист первый(0)
				database_user[str(call.message.chat.id)]["vilage_numb"] = database_user[str(call.message.chat.id)]["vilage_numb"] -1
				 
				markup=types.InlineKeyboardMarkup()
				a=area_list(database_user[str(call.message.chat.id)]["cashe"],database_user[str(call.message.chat.id)]["vilage_numb"])
				for i in a:
					item1=types.InlineKeyboardButton(i[0],callback_data=("vilageCode " + i[1]))
					markup.add(item1)

				item1=types.InlineKeyboardButton("назад",callback_data='vilage -')
				item3=types.InlineKeyboardButton("["+str(database_user[str(call.message.chat.id)]["vilage_numb"])\
					+"/"+str(int((len(database_user[str(call.message.chat.id)]["cashe"])/4)))+"]",callback_data='chet')
				item2=types.InlineKeyboardButton("далее",callback_data='vilage +')

				markup.add(item1,item3,item2)
				markup.add(item_start)
				


				bot.delete_message(str(call.message.chat.id), call.message.id)
				bot.send_message(str(call.message.chat.id),'выберите Город из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)



			else:

				
				database_user[str(call.message.chat.id)]["vilage_numb"] = int((len(database_user[str(call.message.chat.id)]["cashe"])/4))
				markup=types.InlineKeyboardMarkup()


				a=area_list(database_user[str(call.message.chat.id)]["cashe"],int((len(database_user[str(call.message.chat.id)]["cashe"])/4)))
				for i in a:
					item1=types.InlineKeyboardButton(i[0],callback_data=("vilageCode " + i[1]))
					markup.add(item1)



				item1=types.InlineKeyboardButton("назад",callback_data='vilage -')
				item3=types.InlineKeyboardButton("["+str(database_user[str(call.message.chat.id)]["vilage_numb"])\
					+"/"+str(int((len(database_user[str(call.message.chat.id)]["cashe"])/4)))+"]",callback_data='chet')
				item2=types.InlineKeyboardButton("далее",callback_data='vilage +')
				markup.add(item1,item3,item2)
				markup.add(item_start)
				bot.delete_message(str(call.message.chat.id), call.message.id)
				bot.send_message(str(call.message.chat.id),'выберите Город из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)

							

		if call.data.split()[0] == 'vilageCode':
			

			database_user[str(call.message.chat.id)]["settlementCode"]  = call.data.split()[1]
			database_user[str(call.message.chat.id)]["cashe"] =  gd.get_vilage_streat(\
				database_user[str(call.message.chat.id)]["regions"],\
				database_user[str(call.message.chat.id)]["area"],
				database_user[str(call.message.chat.id)]["settlementCode"]

				)
			markup=types.InlineKeyboardMarkup()
			a=vilage_list(database_user[str(call.message.chat.id)]["cashe"],0)
			for i in a:
				item1=types.InlineKeyboardButton(i[0],callback_data=("settlementCode " + i[1]))
				markup.add(item1)

			database_user[str(call.message.chat.id)]["settlement_numb"] = 0

			item1=types.InlineKeyboardButton("назад",callback_data='settlement -')
			item3=types.InlineKeyboardButton("["+str(database_user[str(call.message.chat.id)]["area_numb"])\
				+"/"+str(int((len(database_user[str(call.message.chat.id)]["cashe"])/7)))+"]",callback_data='chet')
			item2=types.InlineKeyboardButton("далее",callback_data='settlement +')
			markup.add(item1,item3,item2)
			markup.add(item_start)
			bot.delete_message(str(call.message.chat.id), call.message.id)
			bot.send_message(str(call.message.chat.id),'выберите улицу из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)

		if call.data == "settlement +": 
			if int(int((len(database_user[str(call.message.chat.id)]["cashe"])/4))) > (database_user[str(call.message.chat.id)]["settlement_numb"] +1): 
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
					+"/"+str(int((len(database_user[str(call.message.chat.id)]["cashe"])/4)))+"]",callback_data='chet')
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
					+"/"+str(int((len(database_user[str(call.message.chat.id)]["cashe"])/4)))+"]",callback_data='chet')
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
					+"/"+str(int((len(database_user[str(call.message.chat.id)]["cashe"])/4)))+"]",callback_data='chet')
				item2=types.InlineKeyboardButton("далее",callback_data='settlement +')

				markup.add(item1,item3,item2)
				markup.add(item_start)
				


				bot.delete_message(str(call.message.chat.id), call.message.id)
				bot.send_message(str(call.message.chat.id),'выберите Город из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)



			else:

				
				database_user[str(call.message.chat.id)]["settlement_numb"] = int((len(database_user[str(call.message.chat.id)]["cashe"])/4))
				markup=types.InlineKeyboardMarkup()


				a=area_list(database_user[str(call.message.chat.id)]["cashe"],int((len(database_user[str(call.message.chat.id)]["cashe"])/4)))
				for i in a:
					item1=types.InlineKeyboardButton(i[0],callback_data=("settlementCode " + i[1]))
					markup.add(item1)



				item1=types.InlineKeyboardButton("назад",callback_data='settlement -')
				item3=types.InlineKeyboardButton("["+str(database_user[str(call.message.chat.id)]["settlement_numb"])\
					+"/"+str(int((len(database_user[str(call.message.chat.id)]["cashe"])/4)))+"]",callback_data='chet')
				item2=types.InlineKeyboardButton("далее",callback_data='settlement +')
				markup.add(item1,item3,item2)
				markup.add(item_start)
				bot.delete_message(str(call.message.chat.id), call.message.id)
				bot.send_message(str(call.message.chat.id),'выберите Город из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)



		#сельский домик ееееееееееее ----------------------

		if call.data.split()[0] == 'settlementCode':
			

			database_user[str(call.message.chat.id)]["streetCode"]  = call.data.split()[1]
			database_user[str(call.message.chat.id)]["cashe"] =  gd.get_vilage_streat_home(\
				database_user[str(call.message.chat.id)]["regions"],\
				database_user[str(call.message.chat.id)]["area"],
				database_user[str(call.message.chat.id)]["settlementCode"],
				database_user[str(call.message.chat.id)]["streetCode"]


				)
			markup=types.InlineKeyboardMarkup()
			a=home_list(database_user[str(call.message.chat.id)]["cashe"],0)
			for i in a:
				item1=types.InlineKeyboardButton(i[0],callback_data=("data_vilage " + i[1]))
				markup.add(item1)

			database_user[str(call.message.chat.id)]["streetCode_numb"] = 0

			item1=types.InlineKeyboardButton("назад",callback_data='settlement -')
			item3=types.InlineKeyboardButton("["+str(database_user[str(call.message.chat.id)]["streetCode_numb"])\
				+"/"+str(int((len(database_user[str(call.message.chat.id)]["cashe"])/7)))+"]",callback_data='chet')
			item2=types.InlineKeyboardButton("далее",callback_data='settlement +')
			markup.add(item1,item3,item2)
			markup.add(item_start)
			bot.delete_message(str(call.message.chat.id), call.message.id)
			bot.send_message(str(call.message.chat.id),'выберите номер дома из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)



		#сельский адрес ----------------------------------

		if call.data.split()[0] == 'data_vilage':

			database_user[str(call.message.chat.id)]["home"]  = call.data.split()[1]
			text =  gd.get_compuni_vilage(\
				database_user[str(call.message.chat.id)]["regions"],\
				database_user[str(call.message.chat.id)]["area"],
				database_user[str(call.message.chat.id)]["settlementCode"],
				database_user[str(call.message.chat.id)]["streetCode"],call.data.split()[1]


				)




			bot.send_message(str(call.message.chat.id),text)	

		#город-------------------------------------------


		if call.data== "citi":
			database_user[str(call.message.chat.id)]["cashe"] =  gd.get_citis(database_user[str(call.message.chat.id)]["regions"])
			database_user[str(call.message.chat.id)]["citi_numb"] = 0
			markup=types.InlineKeyboardMarkup()


			a=area_list(database_user[str(call.message.chat.id)]["cashe"],0)
			for i in a:
				item1=types.InlineKeyboardButton(i[0],callback_data=("citiCode " + i[1]))
				markup.add(item1)



			item1=types.InlineKeyboardButton("назад",callback_data='citi -')
			item3=types.InlineKeyboardButton("["+str(database_user[str(call.message.chat.id)]["citi_numb"])\
				+"/"+str(int((len(database_user[str(call.message.chat.id)]["cashe"])/4)))+"]",callback_data='chet')
			item2=types.InlineKeyboardButton("далее",callback_data='citi +')
			markup.add(item1,item3,item2)
			markup.add(item_start)
			bot.delete_message(str(call.message.chat.id), call.message.id)
			bot.send_message(str(call.message.chat.id),'выберите Город из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)
			





		if call.data == "citi +": 
			if int(int((len(database_user[str(call.message.chat.id)]["cashe"])/4))) > (database_user[str(call.message.chat.id)]["citi_numb"] +1): 
				# эта страшная черуха сравнивает колво страниц с номером на которой ты уже находишь +1 
				# если листов больше ,то перебросит на следущий , если листов меньше , то кинет на лист первый(0)
				database_user[str(call.message.chat.id)]["citi_numb"] = database_user[str(call.message.chat.id)]["citi_numb"] +1
				 
				markup=types.InlineKeyboardMarkup()
				a=area_list(database_user[str(call.message.chat.id)]["cashe"],database_user[str(call.message.chat.id)]["citi_numb"])
				for i in a:
					item1=types.InlineKeyboardButton(i[0],callback_data=("citiCode " + i[1]))
					markup.add(item1)

				item1=types.InlineKeyboardButton("назад",callback_data='citi -')
				item3=types.InlineKeyboardButton("["+str(database_user[str(call.message.chat.id)]["citi_numb"])\
					+"/"+str(int((len(database_user[str(call.message.chat.id)]["cashe"])/4)))+"]",callback_data='chet')
				item2=types.InlineKeyboardButton("далее",callback_data='citi +')

				markup.add(item1,item3,item2)
				markup.add(item_start)
				


				bot.delete_message(str(call.message.chat.id), call.message.id)
				bot.send_message(str(call.message.chat.id),'выберите Город из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)

			else:
				
				database_user[str(call.message.chat.id)]["citi_numb"] = 0
				markup=types.InlineKeyboardMarkup()


				a=area_list(database_user[str(call.message.chat.id)]["cashe"],0)
				for i in a:
					item1=types.InlineKeyboardButton(i[0],callback_data=("citiCode " + i[1]))
					markup.add(item1)



				item1=types.InlineKeyboardButton("назад",callback_data='citi -')
				item3=types.InlineKeyboardButton("["+str(database_user[str(call.message.chat.id)]["citi_numb"])\
					+"/"+str(int((len(database_user[str(call.message.chat.id)]["cashe"])/4)))+"]",callback_data='chet')
				item2=types.InlineKeyboardButton("далее",callback_data='citi +')
				markup.add(item1,item3,item2)
				markup.add(item_start)
				bot.delete_message(str(call.message.chat.id), call.message.id)
				bot.send_message(str(call.message.chat.id),'выберите Город из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)

				


		if call.data == "citi -": 
			if 0<= (database_user[str(call.message.chat.id)]["citi_numb"] -1): 
				# эта страшная черуха сравнивает колво страниц с номером на которой ты уже находишь +1 
				# если листов больше ,то перебросит на следущий , если листов меньше , то кинет на лист первый(0)
				database_user[str(call.message.chat.id)]["citi_numb"] = database_user[str(call.message.chat.id)]["citi_numb"] -1
				 
				markup=types.InlineKeyboardMarkup()
				a=area_list(database_user[str(call.message.chat.id)]["cashe"],database_user[str(call.message.chat.id)]["citi_numb"])
				for i in a:
					item1=types.InlineKeyboardButton(i[0],callback_data=("citiCode " + i[1]))
					markup.add(item1)

				item1=types.InlineKeyboardButton("назад",callback_data='citi -')
				item3=types.InlineKeyboardButton("["+str(database_user[str(call.message.chat.id)]["citi_numb"])\
					+"/"+str(int((len(database_user[str(call.message.chat.id)]["cashe"])/4)))+"]",callback_data='chet')
				item2=types.InlineKeyboardButton("далее",callback_data='citi +')

				markup.add(item1,item3,item2)
				markup.add(item_start)
				


				bot.delete_message(str(call.message.chat.id), call.message.id)
				bot.send_message(str(call.message.chat.id),'выберите Город из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)



			else:

				
				database_user[str(call.message.chat.id)]["citi_numb"] = int((len(database_user[str(call.message.chat.id)]["cashe"])/4))
				markup=types.InlineKeyboardMarkup()


				a=area_list(database_user[str(call.message.chat.id)]["cashe"],int((len(database_user[str(call.message.chat.id)]["cashe"])/4)))
				for i in a:
					item1=types.InlineKeyboardButton(i[0],callback_data=("citiCode " + i[1]))
					markup.add(item1)



				item1=types.InlineKeyboardButton("назад",callback_data='citi -')
				item3=types.InlineKeyboardButton("["+str(database_user[str(call.message.chat.id)]["citi_numb"])\
					+"/"+str(int((len(database_user[str(call.message.chat.id)]["cashe"])/4)))+"]",callback_data='chet')
				item2=types.InlineKeyboardButton("далее",callback_data='citi +')
				markup.add(item1,item3,item2)
				markup.add(item_start)
				bot.delete_message(str(call.message.chat.id), call.message.id)
				bot.send_message(str(call.message.chat.id),'выберите Город из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)

				
		#улицы-------------------------------------------

		if call.data.split()[0] == 'citiCode':
			database_user[str(call.message.chat.id)]["citi"]  = call.data.split()[1]
			database_user[str(call.message.chat.id)]["cashe"] =  gd.get_streat(\
				database_user[str(call.message.chat.id)]["regions"],\
				database_user[str(call.message.chat.id)]["citi"]
				)
			markup=types.InlineKeyboardMarkup()
			a=street_list(database_user[str(call.message.chat.id)]["cashe"],0)
			for i in a:
				item1=types.InlineKeyboardButton(i[0],callback_data=("streetCode " + i[1]))
				markup.add(item1)

			database_user[str(call.message.chat.id)]["street_numb"] = 0

			item1=types.InlineKeyboardButton("назад",callback_data='street -')
			item3=types.InlineKeyboardButton("["+str(database_user[str(call.message.chat.id)]["street_numb"])\
				+"/"+str(int((len(database_user[str(call.message.chat.id)]["cashe"])/7)))+"]",callback_data='chet')
			item2=types.InlineKeyboardButton("далее",callback_data='street +')
			markup.add(item1,item3,item2)
			markup.add(item_start)
			bot.delete_message(str(call.message.chat.id), call.message.id)
			bot.send_message(str(call.message.chat.id),'выберите улицу из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)
				







		if call.data == "street -": 
			if 0<= (database_user[str(call.message.chat.id)]["street_numb"] -1): 
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
					+"/"+str(int((len(database_user[str(call.message.chat.id)]["cashe"])/7)))+"]",callback_data='chet')
				item2=types.InlineKeyboardButton("далее",callback_data='street +')

				markup.add(item1,item3,item2)
				markup.add(item_start)
				


				bot.delete_message(str(call.message.chat.id), call.message.id)
				bot.send_message(str(call.message.chat.id),'выберите субъект из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)

				
			else:

				database_user[str(call.message.chat.id)]["street_numb"] = int((len(database_user[str(call.message.chat.id)]["cashe"]))/7)
				 
				markup=types.InlineKeyboardMarkup()
				a=street_list(database_user[str(call.message.chat.id)]["cashe"],database_user[str(call.message.chat.id)]["street_numb"])
				for i in a:
					item1=types.InlineKeyboardButton(i[0],callback_data=("streetCode " + i[1]))
					markup.add(item1)

				item1=types.InlineKeyboardButton("назад",callback_data='street -')
				item3=types.InlineKeyboardButton("["+str(database_user[str(call.message.chat.id)]["street_numb"])\
					+"/"+str(int((len(database_user[str(call.message.chat.id)]["cashe"])/7)))+"]",callback_data='chet')
				item2=types.InlineKeyboardButton("далее",callback_data='street +')
				markup.add(item1,item3,item2)
				markup.add(item_start)
				bot.delete_message(str(call.message.chat.id), call.message.id)
				bot.send_message(str(call.message.chat.id),'выберите субъект из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)	
		if call.data == "street +": 
			if int(int((len(database_user[str(call.message.chat.id)]["cashe"])/7))) >= (database_user[str(call.message.chat.id)]["street_numb"] +1): 
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
					+"/"+str(int((len(database_user[str(call.message.chat.id)]["cashe"])/7)))+"]",callback_data='chet')
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
					+"/"+str(int((len(database_user[str(call.message.chat.id)]["cashe"])/7)))+"]",callback_data='chet')
				item2=types.InlineKeyboardButton("далее",callback_data='street +')
				markup.add(item1,item3,item2)
				markup.add(item_start)
				bot.delete_message(str(call.message.chat.id), call.message.id)
				bot.send_message(str(call.message.chat.id),'выберите субъект из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)	






		if call.data == "chet": 
			bot.answer_callback_query(call.id, "я просто счетчик , не тыкай на меня позязя)", show_alert=True)




		


		if call.data.split()[0] == 'streetCode':
			database_user[str(call.message.chat.id)]["street"]  = call.data.split()[1]
			database_user[str(call.message.chat.id)]["cashe"] =  gd.get_home(\
				database_user[str(call.message.chat.id)]["regions"],\
				database_user[str(call.message.chat.id)]["citi"],\
				database_user[str(call.message.chat.id)]["street"],\
				)
			markup=types.InlineKeyboardMarkup()
			a=home_list(database_user[str(call.message.chat.id)]["cashe"],0)
			for i in a:
				item1=types.InlineKeyboardButton(i[0],callback_data=("data " + i[1]))
				markup.add(item1)

			database_user[str(call.message.chat.id)]["home_numb"] = 0

			item1=types.InlineKeyboardButton("назад",callback_data='home -')
			item3=types.InlineKeyboardButton("["+str(database_user[str(call.message.chat.id)]["home_numb"])\
				+"/"+str(int((len(database_user[str(call.message.chat.id)]["cashe"])/7)))+"]",callback_data='chet')
			item2=types.InlineKeyboardButton("далее",callback_data='home +')
			markup.add(item1,item3,item2)
			markup.add(item_start)
			bot.delete_message(str(call.message.chat.id), call.message.id)
			bot.send_message(str(call.message.chat.id),'выберите субъект из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)



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

				database_user[str(call.message.chat.id)]["home_numb"] = int((len(database_user[str(call.message.chat.id)]["cashe"]))/7)
				 
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
		if call.data == "home +": 
			if int(int((len(database_user[str(call.message.chat.id)]["cashe"])/7))) >= (database_user[str(call.message.chat.id)]["home_numb"] +1): 
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
					+"/"+str(int((len(database_user[str(call.message.chat.id)]["cashe"])/7)))+"]",callback_data='chet')
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
					+"/"+str(int((len(database_user[str(call.message.chat.id)]["cashe"])/7)))+"]",callback_data='chet')
				item2=types.InlineKeyboardButton("далее",callback_data='home +')
				markup.add(item1,item3,item2)
				markup.add(item_start)
				bot.delete_message(str(call.message.chat.id), call.message.id)
				bot.send_message(str(call.message.chat.id),'выберите субъект из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)	





		if call.data.split()[0] == 'data':

			database_user[str(call.message.chat.id)]["home"]  = call.data.split()[1]
			text =  gd.get_compuni(\
				database_user[str(call.message.chat.id)]["regions"],\
				database_user[str(call.message.chat.id)]["citi"],\
				database_user[str(call.message.chat.id)]["street"],\
				database_user[str(call.message.chat.id)]["home"],\
				)




			bot.send_message(str(call.message.chat.id),text)	


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
			database_user[int(call.message.chat.id)]= {
				"regions_numb":0,#номер страницы 
				"citi_numb":0
			}
			
			bot.send_message(str(call.message.chat.id),'выберите субъект из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)
				
		if call.data == "chet": 
			bot.answer_callback_query(call.id, "я просто счетчик , не тыкай на меня позязя)", show_alert=True)
	except Exception as e:
		database_user[int(call.message.chat.id)]= {
				"regions_numb":0,#номер страницы 
				"citi_numb":0
			}
		bot.send_message(str(call.message.chat.id),'Сожалею , но случилась ошибка . Чтобы продолжить напишите "начать"')
		print(e)

	with open("database_user.json", "w",encoding='utf-8') as file:
		json.dump(database_user, file, indent=4, ensure_ascii=False)
bot.polling(none_stop=True, interval=0)



#street_list
