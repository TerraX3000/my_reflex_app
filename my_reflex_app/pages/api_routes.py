async def api_test(item_id: int):
    return {"my_result": item_id}

async def api_transactions():
    return [
        {
            "account": "Checking",
            "date": "2023-01-01",
            "amount": 100
        },
        {
            "account": "Savings",
            "date": "2023-01-01",
            "amount": 200
        },
        {
            "account": "Credit Card",
            "date": "2023-01-01",
            "amount": 300
        },
        {
            "account": "Checking",
            "date": "2023-01-01",
            "amount": 400
        },
        {
            "account": "Savings",
            "date": "2023-01-01",
            "amount": 500
        },
        {
            "account": "Credit Card",
            "date": "2023-01-01",
            "amount": 600
        }
    ]