import requests
import json
import sys
from rich import print
import pandas as pd
import ast

HEADERS = {
    'Host': 'www.swiggy.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://www.swiggy.com/my-account/orders',
    'Content-Type': 'application/json'
}

GET_ORDERS_URL = 'https://www.swiggy.com/dapi/order/all?order_id='


def getOrders(cookies):
    print("Retrieving...")
    
    s = requests.Session()
    last_order_id = ''
    idx = 1

    f = open("SwiggyOrdersData.csv", "w")
    f.write('S. No.'+","
            +'Order ID'+","
            +'Order Time'+","
            +'Restaurant'+","
            +'Items'+","
            +'Address'+","
            +'Order Status'+","
            +'Order Amount'+","
            +'Swiggy Payment Method'+","
            +'Swiggy Payment Display Name'+","
            +'Swiggy Payment VPA'+","
            +'Payment Gateway Payment Type'+","
            +'Payment Gateway Payment Card'+","
            +'Payment Gateway Payment Issuer')

    while 1:
        # 10 orders retrieved in each api call
        URL = ''
        if last_order_id != '':
            URL = GET_ORDERS_URL+str(last_order_id).strip()
        else:
            URL = GET_ORDERS_URL

        r = s.get(URL, headers=HEADERS, cookies=cookies)
        resp = json.loads(r.text)

        if resp['statusCode'] == 1:
            print("[red][-] Status Code is 1, exiting[/red]")
            break

        if len(resp['data']['orders']) == 0:
            print("Reached end of orders")
            break

        for order in resp['data']['orders']:
            sno = str(idx)
            order_id = str(order['order_id'])
            order_time = str(order['order_time'])
            restaurant = str(order['restaurant_name']).replace(",", "")
            
            item_names = ""
            for items in order['order_items']:
                item_names += items['name']+" "
            item_names = item_names.replace(",", "")

            flat_no = str(order['delivery_address']['flat_no']).replace(",", "")
            location = str(order['delivery_address']['address']).replace(",", "")
            area = str(order['delivery_address']['area']).replace(",", "")
            address = flat_no+" "+location+" "+area

            order_status = str(order['order_status']).replace(",", "")
            order_amount = str(order['order_total'])
            swiggy_payment_method = str(order['paymentTransactions'][0]['paymentMethod']).replace(",", "")
            swiggy_payment_display_name = str(order['paymentTransactions'][0]['paymentMethodDisplayName']).replace(",", "")
            swiggy_payment_vpa = str(order['paymentTransactions'][0]['paymentMeta']['payerVpa']).replace(",", "")

            try:
                externalPGResponse = json.loads(order['paymentTransactions'][0]['paymentMeta']['extPGResponse'])
                payment_gateway_payment_type = str(externalPGResponse['paymentMethod']).replace(",", "")
                payment_gateway_payment_card = str(externalPGResponse['card']['cardType']).replace(",", "")
                payment_gateway_payment_issuer = str(externalPGResponse['card']['cardIssuer']).replace(",", "")
            except Exception as e:
                payment_gateway_payment_type = ""
                payment_gateway_payment_card = ""
                payment_gateway_payment_issuer = ""

            f.write("\n"+sno+","
                    +order_id+","
                    +order_time+","
                    +restaurant+","
                    +item_names+","
                    +address+","
                    +order_status+","
                    +order_amount+","
                    +swiggy_payment_method+","
                    +swiggy_payment_display_name+","
                    +swiggy_payment_vpa+","
                    +payment_gateway_payment_type+","
                    +payment_gateway_payment_card+","
                    +payment_gateway_payment_issuer)
            
            idx+=1

        last_order_id = resp['data']['orders'][-1]['order_id']

    f.close()


def cookiesToDict():
    print("[green][+][/green] Getting cookies from [u]cookies.json[/u]")
    data = None
    cookies = {}
    try:
        with open("cookies.json", "r") as f:
            data = json.load(f)
    except Exception as e:
        print("[red][-] [u]cookies.json[/u] not found[/red]")
        print(str(e))
        return None

    try:
        for i in data:
            cookies[i['name']] = i['value']
    except Exception as e:
        print("[red][-] Cookies are not in proper format[/red]")
        print(str(e))
        return None

    return cookies


def checkLogin(cookies):
    # First check if logged in
    print("[green][+][/green] Checking if session is valid")
    r = requests.get(GET_ORDERS_URL, headers=HEADERS, cookies=cookies)
    resp = None
    try:
        resp = json.loads(r.text)
    except Exception as e:
        print("[red][-] Unexpected Response received[/red]")
        return False

    if 'statusCode' not in resp or 'data' not in resp:
        print("[red][-] Unexpected Response received[/red]")
        return False
    if resp['statusCode'] == 1:
        print("[red][-] Not logged in, check cookies and try again[/red]")
        return False

    return True

cookies = cookiesToDict()

if checkLogin(cookies):
    getOrders(cookies)
