import requests
ses = requests.session()
data={
    "client_id":"sh33djax08y8wa1u",
    "client_secret":"w417z4xghfmfqweu",
    "user_email":"ysora.elkab@gfades.site",
    "username":"mamoeb1288",
    "password":"testsosi"
}
#response = ses.post("https://lolzteam.online/api/index.php?users",data=data).text
data={
    "client_id":"sh33djax08y8wa1u",
    "client_secret":"w417z4xghfmfqweu",
    "grant_type":"refresh_token",
    "refresh_token":"e43d4377ebdd0345edf213519baf401a6e062829"
}
response = ses.post("https://lolzteam.online/api/index.php?oauth/token",data=data).text
print(response)
