import requests
import json

uid = "137327"#ид юзера
tokens = []
f = open("users.txt","r")
for line in f:
	tokens.append(line.split(":")[3][:-1])
print("В базе ", len(tokens),"аккаунтов")

print("Нажмите ENTER для запуска...")
input()

for token in tokens:
	try:
		session = requests.Session()
		session.get(f"https://lolzteam.online/api/index.php?threads/228&oauth_token={token}")
		data={
            "oauth_token":token
		}
		print(session.post(f"https://lolzteam.online/api/index.php?users/{uid}/followers",data=data).text)
		
	except:pass
