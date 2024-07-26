from abc import ABC, abstractmethod
from prettytable import PrettyTable
import matplotlib.pyplot as plt

class ProductPreferenceAnalysisStrategy(ABC):
    @abstractmethod
    def analyze(self):
        pass

class PopularProductsAnalysis(ProductPreferenceAnalysisStrategy):
    def __init__(self, branches):
        self.branches = branches

    def analyze(self):
        product_sales = {}
        for branch in self.branches:
            for sale in branch.sales:
                product_id = sale.product.product_id
                if product_id not in product_sales:
                    product_sales[product_id] = {'quantity': 0, 'revenue': 0.0}
                product_sales[product_id]['quantity'] += sale.quantity
                product_sales[product_id]['revenue'] += sale.total_price

        sorted_products = sorted(product_sales.items(), key=lambda x: x[1]['quantity'], reverse=True)
        top_products = sorted_products[:10]

        return top_products

def print_popular_products_table(popular_products):
    table = PrettyTable()
    table.field_names = ["Product ID", "Quantity Sold", "Total Revenue"]
    for product_id, data in popular_products:
        table.add_row([product_id, data['quantity'], data['revenue']])
    print(table)

def plot_popular_products(popular_products):
    product_ids = [product_id for product_id, _ in popular_products]
    quantities = [data['quantity'] for _, data in popular_products]

    plt.figure(figsize=(12, 6))
    plt.bar(product_ids, quantities)
    plt.title('Top 10 Popular Products')
    plt.xlabel('Product ID')
    plt.ylabel('Quantity Sold')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()
