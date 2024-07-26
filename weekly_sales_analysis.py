from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from collections import defaultdict
import matplotlib.pyplot as plt
from prettytable import PrettyTable
from database import Database

# Strategy Pattern for Weekly Sales Analysis
class WeeklySalesAnalysisStrategy(ABC):
    @abstractmethod
    def analyze(self, year):
        pass

class WeeklySalesAnalysis(WeeklySalesAnalysisStrategy):
    def __init__(self, branches):
        self.branches = branches

    def analyze(self, year):
        weekly_sales = defaultdict(lambda: {'total_sales_amount': 0.0, 'customer_count': set(), 'total_quantity': 0, 'products': defaultdict(lambda: {'quantity': 0, 'revenue': 0.0})})
        
        for branch in self.branches:
            for sale in branch.sales:
                if sale.date.year == year:
                    week_start = sale.date - timedelta(days=sale.date.weekday())
                    week_end = week_start + timedelta(days=6)
                    week_key = f"{week_start.date()} - {week_end.date()}"

                    weekly_sales[week_key]['total_sales_amount'] += sale.total_price
                    weekly_sales[week_key]['customer_count'].add(sale.sale_id)
                    weekly_sales[week_key]['total_quantity'] += sale.quantity
                    weekly_sales[week_key]['products'][sale.product.product_id]['quantity'] += sale.quantity
                    weekly_sales[week_key]['products'][sale.product.product_id]['revenue'] += sale.total_price

        return weekly_sales

# Observer Pattern for Plotting
class WeeklySalesObserver(ABC):
    @abstractmethod
    def update(self, weekly_sales):
        pass

class WeeklySalesPlotter(WeeklySalesObserver):
    def update(self, weekly_sales):
        week_labels = list(weekly_sales.keys())
        total_sales = [data['total_sales_amount'] for data in weekly_sales.values()]
        avg_transaction_values = [
            data['total_sales_amount'] / len(data['customer_count']) if data['customer_count'] else 0
            for data in weekly_sales.values()
        ]
        sales_volumes = [data['total_quantity'] for data in weekly_sales.values()]
        
        self.print_tables(weekly_sales)
        self.plot_sales_analysis(week_labels, total_sales, avg_transaction_values, sales_volumes)
        self.plot_product_sales(weekly_sales)
    
    def print_tables(self, weekly_sales):
        for week, data in weekly_sales.items():
            print(f"\n{'='*40}")
            print(f"Weekly Sales Report: {week}")
            print(f"{'='*40}")
            print(f"Total Sales Amount: {data['total_sales_amount']:.2f} LKR")
            print(f"Customer Count: {len(data['customer_count'])}")
            avg_transaction_value = data['total_sales_amount'] / len(data['customer_count']) if data['customer_count'] else 0
            print(f"Average Transaction Value: {avg_transaction_value:.2f} LKR")
            print(f"Sales Volume: {data['total_quantity']}")
            print("\n" + "-"*40)
            
            # Top-Selling Products
            sorted_products = sorted(data['products'].items(), key=lambda x: x[1]['quantity'], reverse=True)
            top_selling_products = sorted_products[:10]
            print("Top-Selling Products:")
            self.print_table(
                headers=["Product ID", "Sales Quantity", "Revenue"],
                rows=[(pid, info['quantity'], info['revenue']) for pid, info in top_selling_products]
            )
            
            # Low-Selling Products
            low_selling_products = sorted_products[-10:]
            print("\nLow-Selling Products:")
            self.print_table(
                headers=["Product ID", "Sales Quantity", "Revenue"],
                rows=[(pid, info['quantity'], info['revenue']) for pid, info in low_selling_products]
            )
            
            print("\n" + "-"*40)
    
    def print_table(self, headers, rows):
        table = PrettyTable()
        table.field_names = headers
        for row in rows:
            table.add_row(row)
        print(table)

    def plot_sales_analysis(self, weeks, total_sales, avg_transaction_values, sales_volumes):
        plt.figure(figsize=(15, 10))
        
        plt.subplot(3, 1, 1)
        plt.plot(weeks, total_sales, marker='o')
        plt.title('Total Sales Amount Over Time')
        plt.xlabel('Weeks')
        plt.ylabel('Total Sales Amount (LKR)')
        plt.xticks(rotation=45)
        
        plt.subplot(3, 1, 2)
        plt.plot(weeks, avg_transaction_values, marker='o', color='orange')
        plt.title('Average Transaction Value Over Time')
        plt.xlabel('Weeks')
        plt.ylabel('Average Transaction Value (LKR)')
        plt.xticks(rotation=45)
        
        plt.subplot(3, 1, 3)
        plt.plot(weeks, sales_volumes, marker='o', color='green')
        plt.title('Sales Volume Over Time')
        plt.xlabel('Weeks')
        plt.ylabel('Sales Volume')
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        plt.show()

    def plot_product_sales(self, weekly_sales):
        top_selling_products = []
        low_selling_products = []
        
        for data in weekly_sales.values():
            sorted_products = sorted(data['products'].items(), key=lambda x: x[1]['quantity'], reverse=True)
            top_selling_products.extend(sorted_products[:10])
            low_selling_products.extend(sorted_products[-10:])
        
        top_product_ids = [pid for pid, info in top_selling_products]
        top_quantities = [info['quantity'] for pid, info in top_selling_products]
        top_revenues = [info['revenue'] for pid, info in top_selling_products]
        
        low_product_ids = [pid for pid, info in low_selling_products]
        low_quantities = [info['quantity'] for pid, info in low_selling_products]
        low_revenues = [info['revenue'] for pid, info in low_selling_products]
        
        plt.figure(figsize=(15, 10))
        
        plt.subplot(2, 1, 1)
        plt.bar(top_product_ids, top_quantities)
        plt.title('Top-Selling Products (Quantity)')
        plt.xlabel('Product ID')
        plt.ylabel('Quantity Sold')
        plt.xticks(rotation=45)
        
        plt.subplot(2, 1, 2)
        plt.bar(low_product_ids, low_quantities, color='red')
        plt.title('Low-Selling Products (Quantity)')
        plt.xlabel('Product ID')
        plt.ylabel('Quantity Sold')
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        plt.show()

# Notifier Class
class SalesNotifier:
    def __init__(self):
        self._observers = []

    def add_observer(self, observer):
        self._observers.append(observer)

    def notify_observers(self, weekly_sales):
        for observer in self._observers:
            observer.update(weekly_sales)
            
# Main function for Weekly Sales Analysis
def weekly_sales_analysis():
    # Initialize database and load data
    db = Database()
    db.load_data('data/branches.csv', 'data/sales.csv', 'data/products.csv')
    
    sales_data = []
    for branch in db.get_branches():
        sales_data.extend(branch.sales)
    
    # Create a Weekly Sales Analysis Strategy
    strategy = WeeklySalesAnalysis(db.get_branches())
    weekly_sales = strategy.analyze(year=2024)
    
    # Create Notifier and Observer
    notifier = SalesNotifier()
    plotter = WeeklySalesPlotter()
    notifier.add_observer(plotter)
    
    # Notify observers
    notifier.notify_observers(weekly_sales)

if __name__ == "__main__":
    weekly_sales_analysis()


