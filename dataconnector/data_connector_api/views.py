MAX_TRANSACTION_LIST_SIZE = 12
TRANSACTION_TYPE = 1
PAGE_INDEX = 0

import json
import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Trade

def login_to_wallstreetsurvivor(username, password):
    session = requests.Session()

    login_data = {
        "UserName": username,
        "Password": password
    }

    response = session.post("https://app.wallstreetsurvivor.com/login?returnUrl=/account/dashboardv2", data=login_data)
    
    if response.status_code == 200:
        # Check if has correct login cookies
        login_cookie = response.cookies.get('__WallStreetSurvivorProd')
        if login_cookie is None or login_cookie == '':
            raise RuntimeError("Wrong Credentials")
        else: 
            return session, response.cookies.get_dict()
    else:
        return None, None

def extract_transaction_data(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    rows = soup.find_all('tr')
    data = []

    for row in rows:
        columns = row.find_all('td')
        actions = columns[0].text.strip()
        transaction_type = columns[1].text.strip()
        symbol = columns[2].text.strip()
        quantity = columns[3].text.strip()
        type = columns[4].text.strip()
        price_status = columns[5].text.strip()
        fee = columns[6].text.strip()
        date_time = columns[7].text.strip()

        data.append({
            "actions": actions,
            "transaction_type": transaction_type,
            "symbol": symbol,
            "quantity": quantity,
            "type": type,
            "price_status": price_status,
            "fee": fee,
            "date_time": date_time
        })

    return data

@csrf_exempt
def wallstreetsurvivor_view(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username')
        password = data.get('password')
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        # Ensure that username and password were send in the body
        if not all([username, password]):
            return JsonResponse({'error': 'Missing one or more required fields.'}, status=400)

        try:
            session, cookie = login_to_wallstreetsurvivor(username, password)
        except:
            return JsonResponse({'message': 'Wrong credentials'})


        params = {
            "pageIndex": PAGE_INDEX,
            "pageSize": MAX_TRANSACTION_LIST_SIZE,
            "startDate": start_date,
            "endDate": end_date,
            "sortField": "CreateDate",
            "sortDirection": "DESC",
            "transactionType": TRANSACTION_TYPE
        }

        get_transactions_response = session.get("https://app.wallstreetsurvivor.com/account/gettransactions", params=params, cookies=cookie)

        if get_transactions_response.status_code == 200:
            try:
                resp_json = json.loads(get_transactions_response.text)
            except:
                return JsonResponse({'message': 'Response is not Json'})
            html_content = resp_json['Html']
            transaction_data = extract_transaction_data(html_content)
            return JsonResponse({"response": transaction_data}, json_dumps_params={'indent': 2})
        else:
            return JsonResponse({'message': f'GET request failed with status code {get_transactions_response.status_code}'})

    return JsonResponse({'message': 'This view only accepts POST requests'})