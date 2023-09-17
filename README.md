# Dataconnector
Data collection from wallstreetsurvivor website


## Installation

First, install the required dependencies by running:
```bash
python3 -m pip install -r requirements.txt
```

## Setup
1. Navigate to the project directory
```bash
cd dataconnector
```

2. Make migrations
```bash
python manage.py migrate
```

3. Create a .env file in the same directory as settings.py with your WallStreetSurvivor username and password
```bash
USERNAME=yourusername
PASSWORD=yourpassword
```

4. Run tests to check if everything is working correctly
```bash
python manage.py test
```

5. Run the server
```bash
python manage.py runserver
```

## Make requests
You can make requests like this:
```bash
 curl -X POST -H "Content-type: application/json" -H "Accept: application/json" -d '{
    "username": "your username>",
    "password": "your password",
    "start_date": "2023-03-15",
    "end_date": "2023-09-17"
}' "http://127.0.0.1:8000/wallstreetsurvivor/"
```

You should receive a response like this:
```json
{
  "response": [
    {
      "actions": "",
      "transaction_type": "Market - Buy",
      "symbol": "K",
      "quantity": 3,
      "type": "Equities",
      "price_status": "60.0500",
      "fee": "1.00",
      "date_time": "09/15/2023 - 12:52"
    },
  ]
}
```









