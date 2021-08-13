from selenium import webdriver as wb
import time
import requests
import threading
import random
import json
from fake_useragent import UserAgent

#consts
threads = int(input("Количество потоков: "))
path = '/home/g1fl3x/Рабочий стол/chromedriver'
server = 'https://lolzteam.online/'

proxy_list = []
f = open("proxy.txt","r")
for line in f:
	proxy_list.append(line[:-1])
k=0


class User:
	def login_by_mail(self,mail):
		symbols = "zyxwvutsrqponmlkjihgfedcba0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
		
		login = mail[:mail.find("@")]
		login = login.replace(".","").replace("-","")
		new_login = ""
		for i in range(len(login)):
			if random.random() == 0:
				new_login += login[random.randint(0,len(login)-1)]
			else:
				new_login += symbols[random.randint(0,len(symbols)-1)]
		
		if len(login)>=16:
			new_login = new_login[:16]
		
		return new_login
		
	def get_password(self):
		symbols = "zyxwvutsrqponmlkjihgfedcba0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
		
		tmp_password = ""
		for i in range(random.randint(8,14)):
			tmp_password += symbols[random.randint(0,len(symbols)-1)]
		return tmp_password
	
class Mail:
	def __init__(self):
		self.session = requests.session()
		self.session.get("https://10minutemail.com/")
	def get_mail(self):
		mail = json.loads(self.session.get("https://10minutemail.com/session/address").text)["address"]
		return mail
		
	def count_messages(self):
		count = json.loads(self.session.get("https://10minutemail.com/messages/messageCount").text)["messageCount"]
		return str(count)
		
	def get_message(self,message_id):
		data = json.loads(self.session.get(f"https://10minutemail.com/messages/messagesAfter/{message_id}").text)[0]
		return data["bodyPlainText"]

class Lolzteam:
	def __init__(self,path,server):
		self.path = path
		self.server = server

	def reg(self,login,email,password,proxy,mail):
		try:
			options = wb.ChromeOptions()
			
			#ставим прокси
			options.add_argument('--proxy-server=socks4://' + proxy)
			
			#фейковый user agent
			ua = UserAgent()
			userAgent = ua.random
			options.add_argument(f'user-agent={userAgent}')
			
			#запускаем браузер для лолза
			driver = wb.Chrome(self.path,options=options)
			driver.set_page_load_timeout(12)
			driver.set_window_size(1900,1000)
			driver.get(f"{self.server}register/")
			
			#_______________________LOLZTEAM REG
			time.sleep(5)
			
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
			time.sleep(random.randint(1,2))
			
			#отправка формы
			element = driver.find_element_by_css_selector('#SubmitButton')
			element.click()
			#_______________________MAIL ACCEPT
			
			time.sleep(6)
			count = mail.count_messages()
			count = mail.count_messages()
			print(count)
			if count != "0":
				text = mail.get_message(0)
				print(text)
				confirmation_link = text[text.find("https://lolzteam.online/account-confirmation/"):]
				confirmation_link = confirmation_link[:confirmation_link.find('\n')]
				print("link:")
				print(confirmation_link)
				time.sleep(2)
				driver.get(confirmation_link)
				time.sleep(3)
			else:

				driver.close()
			
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
			print(login)
		except:pass



######################__CODE__####################
lolz = Lolzteam(path,server)

def reg_start(lolz):
	global k,proxy_list
	while True:
		try:
			proxy = proxy_list[k]
		except:
			k = 0
			proxy = proxy_list[k]
		k += 1

		mail = Mail()
		
		email = mail.get_mail()
		login = User().login_by_mail(email)
		password = User().get_password()
		
		lolz.reg(login,email,password,proxy,mail)

#запускаем потоки
for i in range(threads):
	threading.Thread(target=reg_start, args=(lolz,)).start()
	time.sleep(2)
