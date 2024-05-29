import os
import requests
from bs4 import BeautifulSoup
import telebot
from telebot import types
import random
import uuid
import re
import pycountry
import time
from faker import Faker
from Strip import Payment
faker = Faker()
token = "7172061329:AAFL3NVUELJjrIF-H6mvgbyz97t2dqtclks"
bot = telebot.TeleBot(token, parse_mode="HTML")

@bot.callback_query_handler(func=lambda call: call.data == 'stop')
def menu_callback(call):
    os._exit(0)

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "<strong>Send the Combo TXT File \n ارسل ملف الكومبو</strong>")

@bot.message_handler(content_types=["document"])
def main(message):
    ch = 0
    live = 0
    dd = 0
    koko = bot.reply_to(message, "CHECKING STARTED BY MAHOS ✅...⌛").message_id
    file_info = bot.get_file(message.document.file_id)
    ee = bot.download_file(file_info.file_path)

    with open("combo.txt", "wb") as w:
        w.write(ee)

    try:
        with open("combo.txt", 'r') as file:
            lino = file.readlines()
            total = len(lino)

            for P in lino:
                try:
                    start_time = time.time()
                    res = Payment(P)
                    print(res)
                except Exception as e:
                    print(e)
                    continue

                try:
                    if any(keyword in res for keyword in ["Your card has insufficient funds", "insufficient funds", "Payment success", "Thank you for your support.", "insufficient_funds", "card has insufficient funds", "successfully", "Your card does not support this type of purchase.", "payment-successfully"]):
                        ch += 1
                        stay = 'CHARGED ✅'
                        try:
                            kill = res.get('message', "")
                        except:
                            kill = ""
                        infobin(P, stay, kill, start_time, message)
                    elif any(keyword in res for keyword in ["Your card's security code is incorrect.", "security code is invalid", "incorrect_cvc", "security code is incorrect", "Your card zip code is incorrect.", "card's security code is incorrect"]):
                        live += 1
                        stay = 'CCN,CVV ♻️'
                        try:
                            kill = res.get('message', "")
                        except:
                            kill = ""
                        infobin(P, stay, kill, start_time, message)
                        
                    elif any(keyword in res for keyword in ["Your card was declined.", "Your card has expired", "risk_threshold", "Error Processing Payment", "Your card number is incorrect.", "Invalid or Missing Payment Information - Please Reload and Try Again"]):
                        dd += 1
                        stay = 'DEAD ❌'
                        try:
                            kill = res.get('message', "")
                        except:                            
                            kill = ""
                    else:
                        dd += 1
                        stay = 'DEAD ❌'
                        try:
                            kill = res.get('message', "")
                        except:                            
                            kill = ""
                except Exception as e:
                    print(e)
                    dd += 1

                mes = types.InlineKeyboardMarkup(row_width=1)
                cm1 = types.InlineKeyboardButton(f"• {P} •", callback_data='u8')
                status = types.InlineKeyboardButton(f"• 𝗦𝗧𝗔𝗧𝗨𝗦 ➜ {kill} •", callback_data='u8')
                cm3 = types.InlineKeyboardButton(f"• 𝗖𝗛𝗔𝗥𝗚𝗘 ✅ ➜ [ {ch} ] •", callback_data='x')
                cm4 = types.InlineKeyboardButton(f"• 𝗔𝗣𝗣𝗥𝗢𝗩𝗘𝗗 ✅ ➜ [ {live} ] •", callback_data='x')
                cm5 = types.InlineKeyboardButton(f"• 𝗗𝗘𝗖𝗟𝗜𝗡𝗘𝗗 ❌ ➜ [ {dd} ] •", callback_data='x')
                cm6 = types.InlineKeyboardButton(f"• 𝗧𝗢𝗧𝗔𝗟 👻 ➜ [ {total} ] •", callback_data='x')
                stop = types.InlineKeyboardButton(f"[ 𝐒𝐓𝐎𝐏 ]", callback_data='stop')
                mes.add(cm1, status, cm3, cm4, cm5, cm6, stop)
                bot.edit_message_text(chat_id=message.chat.id, message_id=koko,
                                      text='''WAITING MONEY ➜ @maho_s9 ''', reply_markup=mes)

    except Exception as e:
        print(e)

def infobin(P, stay, kill, start_time, message):
    bin_number = P[:6]
    url = "https://bins.su"
    payload = f"action=searchbins&bins={bin_number}&bank=&country="
    headers = {
        'User-Agent': "Mozilla/5.0 (Linux; Android 10; ART-L29N; HMSCore 6.13.0.321) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.88 HuaweiBrowser/14.0.5.303 Mobile Safari/537.36",
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "max-age=0",
        'sec-ch-ua': "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"99\", \"HuaweiBrowser\";v=\"99\"",
        'sec-ch-ua-mobile': "?1",
        'sec-ch-ua-platform': "\"Android\"",
        'Upgrade-Insecure-Requests': "1",
        'origin': "https://bins.su",
        'Sec-Fetch-Site': "same-origin",
        'Sec-Fetch-Mode': "navigate",
        'Sec-Fetch-User': "?1",
        'Sec-Fetch-Dest': "document",
        'Referer': "https://bins.su/",
        'Accept-Language': "ar-YE,ar;q=0.9,en-YE;q=0.8,en-US;q=0.7,en;q=0.6",
    }

    api = requests.post(url, data=payload, headers=headers)
    res = re.search(r'<div id="result">(.+?)</div>', api.text, re.DOTALL)

    if res:
        bins = re.findall(r'<tr><td>(\d+)</td><td>([A-Z]{2})</td><td>(\w+)</td><td>(\w+)</td><td>(\w+)</td><td>(.+?)</td></tr>', res.group(1))
        if bins:
            bin_number, country_code, vendor, card_type, level, bank = bins[0]
        else:
            bin_number, country_code, vendor, card_type, level, bank = "", "", "", "", "", ""
    else:
        bin_number, country_code, vendor, card_type, level, bank = "", "", "", "", "", ""

    if len(country_code) == 2 and country_code.isalpha():
        country_code = country_code.upper()
        flag_offset = 127397
        flag = ''.join(chr(ord(char) + flag_offset) for char in country_code)
    else:
        flag = ""

    try:
        country = pycountry.countries.get(alpha_2=country_code)
        country_name = country.name if country else ""
    except:
        country_name = ""

    end_time = time.time()
    duration = int(end_time - start_time)

    msg = f"""
𝐒𝐭𝐫𝐢𝐩 𝐂𝐡𝐫𝐚𝐠𝐞 ⇾ 💱
𝐂𝐚𝐫𝐝 ⇾ {P}
𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞 ⇾ {kill}
𝐌𝐚𝐬𝐬𝐚𝐠𝐞 ⇾ {stay}
━━━━━━━━━━━━━━━━━
- 𝗕𝗜𝗡 ⇾ {bin_number}
- 𝗜𝗻𝗳𝗼 ⇾ {card_type} - {level}
- 𝐈𝐬𝐬𝐮𝐞𝐫 ⇾ {bank}
- 𝐂𝐨𝐮𝐧𝐭𝐫𝐲 ⇾ {country_name} {flag}
- 𝐎𝐓𝐇𝐄𝐑 ⇾ {vendor}
- 𝐓𝐢𝐦𝐞⇾ {duration}s
━━━━━━━━━━━━━━━━━
◆ 𝐁𝐘: @maho_s9
    """

    bot.reply_to(message, msg)

print('Done')
while True:
    try:
        bot.infinity_polling()
    except Exception as e:
        print(e)
        pass
