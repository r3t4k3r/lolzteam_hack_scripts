import requests
import json

tokens = []
f = open("users.txt","r")
for line in f:
	tokens.append(line.split(":")[3][:-1])
print("В базе ",len(tokens),"аккаунтов")

print("Нажмите ENTER для запуска...")
input()

name_thread = "БАСТЕР с ДР УРА!"
post_body = """
Бастер ура, поздравляю тебя с днем рождения.

Нашему другу сегодня исполнилось 33 года, поздравим его!!!!!
Пишите ему во все соц сети и шлите открытки.

@Бастер желаю тебе счастья, здоровья, перестать слушать Элджея, а так-же долгих лет жизни !!!!!

Написать мне:
vk*com/id474370216

Мой аккаунт, если оставите коментарий буду рад.
@g1fl3x :2011_like:

PS: @Джесус - пидорас (ничего личного бро).
"""

u = 1

while True:
	for token in tokens:
		try:
			session = requests.Session()
			session.get(f"https://lolzteam.online/api/index.php?threads/228&oauth_token={token}")

			full_name = name_thread + " №" +str(u)
			full_body = post_body + "НОМЕР ТЕМЫ: " +str(u)
			response = json.loads(session.post(f"https://lolzteam.online/api/index.php?threads&forum_id=86&thread_title={full_name}&post_body={full_body}&oauth_token={token}").text)
			thread_id = response["thread"]["thread_id"]
			print("Создана тема: "+full_name)
			u += 1
		except:
			pass
