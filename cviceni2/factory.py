class PaymentProcessor:
    def pay(self, payment_type, amount):
        if payment_type == "card":
            ...
        elif payment_type == "paypal":
            ...
        elif payment_type == "bank":
            ...


if __name__ == "__main__":
    processor = PaymentProcessor()
    processor.pay("card", 100)
    processor.pay("paypal", 200)
    processor.pay("bank", 300)