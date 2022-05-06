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
