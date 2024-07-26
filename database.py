import csv
from sale import Sale
from product import Product
from branch import Branch

class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.branches = []
            cls._instance.products = {}
        return cls._instance

    def load_data(self, branches_file, sales_file, products_file):
        self.branches = []
        self.products = {}
        self._load_branches(branches_file)
        self._load_products(products_file)
        self._load_sales(sales_file)

    def _load_branches(self, file):
        with open(file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                branch = BranchFactory.create_branch(row)
                self.branches.append(branch)

    def _load_products(self, file):
        with open(file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                product = ProductFactory.create_product(row)
                self.products[product.product_id] = product

    def _load_sales(self, file):
        with open(file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                sale = SaleFactory.create_sale(row, self.products)
                for branch in self.branches:
                    if branch.branch_id == sale.branch_id:
                        branch.add_sale(sale)
                        break

    def get_branches(self):
        return self.branches

    def get_product(self, product_id):
        return self.products.get(product_id)

# Factories for creating instances
class BranchFactory:
    @staticmethod
    def create_branch(data):
        return Branch(
            branch_id=data['branch_id'],
            name=data['name'],
            location=data['location']  
        )


class ProductFactory:
    @staticmethod
    def create_product(data):
        return Product(
            product_id=data['product_id'],
            name=data['name'],
            price=float(data['price']),
            category=data['category']
        )

class SaleFactory:
    @staticmethod
    def create_sale(data, products):
        product = products.get(data['product_id'])
        return Sale(
            sale_id=data['sale_id'],
            branch_id=data['branch_id'],
            product=product,
            quantity=int(data['quantity']),
            total_price=float(data['total_price']),
            date=data['date'],
            item_price=float(data['item_price'])
        )
