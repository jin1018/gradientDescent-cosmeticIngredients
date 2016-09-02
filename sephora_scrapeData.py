"""
Web Scraper
collect information of cosmetic products(name, size, price, rating, list of ingredients)
save data in a txt file(sephora_data_foundation.txt)
"""

import requests
import re
import string
#from bs4 import BeautifulSoup

f = open("sephora_data_foundation", 'w')

for pageNum in range(1,5):
	print("pageNum: " + str(pageNum))
	req = "http://www.sephora.com/foundation-makeup?currentPage="+str(pageNum)
	response = requests.get(req).text

	#go to link for each product
	productURL = re.findall('"product_url":"(.*?)","',response)
	for i in productURL:
		#print(i)
		product_req = "http://www.sephora.com"+i
		product_response = requests.get(product_req).text

		#Get Name of Product
		name= re.findall('"productName":"(.*?)"',product_response)
		if name:
			product_name=name[0]
			#print(product_name)
			f.write(product_name.encode('utf8'))
		else:
			f.write("")
		f.write("|")


		#Get Size of Product
		size= re.findall('"sku_size":"(.*?)"',product_response)
		if size:
			product_size=size[0]#in ounces
			product_size=product_size.replace(" oz", "")
			#print(product_size)
			f.write(product_size)
		else:
			f.write("")
		f.write("|")

		#Get Price of Product
		price= re.findall('"list_price":(.*?),',product_response)
		if price:
			product_price=price[0]#US Dollars
			#print(product_price)
			f.write(product_price)
		else:
			f.write("")
		f.write("|")

		#Get Rating of Product
		rating= re.findall('"rating":(.*?),',product_response)
		if rating:
			product_rating=rating[0]
			#print(product_rating)
			f.write(product_rating)
		else:
			f.write("")
		f.write("|")

		#Get Ingredients
		ingredients_list = re.findall('"ingredients":(.*?)","shipping_info":"',product_response)
		if ingredients_list:
			ing_string=ingredients_list[0]#string(ingredient section)
			if "May" in ing_string:
				ing_string = re.findall('(.*?)May',ing_string)[0]#Remove "May Contain...". Delete after period(.)
			#print ("ing_string")#string- ingredient section
			#print (ing_string)

			del_comments = re.findall('-(.*?)<br>',ing_string)#list of strings that need to be deleted

			for i in del_comments:#delete all of them here
				ing_string=ing_string.replace(i,'')

			#remove ", -, <br>, . , strip white space
			ing_string=ing_string.strip()#strip white spaces
			ing_string=ing_string.replace("<br>",'')
			ing_string=ing_string.replace("-",'')
			ing_string=ing_string.replace("\\r",'')
			ing_string=ing_string.replace("\\n",'')
			ing_string=ing_string.replace('"','')
			ing_string=ing_string.replace('.','')
			ing_string=ing_string.lower()

			ing_list=ing_string.split(", ")
			for i in ing_list:
				i = i.strip()
			#print(ing_list)
			f.write("[")
			for j in ing_list:
				f.write(j)
				f.write(",")
			f.write("]")
		else:
			f.write("")


		f.write("\n")
f.close

