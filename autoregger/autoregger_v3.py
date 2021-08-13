from selenium import webdriver as wb
import time
import requests
import threading
import random
import json

#consts
server_name = "https://lolzteam.online/"
path_to_driver = "C:/Users/User/Desktop/phantomjs-2.1.1-windows/bin/phantomjs.exe"
threads = int(input("Количество потоков: "))
client_id = "sh33djax08y8wa1u"
client_secret = "w417z4xghfmfqweu"
accounts = 0
#end

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

class Lolzteam:

	def __init__(self,path,server,client_id,client_secret):
		self.path = path
		self.server = server
		self.client_id = client_id
		self.client_secret = client_secret

	def create_user(self,login,email,password):
		ses = requests.session()
		data={
		"client_id":self.client_id,
		"client_secret":self.client_secret,
		"user_email":email,
		"username":login,
		"password":password
		}
		ses.post(f"{self.server}api/index.php?users",data=data).text

	def reg(self):
                global accounts
                #подключаем классы
                user = User()

                #запускаем браузер с мылом
                mail = wb.Chrome(self.path)
                try:
                        mail.get("https://generator.email/")
                        time.sleep(1)

			#get email
                        source = mail.page_source
                        source = source[source.find("<span id=\"email_ch_text\">"):]

			#get userdata
                        email = source[25:source.find("</span>")]
                        login = user.login_by_mail(email)
                        password = user.get_password()

                        self.create_user(login,email,password)

			#confim email
                        time.sleep(6)
                        a = mail.page_source
                        a = a[a.find(f"{self.server}account-confirmation/"):]
                        a = a[:a.find("\"")]
                        mail.get(a)
                        time.sleep(2)

			#__AUTH
                        mail.get("https://lolzteam.online/login")
			#write
                        mail.find_element_by_css_selector('#ctrl_pageLogin_login').send_keys(login)
                        mail.find_element_by_css_selector('#ctrl_pageLogin_password').send_keys(password)
                        mail.find_element_by_xpath('//input[@class="button primary large full"]').click()

			#get token
                        mail.get(f"{self.server}account/authorize?client_id={self.client_id}&client_secret={self.client_secret}&response_type=token&scope=read+post")
                        time.sleep(2)
                        uri = mail.current_url
                        token = uri[uri.find("access_token=")+13:uri.find("&")]

                        #write in file
                        mes = "\n"+login+":"+password+":"+email+":"+token
                        f=open("users.txt","a")
                        f.write(mes)
                        f.close()

                        accounts+=1
                        print(f"[{accounts}] {email}")

			#CLOSE
                        mail.close()
                except:
                        mail.close()


#CODE
lzt = Lolzteam(path_to_driver, server_name ,client_id ,client_secret)

def main(lzt):
	while True:
		try:
			lzt.reg()
		except:pass

for i in range(threads):
	threading.Thread(target=main, args=(lzt,)).start()
