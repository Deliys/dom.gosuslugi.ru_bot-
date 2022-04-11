import requests
import json
import telebot
from telebot import types
import math

import pypo.getdata as gd #импорт функция из файла getdata в pypo 
bot = telebot.TeleBot('5225585818:AAGSLsqeM02iZ5JwvEuocZmK9X4P2vlP6eE')



database_user = {
	308815740:{
		"regions_numb":0,#номер страницы 
		"citi_numb":0
	}


}


with open('regions.json', 'r',encoding='utf-8') as fp:
	regions = json.load(fp)

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

	print(numb)

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

	print(numb)


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
	bot.send_message(m.chat.id, 'Я на связи. Напиши мне что-нибудь )')
# Получение сообщений от юзера


#----------------

@bot.message_handler(content_types=["text"])

def handle_text(message):
	if message.text == "начать":
		markup=types.InlineKeyboardMarkup()


		a=regions_list(regions,0)

		for i in a:
			item1=types.InlineKeyboardButton(i[0],callback_data=("regionCode " + i[1]))
			markup.add(item1)

		item1=types.InlineKeyboardButton("-",callback_data='regions -')
		item3=types.InlineKeyboardButton("[0/"+str(int((len(regions)/8)))+"]",callback_data='chet')
		item2=types.InlineKeyboardButton("+",callback_data='regions +')

		markup.add(item1,item3,item2)
		
		bot.send_message(message.chat.id,'выберите субъект из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)




	else:
		bot.send_message(message.chat.id, 'Вы написали: ' + message.text)
# Запускаем бота


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
	if call.data == "regions -": 
		if 0<= (database_user[call.message.chat.id]["regions_numb"] -1): 
			# эта страшная черуха сравнивает колво страниц с номером на которой ты уже находишь +1 
			# если листов больше ,то перебросит на следущий , если листов меньше , то кинет на лист первый(0)
			database_user[call.message.chat.id]["regions_numb"] = database_user[call.message.chat.id]["regions_numb"] -1
			 
			markup=types.InlineKeyboardMarkup()
			a=regions_list(regions,database_user[call.message.chat.id]["regions_numb"])
			for i in a:
				item1=types.InlineKeyboardButton(i[0],callback_data=("regionCode " + i[1]))
				markup.add(item1)

			item1=types.InlineKeyboardButton("-",callback_data='regions -')
			item3=types.InlineKeyboardButton("["+str(database_user[call.message.chat.id]["regions_numb"])\
				+"/"+str(int((len(regions)/8)))+"]",callback_data='chet')
			item2=types.InlineKeyboardButton("+",callback_data='regions +')

			markup.add(item1,item3,item2)
			


			bot.delete_message(call.message.chat.id, call.message.id)
			bot.send_message(call.message.chat.id,'выберите субъект из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)

			
		else:

			database_user[call.message.chat.id]["regions_numb"] = int((len(regions)/8))
			 
			markup=types.InlineKeyboardMarkup()
			a=regions_list(regions,database_user[call.message.chat.id]["regions_numb"])
			for i in a:
				item1=types.InlineKeyboardButton(i[0],callback_data=("regionCode " + i[1]))
				markup.add(item1)

			item1=types.InlineKeyboardButton("-",callback_data='regions -')
			item3=types.InlineKeyboardButton("["+str(database_user[call.message.chat.id]["regions_numb"])\
				+"/"+str(int((len(regions)/8)))+"]",callback_data='chet')
			item2=types.InlineKeyboardButton("+",callback_data='regions +')
			markup.add(item1,item3,item2)
			bot.delete_message(call.message.chat.id, call.message.id)
			bot.send_message(call.message.chat.id,'выберите субъект из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)	
	if call.data == "regions +": 
		if int(int((len(regions)/8))) >= (database_user[call.message.chat.id]["regions_numb"] +1): 
			# эта страшная черуха сравнивает колво страниц с номером на которой ты уже находишь +1 
			# если листов больше ,то перебросит на следущий , если листов меньше , то кинет на лист первый(0)
			database_user[call.message.chat.id]["regions_numb"] = database_user[call.message.chat.id]["regions_numb"] +1
			 
			markup=types.InlineKeyboardMarkup()
			a=regions_list(regions,database_user[call.message.chat.id]["regions_numb"])
			for i in a:
				item1=types.InlineKeyboardButton(i[0],callback_data=("regionCode " + i[1]))
				markup.add(item1)

			item1=types.InlineKeyboardButton("-",callback_data='regions -')
			item3=types.InlineKeyboardButton("["+str(database_user[call.message.chat.id]["regions_numb"])\
				+"/"+str(int((len(regions)/8)))+"]",callback_data='chet')
			item2=types.InlineKeyboardButton("+",callback_data='regions +')

			markup.add(item1,item3,item2)
			


			bot.delete_message(call.message.chat.id, call.message.id)
			bot.send_message(call.message.chat.id,'выберите субъект из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)

			
		else:

			database_user[call.message.chat.id]["regions_numb"] = 0
			 
			markup=types.InlineKeyboardMarkup()
			a=regions_list(regions,database_user[call.message.chat.id]["regions_numb"])
			for i in a:
				item1=types.InlineKeyboardButton(i[0],callback_data=("regionCode " + i[1]))
				markup.add(item1)

			item1=types.InlineKeyboardButton("-",callback_data='regions -')
			item3=types.InlineKeyboardButton("["+str(database_user[call.message.chat.id]["regions_numb"])\
				+"/"+str(int((len(regions)/8)))+"]",callback_data='chet')
			item2=types.InlineKeyboardButton("+",callback_data='regions +')
			markup.add(item1,item3,item2)
			bot.delete_message(call.message.chat.id, call.message.id)
			bot.send_message(call.message.chat.id,'выберите субъект из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)		

	#район или город-------------------------------------------


	if call.data.split()[0] == "regionCode":
		database_user[call.message.chat.id]["regions"]  = call.data.split()[1]
		markup=types.InlineKeyboardMarkup()
		item1=types.InlineKeyboardButton("Город",callback_data='citi')
		item2=types.InlineKeyboardButton("Район",callback_data='area')
		markup.add(item1,item2)

		bot.delete_message(call.message.chat.id, call.message.id)
		bot.send_message(call.message.chat.id,'выберите Город или Район',reply_markup=markup)	
		
	

	#город-------------------------------------------


	if call.data== "citi":
		database_user[call.message.chat.id]["cashe"] =  gd.get_citis(database_user[call.message.chat.id]["regions"])
		database_user[call.message.chat.id]["citi_numb"] = 0
		markup=types.InlineKeyboardMarkup()


		a=citi_list(database_user[call.message.chat.id]["cashe"],0)
		for i in a:
			item1=types.InlineKeyboardButton(i[0],callback_data=("citiCode " + i[1]))
			markup.add(item1)



		item1=types.InlineKeyboardButton("-",callback_data='citi -')
		item3=types.InlineKeyboardButton("["+str(database_user[call.message.chat.id]["citi_numb"])\
			+"/"+str(int((len(database_user[call.message.chat.id]["cashe"])/4)))+"]",callback_data='chet')
		item2=types.InlineKeyboardButton("+",callback_data='citi +')
		markup.add(item1,item3,item2)
		bot.delete_message(call.message.chat.id, call.message.id)
		bot.send_message(call.message.chat.id,'выберите Город из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)
		





	if call.data == "citi +": 
		if int(int((len(database_user[call.message.chat.id]["cashe"])/4))) > (database_user[call.message.chat.id]["citi_numb"] +1): 
			# эта страшная черуха сравнивает колво страниц с номером на которой ты уже находишь +1 
			# если листов больше ,то перебросит на следущий , если листов меньше , то кинет на лист первый(0)
			database_user[call.message.chat.id]["citi_numb"] = database_user[call.message.chat.id]["citi_numb"] +1
			 
			markup=types.InlineKeyboardMarkup()
			a=regions_list(database_user[call.message.chat.id]["cashe"],database_user[call.message.chat.id]["citi_numb"])
			for i in a:
				item1=types.InlineKeyboardButton(i[0],callback_data=("citiCode " + i[1]))
				markup.add(item1)

			item1=types.InlineKeyboardButton("-",callback_data='citi -')
			item3=types.InlineKeyboardButton("["+str(database_user[call.message.chat.id]["citi_numb"])\
				+"/"+str(int((len(database_user[call.message.chat.id]["cashe"])/4)))+"]",callback_data='chet')
			item2=types.InlineKeyboardButton("+",callback_data='citi +')

			markup.add(item1,item3,item2)
			


			bot.delete_message(call.message.chat.id, call.message.id)
			bot.send_message(call.message.chat.id,'выберите Город из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)

		else:
			
			database_user[call.message.chat.id]["citi_numb"] = 0
			markup=types.InlineKeyboardMarkup()


			a=citi_list(database_user[call.message.chat.id]["cashe"],0)
			for i in a:
				item1=types.InlineKeyboardButton(i[0],callback_data=("citiCode " + i[1]))
				markup.add(item1)



			item1=types.InlineKeyboardButton("-",callback_data='citi -')
			item3=types.InlineKeyboardButton("["+str(database_user[call.message.chat.id]["citi_numb"])\
				+"/"+str(int((len(database_user[call.message.chat.id]["cashe"])/4)))+"]",callback_data='chet')
			item2=types.InlineKeyboardButton("+",callback_data='citi +')
			markup.add(item1,item3,item2)
			bot.delete_message(call.message.chat.id, call.message.id)
			bot.send_message(call.message.chat.id,'выберите Город из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)

			


	if call.data == "citi -": 
		if 0<= (database_user[call.message.chat.id]["citi_numb"] -1): 
			# эта страшная черуха сравнивает колво страниц с номером на которой ты уже находишь +1 
			# если листов больше ,то перебросит на следущий , если листов меньше , то кинет на лист первый(0)
			database_user[call.message.chat.id]["citi_numb"] = database_user[call.message.chat.id]["citi_numb"] -1
			 
			markup=types.InlineKeyboardMarkup()
			a=regions_list(database_user[call.message.chat.id]["cashe"],database_user[call.message.chat.id]["citi_numb"])
			for i in a:
				item1=types.InlineKeyboardButton(i[0],callback_data=("citiCode " + i[1]))
				markup.add(item1)

			item1=types.InlineKeyboardButton("-",callback_data='citi -')
			item3=types.InlineKeyboardButton("["+str(database_user[call.message.chat.id]["citi_numb"])\
				+"/"+str(int((len(database_user[call.message.chat.id]["cashe"])/4)))+"]",callback_data='chet')
			item2=types.InlineKeyboardButton("+",callback_data='citi +')

			markup.add(item1,item3,item2)
			


			bot.delete_message(call.message.chat.id, call.message.id)
			bot.send_message(call.message.chat.id,'выберите Город из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)



		else:

			
			database_user[call.message.chat.id]["citi_numb"] = int((len(database_user[call.message.chat.id]["cashe"])/4))
			markup=types.InlineKeyboardMarkup()


			a=citi_list(database_user[call.message.chat.id]["cashe"],int((len(database_user[call.message.chat.id]["cashe"])/4)))
			for i in a:
				item1=types.InlineKeyboardButton(i[0],callback_data=("citiCode " + i[1]))
				markup.add(item1)



			item1=types.InlineKeyboardButton("-",callback_data='citi -')
			item3=types.InlineKeyboardButton("["+str(database_user[call.message.chat.id]["citi_numb"])\
				+"/"+str(int((len(database_user[call.message.chat.id]["cashe"])/4)))+"]",callback_data='chet')
			item2=types.InlineKeyboardButton("+",callback_data='citi +')
			markup.add(item1,item3,item2)
			bot.delete_message(call.message.chat.id, call.message.id)
			bot.send_message(call.message.chat.id,'выберите Город из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)

			
	#улицы-------------------------------------------

	if call.data.split()[0] == 'citiCode':
		database_user[call.message.chat.id]["citi"]  = call.data.split()[1]
		database_user[call.message.chat.id]["cashe"] =  gd.get_streat(\
			database_user[call.message.chat.id]["regions"],\
			database_user[call.message.chat.id]["citi"]
			)
		markup=types.InlineKeyboardMarkup()
		a=street_list(database_user[call.message.chat.id]["cashe"],0)
		for i in a:
			item1=types.InlineKeyboardButton(i[0],callback_data=("streetCode " + i[1]))
			markup.add(item1)

		database_user[call.message.chat.id]["street_numb"] = 0

		item1=types.InlineKeyboardButton("-",callback_data='street -')
		item3=types.InlineKeyboardButton("["+str(database_user[call.message.chat.id]["street_numb"])\
			+"/"+str(int((len(database_user[call.message.chat.id]["cashe"])/7)))+"]",callback_data='chet')
		item2=types.InlineKeyboardButton("+",callback_data='street +')
		markup.add(item1,item3,item2)
		bot.delete_message(call.message.chat.id, call.message.id)
		bot.send_message(call.message.chat.id,'выберите улицу из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)
			







	if call.data == "street -": 
		if 0<= (database_user[call.message.chat.id]["street_numb"] -1): 
			# эта страшная черуха сравнивает колво страниц с номером на которой ты уже находишь +1 
			# если листов больше ,то перебросит на следущий , если листов меньше , то кинет на лист первый(0)
			database_user[call.message.chat.id]["street_numb"] = database_user[call.message.chat.id]["street_numb"] -1
			 
			markup=types.InlineKeyboardMarkup()
			a=street_list(database_user[call.message.chat.id]["cashe"],database_user[call.message.chat.id]["street_numb"])
			for i in a:
				item1=types.InlineKeyboardButton(i[0],callback_data=("streetCode " + i[1]))
				markup.add(item1)

			item1=types.InlineKeyboardButton("-",callback_data='street -')
			item3=types.InlineKeyboardButton("["+str(database_user[call.message.chat.id]["street_numb"])\
				+"/"+str(int((len(database_user[call.message.chat.id]["cashe"])/7)))+"]",callback_data='chet')
			item2=types.InlineKeyboardButton("+",callback_data='street +')

			markup.add(item1,item3,item2)
			


			bot.delete_message(call.message.chat.id, call.message.id)
			bot.send_message(call.message.chat.id,'выберите субъект из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)

			
		else:

			database_user[call.message.chat.id]["street_numb"] = int((len(database_user[call.message.chat.id]["cashe"]))/7)
			 
			markup=types.InlineKeyboardMarkup()
			a=street_list(database_user[call.message.chat.id]["cashe"],database_user[call.message.chat.id]["street_numb"])
			for i in a:
				item1=types.InlineKeyboardButton(i[0],callback_data=("streetCode " + i[1]))
				markup.add(item1)

			item1=types.InlineKeyboardButton("-",callback_data='street -')
			item3=types.InlineKeyboardButton("["+str(database_user[call.message.chat.id]["street_numb"])\
				+"/"+str(int((len(database_user[call.message.chat.id]["cashe"])/7)))+"]",callback_data='chet')
			item2=types.InlineKeyboardButton("+",callback_data='street +')
			markup.add(item1,item3,item2)
			bot.delete_message(call.message.chat.id, call.message.id)
			bot.send_message(call.message.chat.id,'выберите субъект из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)	
	if call.data == "street +": 
		if int(int((len(database_user[call.message.chat.id]["cashe"])/7))) >= (database_user[call.message.chat.id]["street_numb"] +1): 
			# эта страшная черуха сравнивает колво страниц с номером на которой ты уже находишь +1 
			# если листов больше ,то перебросит на следущий , если листов меньше , то кинет на лист первый(0)
			database_user[call.message.chat.id]["street_numb"] = database_user[call.message.chat.id]["street_numb"] +1
			 
			markup=types.InlineKeyboardMarkup()
			a=street_list(database_user[call.message.chat.id]["cashe"],database_user[call.message.chat.id]["street_numb"])
			for i in a:
				item1=types.InlineKeyboardButton(i[0],callback_data=("streetCode " + i[1]))
				markup.add(item1)

			item1=types.InlineKeyboardButton("-",callback_data='street -')
			item3=types.InlineKeyboardButton("["+str(database_user[call.message.chat.id]["street_numb"])\
				+"/"+str(int((len(database_user[call.message.chat.id]["cashe"])/7)))+"]",callback_data='chet')
			item2=types.InlineKeyboardButton("+",callback_data='street +')

			markup.add(item1,item3,item2)
			


			bot.delete_message(call.message.chat.id, call.message.id)
			bot.send_message(call.message.chat.id,'выберите субъект из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)

			
		else:

			database_user[call.message.chat.id]["street_numb"] = 0
			 
			markup=types.InlineKeyboardMarkup()
			a=street_list(database_user[call.message.chat.id]["cashe"],database_user[call.message.chat.id]["street_numb"])
			for i in a:
				item1=types.InlineKeyboardButton(i[0],callback_data=("streetCode " + i[1]))
				markup.add(item1)

			item1=types.InlineKeyboardButton("-",callback_data='street -')
			item3=types.InlineKeyboardButton("["+str(database_user[call.message.chat.id]["street_numb"])\
				+"/"+str(int((len(database_user[call.message.chat.id]["cashe"])/7)))+"]",callback_data='chet')
			item2=types.InlineKeyboardButton("+",callback_data='street +')
			markup.add(item1,item3,item2)
			bot.delete_message(call.message.chat.id, call.message.id)
			bot.send_message(call.message.chat.id,'выберите субъект из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)	






	if call.data == "chet": 
		bot.answer_callback_query(call.id, "я просто счетчик , не тыкай на меня позязя)", show_alert=True)




	#не раб 


	if call.data.split()[0] == 'streetCode':
		database_user[call.message.chat.id]["street"]  = call.data.split()[1]
		database_user[call.message.chat.id]["cashe"] =  gd.get_home(\
			database_user[call.message.chat.id]["regions"],\
			database_user[call.message.chat.id]["citi"],\
			database_user[call.message.chat.id]["street"],\
			)
		markup=types.InlineKeyboardMarkup()
		a=home_list(database_user[call.message.chat.id]["cashe"],0)
		for i in a:
			item1=types.InlineKeyboardButton(i[0],callback_data=("data " + i[1]))
			markup.add(item1)

		database_user[call.message.chat.id]["home_numb"] = 0

		item1=types.InlineKeyboardButton("-",callback_data='home -')
		item3=types.InlineKeyboardButton("["+str(database_user[call.message.chat.id]["home_numb"])\
			+"/"+str(int((len(database_user[call.message.chat.id]["cashe"])/7)))+"]",callback_data='chet')
		item2=types.InlineKeyboardButton("+",callback_data='home +')
		markup.add(item1,item3,item2)
		bot.delete_message(call.message.chat.id, call.message.id)
		bot.send_message(call.message.chat.id,'выберите субъект из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)



	if call.data == "home -": 
		if 0<= (database_user[call.message.chat.id]["home_numb"] -1): 
			# эта страшная черуха сравнивает колво страниц с номером на которой ты уже находишь +1 
			# если листов больше ,то перебросит на следущий , если листов меньше , то кинет на лист первый(0)
			database_user[call.message.chat.id]["home_numb"] = database_user[call.message.chat.id]["home_numb"] -1
			 
			markup=types.InlineKeyboardMarkup()
			a=home_list(database_user[call.message.chat.id]["cashe"],database_user[call.message.chat.id]["home_numb"])
			for i in a:
				item1=types.InlineKeyboardButton(i[0],callback_data=("data " + i[1]))
				markup.add(item1)

			item1=types.InlineKeyboardButton("-",callback_data='home -')
			item3=types.InlineKeyboardButton("["+str(database_user[call.message.chat.id]["home_numb"])\
				+"/"+str(int((len(database_user[call.message.chat.id]["cashe"])/7)))+"]",callback_data='chet')
			item2=types.InlineKeyboardButton("+",callback_data='home +')

			markup.add(item1,item3,item2)
			


			bot.delete_message(call.message.chat.id, call.message.id)
			bot.send_message(call.message.chat.id,'выберите субъект из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)

			
		else:

			database_user[call.message.chat.id]["home_numb"] = int((len(database_user[call.message.chat.id]["cashe"]))/7)
			 
			markup=types.InlineKeyboardMarkup()
			a=home_list(database_user[call.message.chat.id]["cashe"],database_user[call.message.chat.id]["home_numb"])
			for i in a:
				item1=types.InlineKeyboardButton(i[0],callback_data=("data " + i[1]))
				markup.add(item1)

			item1=types.InlineKeyboardButton("-",callback_data='home -')
			item3=types.InlineKeyboardButton("["+str(database_user[call.message.chat.id]["home_numb"])\
				+"/"+str(int((len(database_user[call.message.chat.id]["cashe"])/7)))+"]",callback_data='chet')
			item2=types.InlineKeyboardButton("+",callback_data='home +')
			markup.add(item1,item3,item2)
			bot.delete_message(call.message.chat.id, call.message.id)
			bot.send_message(call.message.chat.id,'выберите субъект из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)	
	if call.data == "home +": 
		if int(int((len(database_user[call.message.chat.id]["cashe"])/7))) >= (database_user[call.message.chat.id]["home_numb"] +1): 
			# эта страшная черуха сравнивает колво страниц с номером на которой ты уже находишь +1 
			# если листов больше ,то перебросит на следущий , если листов меньше , то кинет на лист первый(0)
			database_user[call.message.chat.id]["home_numb"] = database_user[call.message.chat.id]["home_numb"] +1
			 
			markup=types.InlineKeyboardMarkup()
			a=home_list(database_user[call.message.chat.id]["cashe"],database_user[call.message.chat.id]["home_numb"])
			for i in a:
				item1=types.InlineKeyboardButton(i[0],callback_data=("data " + i[1]))
				markup.add(item1)

			item1=types.InlineKeyboardButton("-",callback_data='home -')
			item3=types.InlineKeyboardButton("["+str(database_user[call.message.chat.id]["home_numb"])\
				+"/"+str(int((len(database_user[call.message.chat.id]["cashe"])/7)))+"]",callback_data='chet')
			item2=types.InlineKeyboardButton("+",callback_data='home +')

			markup.add(item1,item3,item2)
			


			bot.delete_message(call.message.chat.id, call.message.id)
			bot.send_message(call.message.chat.id,'выберите субъект из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)

			
		else:

			database_user[call.message.chat.id]["home_numb"] = 0
			 
			markup=types.InlineKeyboardMarkup()
			a=home_list(database_user[call.message.chat.id]["cashe"],database_user[call.message.chat.id]["home_numb"])
			for i in a:
				item1=types.InlineKeyboardButton(i[0],callback_data=("data " + i[1]))
				markup.add(item1)

			item1=types.InlineKeyboardButton("-",callback_data='home -')
			item3=types.InlineKeyboardButton("["+str(database_user[call.message.chat.id]["home_numb"])\
				+"/"+str(int((len(database_user[call.message.chat.id]["cashe"])/7)))+"]",callback_data='chet')
			item2=types.InlineKeyboardButton("+",callback_data='home +')
			markup.add(item1,item3,item2)
			bot.delete_message(call.message.chat.id, call.message.id)
			bot.send_message(call.message.chat.id,'выберите субъект из списка с помощью кнопок или напиши самостоятельно',reply_markup=markup)	





	if call.data.split()[0] == 'data':

		database_user[call.message.chat.id]["home"]  = call.data.split()[1]
		text =  gd.get_compuni(\
			database_user[call.message.chat.id]["regions"],\
			database_user[call.message.chat.id]["citi"],\
			database_user[call.message.chat.id]["street"],\
			database_user[call.message.chat.id]["home"],\
			)




		bot.send_message(call.message.chat.id,text)	



			
	if call.data == "chet": 
		bot.answer_callback_query(call.id, "я просто счетчик , не тыкай на меня позязя)", show_alert=True)
bot.polling(none_stop=True, interval=0)



#street_list
