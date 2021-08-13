from selenium import webdriver as wb
import time
import requests
import threading
import random

#consts
threads = int(input("Количество потоков: "))
path = '/home/g1fl3x/Рабочий стол/chromedriver'
server = 'https://lolzteam.online/'

proxy_list = []
f = open("proxy.txt","r")
for line in f:
	proxy_list.append(line[:-1])

k = 0
symbols = "zyxwvutsrqponmlkjihgfedcba0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

class Lolzteam:
	def __init__(self,path,server):
		self.path = path
		self.server = server

	def reg(self,password,proxy,symbols):
		try:
			options = wb.ChromeOptions()
			
			#ставим прокси
			options.add_argument('--proxy-server=socks4://' + proxy)
			
			#фейковый user agent
			#ua = UserAgent()
			#userAgent = ua.random
			#options.add_argument(f'user-agent={userAgent}')
			
			#запускаем браузер с мылом
			mail = wb.Chrome(self.path,options=options)
			mail.set_window_size(random.randint(600,1000), random.randint(600,1000))
			mail.get("https://generator.email/")
			
			#запускаем браузер для лолза
			driver = wb.Chrome(self.path,options=options)
			driver.set_page_load_timeout(12)
			driver.set_window_size(1800,1000)
			driver.get(f"{self.server}register/")
			
			#_______________________MAIL GET
			
			time.sleep(2)
			
			#get mail
			source = mail.page_source
			source = source[source.find("<span id=\"email_ch_text\">"):]
			email = source[25:source.find("</span>")]
			
			#получаем логин
			login = email[:email.find("@")]
			login = login.replace(".","").replace("-","")
			new_login = ""
			for i in range(len(login)):
				if random.random() == 0:
					new_login += login[random.randint(0,len(login)-1)]
				else:
					new_login += symbols[random.randint(0,len(symbols)-1)]
			login = new_login
			if len(login)>16:
				login = login[:15]
			
			#_______________________LOLZTEAM REG
			time.sleep(4)
			
			#исходный код
			s = driver.page_source
			
			#вводим данные
			tmp = s[:s.find("placeholder=\"Логин\"")]
			tmp = tmp[tmp.rfind("id=\"")+4:]
			login_id = "#"+tmp[:tmp.find("\"")]
			element = driver.find_element_by_css_selector(login_id)
			element.send_keys(login)
			time.sleep(random.randint(1,2))

			tmp = s[:s.find("placeholder=\"E-mail\"")]
			tmp = tmp[tmp.rfind("id=\"")+4:]
			email_id = "#"+tmp[:tmp.find("\"")]
			element = driver.find_element_by_css_selector(email_id)
			element.send_keys(email)
			time.sleep(random.randint(1,2))

			tmp = s[:s.find("placeholder=\"Пароль\"")]
			tmp = tmp[tmp.rfind("id=\"")+4:]
			pass_id = "#"+tmp[:tmp.find("\"")]
			element = driver.find_element_by_css_selector(pass_id)
			element.send_keys(password)
			time.sleep(random.randint(1,2))
			
			element = driver.find_element_by_css_selector('#ctrl_agree')
			element.click()
			time.sleep(2)
			
			#отправка формы
			element = driver.find_element_by_css_selector('#SubmitButton')
			element.click()
			time.sleep(3)
			driver.get(self.server)
			#_______________________MAIL ACCEPT
			
			#кликаем reflash
			time.sleep(2)
			mail.get(f"https://generator.email/{email}")
			time.sleep(3)
			
			#подтверждение
			a = mail.page_source
			a = a[a.find("https://lolzteam.online/account-confirmation/"):]
			a = a[:a.find("\"")]
			mail.get(a)
			time.sleep(2)
			
			#_______________________GET TOKEN
			
			driver.get(f"{self.server}account/authorize?client_id=sh33djax08y8wa1u&client_secret=w417z4xghfmfqweu&response_type=token&scope=read+post")
			driver.find_element_by_xpath('//input[@class="button primary"]').click()
			time.sleep(0.5)
			uri = driver.current_url
			token = uri[uri.find("access_token=")+13:uri.find("&")]
			
			# Запись в файл
			mes = "\n"+login+":"+password+":"+email+":"+token
			f=open("users.txt","a")
			f.write(mes)
			f.close()
			driver.close()
			mail.close()
			print(login)
		except:
			driver.close()
			mail.close()
			
		#___________________PODPISKA
		"""
		driver.get(f"{self.server}g1fl3x/")
		time.sleep(1)
		element = driver.find_element_by_xpath('//a[@class="FollowLink_Advanced followButton button block"]')
		element.click()
		time.sleep(1)
		"""


######################__CODE__####################
lolz = Lolzteam(path,server)
def reg_start(lolz,symbols):
	global k,proxy_list
	while True:
		try:
			proxy = proxy_list[k]
		except:
			k = 0
			proxy = proxy_list[k]
		k + =1
		#генерим пароль
		tmp_password = ""
		for i in range(random.randint(8,14)):
			tmp_password += symbols[random.randint(0,len(symbols)-1)]
		#регаем
		try:
			lolz.reg(tmp_password,proxy,symbols)
		except:pass
		i += random.randint(1,4)

#запускаем потоки
for i in range(threads):
	threading.Thread(target=reg_start, args=(lolz,symbols)).start()
	time.sleep(random.randint(3,8))
