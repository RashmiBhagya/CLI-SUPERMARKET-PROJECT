from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
from prettytable import PrettyTable
from database import Database

class ProductPriceAnalysisStrategy(ABC):
    @abstractmethod
    def analyze(self, product_id):
        pass

class AverageSellingPriceAnalysis(ProductPriceAnalysisStrategy):
    def analyze(self, product_id):
        db = Database()
        product = db.get_product(product_id)
        if not product:
            raise ValueError(f"Product ID {product_id} not found.")
        
        prices = [sale.item_price for branch in db.get_branches() for sale in branch.sales if sale.product.product_id == product_id]
        avg_price = sum(prices) / len(prices) if prices else 0.0

        return avg_price

class PriceVariationAnalysis(ProductPriceAnalysisStrategy):
    def analyze(self, product_id):
        db = Database()
        product = db.get_product(product_id)
        if not product:
            raise ValueError(f"Product ID {product_id} not found.")
        
        prices = [sale.item_price for branch in db.get_branches() for sale in branch.sales if sale.product.product_id == product_id]
        if not prices:
            return 0.0

        avg_price = sum(prices) / len(prices)
        variance = sum((price - avg_price) ** 2 for price in prices) / len(prices)
        stddev = variance ** 0.5

        return stddev

def print_price_analysis_table(product_id, avg_price, price_variation):
    table = PrettyTable()
    table.field_names = ["Product ID", "Average Selling Price", "Price Variation"]
    table.add_row([product_id, avg_price, price_variation])
    print(table)

def plot_price_variation(prices):
    plt.figure(figsize=(12, 6))
    plt.hist(prices, bins=30, edgecolor='black')
    plt.title('Price Variation Distribution')
    plt.xlabel('Price')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.tight_layout()
    plt.show()
