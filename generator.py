import requests, names, time, os, threading
from account_generator_helper import GmailNator
from datetime import datetime, timedelta
from colorama import init, Fore
from random import randint
#from discord_webhook import DiscordWebhook, DiscordEmbed
init()

def putSql(email,passw,first,last,brith):
    """webhook = DiscordWebhook(url='nope')
    embed = DiscordEmbed(title='O\'Tacos Account Generator', description='An Other Account Generated:', color='03b2f8')
    embed.add_embed_field(name='💌Email', value=email[:10] + "***********@gmail.com")
    embed.add_embed_field(name='💳Password', value=passw)
    embed.add_embed_field(name='😀First Name', value=first)
    embed.add_embed_field(name='😁Last Name', value=last)
    embed.add_embed_field(name='👶Birth', value=brith)
    webhook.add_embed(embed)
    webhook.execute()"""
    pass

started = time.time()

generated = 0
verified = 0
error = 0
genera = []

def getAuthToken(email,passw):
    headers = {
        "accept": "application/x-www-form-urlencoded",
        "host": "api.flyx.cloud",
        "user-agent": "okhttp/4.9.1"
    }
    parms = {
        "grant_type": "password",
        "username": email,
        "password": passw,
        "client_id": "app",
        "client_secret": "1QQ2CRDBOHVTSK5R6ZLFWJ7WQUCCM",
        "scope": "ordering_api app_api identity_api payment_api offline_access openid"
    }
    try:
        loginReq = requests.post("https://api.flyx.cloud/otacos/app/Connect/Token", headers=headers, data=parms)
        return loginReq.json()['access_token']
    except:
        error += 1
        return "None"
def genAccount(first,last,email, passw):
    headers = {
        "accept": "application/json, text/plain, */*",
        "authorization": "",
        "host": "api.flyx.cloud",
        "user-agent": "okhttp/4.9.1"
    }
    payload = {
    "firstName": first,
    "lastName": last,
    "email": email,
    "password": passw,
    "confirmPassword": passw,
    "acceptPushNotifications": True,
    "isAdvanced": False,
    "language": "fr-FR",
    "optins": [
        {
        "id": 1,
        "translationKey": "optins.cc.cgu.sales",
        "moduleId": 2,
        "isChecked": True,
        "isMandatory": False,
        "hasChanged": False,
        "legalTextIds": [
            7,
            5
        ]
        },
        {
        "id": 2,
        "translationKey": "optins.loyalty.privacy.cgu.sales",
        "moduleId": 1,
        "isChecked": True,
        "isMandatory": False,
        "hasChanged": False,
        "legalTextIds": [
            2,
            8,
            5
        ]
        },
        {
        "id": 3,
        "translationKey": "optins.core.marketing.privacy",
        "moduleId": 4,
        "isChecked": True,
        "isMandatory": False,
        "hasChanged": False,
        "legalTextIds": [
            2
        ]
        },
        {
        "id": 4,
        "translationKey": "optins.core.tracking",
        "moduleId": 4,
        "isChecked": True,
        "isMandatory": False,
        "hasChanged": False,
        "legalTextIds": [
            2
        ]
        }
    ]
    }
    try:
        responce = requests.post("https://api.flyx.cloud/otacos/app/api/User", headers=headers, json=payload)
        if "data" not in responce.text:
            return responce.json()
        else:
            return responce.json()['data']
    except:
        return "None"

def addProfileInfo(token, date ,zip):
    headers = {
        "accept": "application/json, text/plain, */*",
        "authorization": "Bearer " + token,
        "host": "api.flyx.cloud",
        "user-agent": "okhttp/4.9.1"
    }
    payload = {
        "Gender": "Male",
        "BirthDate": str(str(date) + "/1998"),
        "Country": "France",
        "ZipCode": str(zip),
        "FavoriteUnits": [
            "Medium tacos"
        ],
        "FavoriteStores": [
            173
        ]
    }
    try:
        profileInfo = requests.put("https://api.flyx.cloud/otacos/app/api/AdvancedProfile", headers=headers, json=payload)
        if "data" not in profileInfo.text:
            print(profileInfo.json())
            error += 1
            return "None"
        else:
            finalReq = requests.put("https://api.flyx.cloud/otacos/app/api/Optin/2/true", headers=headers, json={})
            if "data" not in profileInfo.text:
                print(profileInfo.json())
                error += 1
                return "None"
            else:
                return "Miaou"
    except:
        error += 1
        return "None"

def regAcc():
    try:
        global generated
        global verified
        global error
        first = names.get_first_name()
        last = names.get_last_name()
        mail = GmailNator()
        mail.set_email(mail.get_email_online(True,True,True))
        email = mail._email
        passw = "$y$yG€n-" + str(randint(10000,1000000)) + "-@#"
        result = genAccount(first, last, email, passw)
        if result != "None":
            generated += 1
            if "-" in result:
                time.sleep(5)
                for _letter in mail.get_inbox():
                    if "tacos" in _letter.letter:
                        mailVerif = _letter.letter.replace("\\r\\n", "")
                        mailVerif= mailVerif.split('<a href="')[1].split('" style="color: #FFFFFF; font-family: Helvetica; font-size: 18px; font-weight: bold; text-decoration: none;"> Je confirme mon adresse email </a>')[0]
                        mailContent = requests.get(mailVerif, allow_redirects=True).url
                        mailToken = mailContent.split("?token=")[1].split("&guid=")[0]
                        print(Fore.CYAN +"Mail Token [" + mailToken + "]")
                        confirmReq = requests.put("https://api.flyx.cloud/otacos/app/api/User/VerifyEmail?token=" + mailToken + "&guid=" + result).json()
                        if confirmReq['StatusCode'] == 200:
                            token = getAuthToken(email, passw)
                            if token != "None":
                                today = datetime.now()
                                tomorrow = today + timedelta(19)
                                path = tomorrow.strftime('%d-%m-%y')
                                if addProfileInfo(token, tomorrow.strftime('%m/%d'), '33650') != None:
                                    isExist = os.path.exists(path)
                                    if not isExist:
                                        os.makedirs(path)
                                        print("The new directory is created!")
                                    with open(f"./{path}/account.txt", "a",  encoding="utf-8") as myfile:
                                        myfile.write("-----------------Sysy's OTacos Generator-----------------\n\n")
                                        myfile.write(f"Email: {email}\nPassword: {passw}\nFirst Name: {first}\nLast Name: {last}\nGUID: {result}\n\n")
                                        myfile.write("-----------------Sysy's OTacos Generator-----------------\n\n")
                                    with open(f".\{path}\compatch.txt", "a",  encoding="utf-8") as myfile:
                                        myfile.write(f"{email}:{passw} | First Name: {first} | Last Name: {last} | GUID: {result}\n")
                                    
                                    genera.append(f"{email}|{passw}|{first}|{last}|{tomorrow.strftime('%d-%m-%y')}")
                                    verified += 1
                                    print(Fore.CYAN +f"Added Advanced Profile [{tomorrow.strftime('%d/%m')}/1998]")
                                    print(Fore.GREEN +f"Account Created | First: {first} | Last: {last} | Email: {email} | Pass: {passw} | GUID: {result}")
                            else:
                                error +=1
            else:
                error +=1
        else:
            error += 1
            print(Fore.RED + f"Error: {result}")
    except Exception as e:
        error += 1
        print(Fore.RED + f"Error: {e}")

def updateTitle():
    global genera
    while True:
        genperm = round(verified / ((time.time()-started) / 60), 2)
        os.system(f"title O'Tacos Generator - Verfied: {verified} - Generated: {generated} - Money Win: {verified*1.75}$ - Gen/m: {genperm} - Error: {error}")
        time.sleep(0.2)
        if len(genera) >= 20:
            for acc in genera:
                uwu = str(acc).split("|")
                putSql(uwu[0], uwu[1], uwu[2], uwu[3], uwu[4])
            genera = []

def gen():
    while True:
        regAcc()

def main():
    os.system("cls")
    print(Fore.MAGENTA + """
░█████╗░██╗████████╗░█████╗░░█████╗░░█████╗░░██████╗  ░██████╗░███████╗███╗░░██╗
██╔══██╗╚█║╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗██╔════╝  ██╔════╝░██╔════╝████╗░██║
██║░░██║░╚╝░░░██║░░░███████║██║░░╚═╝██║░░██║╚█████╗░  ██║░░██╗░█████╗░░██╔██╗██║
██║░░██║░░░░░░██║░░░██╔══██║██║░░██╗██║░░██║░╚═══██╗  ██║░░╚██╗██╔══╝░░██║╚████║
╚█████╔╝░░░░░░██║░░░██║░░██║╚█████╔╝╚█████╔╝██████╔╝  ╚██████╔╝███████╗██║░╚███║
░╚════╝░░░░░░░╚═╝░░░╚═╝░░╚═╝░╚════╝░░╚════╝░╚═════╝░  ░╚═════╝░╚══════╝╚═╝░░╚══╝

By Not Sysy's#6700 - V0.0.1
    """)
    threading.Thread(target=updateTitle).start()
    for _ in range(int(input("Thread Number> "))):
        threading.Thread(target=gen).start()

main()