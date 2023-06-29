import requests
import json
import sys
from rich import print
import pandas as pd

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
    spent = 0
    s = requests.Session()
    last_order_id = ''
    num_of_orders = 0

    f = open("SwiggyOrdersData.csv", "w")
    f.write('order_total'+","+'order_id'+","+"delivery_address")

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
            f.write("\n"+str(order['order_total'])+"," +
                    str(order['order_id'])+"," +
                    str(order['delivery_address']['address']).replace(",", ""))

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
        print("[red][-] [u]cookies.json[/u] not found in the path[/red]")
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
