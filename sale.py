from datetime import datetime

class Sale:
    def __init__(self, sale_id, branch_id, product, quantity, total_price, date, item_price):
        self.sale_id = sale_id
        self.branch_id = branch_id
        self.product = product
        self.quantity = quantity
        self.total_price = total_price
        self.date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        self.item_price = item_price  

    def get_hour(self):
        return self.date.hour

    def __repr__(self):
        return (f'Sale(id={self.sale_id}, branch_id={self.branch_id}, '
                f'product={self.product}, quantity={self.quantity}, '
                f'total_price={self.total_price}, date={self.date}, item_price={self.item_price})')
