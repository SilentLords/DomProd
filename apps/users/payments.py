from yandex_checkout import Configuration, Payment
DEBUG = False

if not DEBUG:
    Configuration.account_id = 723426
    Configuration.secret_key = "live_8aVT9k5VloQ4KJV3Ma3OopxbrbVc2znwO6OuvVDl2uA"
else:
    Configuration.account_id = 725297
    Configuration.secret_key = 'test_N1nxSKIVxuNqTJIOC12laqvuVpFtH8_0Zsdby3F6T74'


def create_payment(price, days):
    payment = Payment.create({
        "amount": {
            "value": f"{price}",
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "http://localhost:3000/pay_success"
        },
        "capture": True,
        "description": "Заказ №1",
        'metadata': {
            'days': days
        }
    })
    p_id = payment.id
    print(p_id)
    return payment.confirmation.confirmation_url, p_id



def check_payment(p_id):
    payment_status = Payment.find_one(payment_id=p_id).status
    if payment_status == 'succeeded':
        return True
    else:
        return False
