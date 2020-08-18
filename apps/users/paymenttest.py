from yandex_checkout import Configuration, Payment

Configuration.account_id = 725297
Configuration.secret_key = 'test_N1nxSKIVxuNqTJIOC12laqvuVpFtH8_0Zsdby3F6T74'

payment = Payment.create({
    "amount": {
        "value": "500.00",
        "currency": "RUB"
    },
    "confirmation": {
        "type": "redirect",
        "return_url": "https://www.merchant-website.com/return_url"
    },
    "capture": True,
    "description": "Заказ №2",
    'receipt': {
        "customer": {
            'phone': "79221379198"
        },
        "items": {
            "description": "Сapybara",
            "quantity": 5.000,
            "amount": {
                "value": "2500.50",
                "currency": "RUB"
            },
            "vat_code": 2,
            "payment_mode": "full_payment",
        }
    }
})
print(payment.confirmation.confirmation_url)
