import json
from telebot import types
from pypo.data_list import regions_list, vilage_list , citi_list, area_list ,street_list ,home_list
from pypo.text import area_next_text ,citi_next_text , vilage_next_text
import pypo.getdata as gd #импорт функция из файла getdata в pypo
import pypo.change_write as cw 
from pypo.change_write import item_start
from pypo.change_write import button_gen


def regions_next(bot, call ,database_user ,regions):

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


def area_next(bot, call ,database_user ):
	
	if call.data== "area":
		database_user[str(call.message.chat.id)]["cashe"] =  gd.get_area(database_user[str(call.message.chat.id)]["regions"])
		database_user[str(call.message.chat.id)]["area_numb"] = 0
		a=area_list(database_user[str(call.message.chat.id)]["cashe"],0)
		button_gen(database_user,bot , call , area_next_text ,a , "area" , "area")
	if call.data == "area +": 
		if int(int((len(database_user[str(call.message.chat.id)]["cashe"])/4))) > (database_user[str(call.message.chat.id)]["area_numb"] +1): 
			# эта страшная черуха сравнивает колво страниц с номером на которой ты уже находишь +1 
			# если листов больше ,то перебросит на следущий , если листов меньше , то кинет на лист первый(0)
			database_user[str(call.message.chat.id)]["area_numb"] = database_user[str(call.message.chat.id)]["area_numb"] +1
			a=area_list(database_user[str(call.message.chat.id)]["cashe"],database_user[str(call.message.chat.id)]["area_numb"])
			button_gen(database_user,bot , call , area_next_text ,a , "area" , "area")
		else:
			database_user[str(call.message.chat.id)]["area_numb"] = 0
			markup=types.InlineKeyboardMarkup()
			a=area_list(database_user[str(call.message.chat.id)]["cashe"],0)
			button_gen(database_user,bot , call , area_next_text ,a , "area" , "area")
	if call.data == "area -": 
		if 0<= (database_user[str(call.message.chat.id)]["area_numb"] -1): 
			# эта страшная черуха сравнивает колво страниц с номером на которой ты уже находишь +1 
			# если листов больше ,то перебросит на следущий , если листов меньше , то кинет на лист первый(0)
			database_user[str(call.message.chat.id)]["area_numb"] = database_user[str(call.message.chat.id)]["area_numb"] -1			 
			markup=types.InlineKeyboardMarkup()
			a=area_list(database_user[str(call.message.chat.id)]["cashe"],database_user[str(call.message.chat.id)]["area_numb"])
			button_gen(database_user,bot , call , area_next_text ,a , "area" , "area")
		else:
			database_user[str(call.message.chat.id)]["area_numb"] = int((len(database_user[str(call.message.chat.id)]["cashe"])/4))
			markup=types.InlineKeyboardMarkup()
			a=area_list(database_user[str(call.message.chat.id)]["cashe"],int((len(database_user[str(call.message.chat.id)]["cashe"])/4)))
			button_gen(database_user,bot , call , area_next_text ,a , "area" , "area")

def vilage_next(bot, call ,database_user ):
	if call.data== "vilage":
		database_user[str(call.message.chat.id)]["cashe"] =  gd.get_vilages(database_user[str(call.message.chat.id)]["regions"])
		database_user[str(call.message.chat.id)]["vilage_numb"] = 0

		a=area_list(database_user[str(call.message.chat.id)]["cashe"],0)
		button_gen(database_user,bot , call , vilage_next_text ,a , "vilage" , "vilage")

	if call.data == "vilage +": 
		if int(int((len(database_user[str(call.message.chat.id)]["cashe"])/4))) > (database_user[str(call.message.chat.id)]["vilage_numb"] +1): 
			# эта страшная черуха сравнивает колво страниц с номером на которой ты уже находишь +1 
			# если листов больше ,то перебросит на следущий , если листов меньше , то кинет на лист первый(0)
			database_user[str(call.message.chat.id)]["vilage_numb"] = database_user[str(call.message.chat.id)]["vilage_numb"] +1
			 
			a=area_list(database_user[str(call.message.chat.id)]["cashe"],0)
			button_gen(database_user,bot , call , vilage_next_text ,a , "vilage" , "vilage")

		else:
			
			database_user[str(call.message.chat.id)]["vilage_numb"] = 0
			a=area_list(database_user[str(call.message.chat.id)]["cashe"],0)
			button_gen(database_user,bot , call , vilage_next_text ,a , "vilage" , "vilage")
	if call.data == "vilage -": 
		if 0<= (database_user[str(call.message.chat.id)]["vilage_numb"] -1): 
			# эта страшная черуха сравнивает колво страниц с номером на которой ты уже находишь +1 
			# если листов больше ,то перебросит на следущий , если листов меньше , то кинет на лист первый(0)
			database_user[str(call.message.chat.id)]["vilage_numb"] = database_user[str(call.message.chat.id)]["vilage_numb"] -1
			 
			a=area_list(database_user[str(call.message.chat.id)]["cashe"],0)
			button_gen(database_user,bot , call , vilage_next_text ,a , "vilage" , "vilage")
		else:
			database_user[str(call.message.chat.id)]["vilage_numb"] = int((len(database_user[str(call.message.chat.id)]["cashe"])/4))
			a=area_list(database_user[str(call.message.chat.id)]["cashe"],0)
			button_gen(database_user,bot , call , vilage_next_text ,a , "vilage" , "vilage")


def citi_next(bot, call ,database_user ):
	if call.data== "citi":
		database_user[str(call.message.chat.id)]["cashe"] =  gd.get_citis(database_user[str(call.message.chat.id)]["regions"])
		database_user[str(call.message.chat.id)]["citi_numb"] = 0
		a=area_list(database_user[str(call.message.chat.id)]["cashe"],0)
		button_gen(database_user,bot , call , citi_next_text ,a , "citi" , "citi")
	if call.data == "citi +": 
		if int(int((len(database_user[str(call.message.chat.id)]["cashe"])/4))) > (database_user[str(call.message.chat.id)]["citi_numb"] +1): 
			# эта страшная черуха сравнивает колво страниц с номером на которой ты уже находишь +1 
			# если листов больше ,то перебросит на следущий , если листов меньше , то кинет на лист первый(0)
			database_user[str(call.message.chat.id)]["citi_numb"] = database_user[str(call.message.chat.id)]["citi_numb"] +1
			a=area_list(database_user[str(call.message.chat.id)]["cashe"],database_user[str(call.message.chat.id)]["citi_numb"])
			button_gen(database_user,bot , call , citi_next_text ,a , "citi" , "citi")
		else:
			database_user[str(call.message.chat.id)]["citi_numb"] = 0
			a=area_list(database_user[str(call.message.chat.id)]["cashe"],0)
			button_gen(database_user,bot , call , citi_next_text ,a , "citi" , "citi")

	if call.data == "citi -": 
		if 0<= (database_user[str(call.message.chat.id)]["citi_numb"] -1): 
			# эта страшная черуха сравнивает колво страниц с номером на которой ты уже находишь +1 
			# если листов больше ,то перебросит на следущий , если листов меньше , то кинет на лист первый(0)
			database_user[str(call.message.chat.id)]["citi_numb"] = database_user[str(call.message.chat.id)]["citi_numb"] -1
			a=area_list(database_user[str(call.message.chat.id)]["cashe"],database_user[str(call.message.chat.id)]["citi_numb"])
			button_gen(database_user,bot , call , citi_next_text ,a , "citi" , "citi")
		else:
			database_user[str(call.message.chat.id)]["citi_numb"] = int((len(database_user[str(call.message.chat.id)]["cashe"])/4))
			a=area_list(database_user[str(call.message.chat.id)]["cashe"],int((len(database_user[str(call.message.chat.id)]["cashe"])/4)))
			button_gen(database_user,bot , call , citi_next_text ,a , "citi" , "citi")
