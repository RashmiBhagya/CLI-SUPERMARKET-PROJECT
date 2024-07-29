import csv
from datetime import datetime
from abc import ABC, abstractmethod
from database import Database
from sales_analysis import (
    MonthlySalesAnalysis, print_table, plot_daily_sales_report,
    plot_hourly_sales_report, plot_specific_branch_daily_sales_report,
    plot_specific_branch_hourly_sales_report
)
from product_price_analysis import (
    AverageSellingPriceAnalysis, PriceVariationAnalysis,
    print_price_analysis_table, plot_price_variation
)
from weekly_sales_analysis import WeeklySalesAnalysis, WeeklySalesPlotter
from product_preference_analysis import PopularProductsAnalysis, print_popular_products_table, plot_popular_products
from sales_distribution_analysis import sales_distribution_analysis

# Singleton Pattern for Database
class DatabaseSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.db = Database()
        return cls._instance

    def get_database(self):
        return self._instance.db

# Factory Method Pattern for Analysis
class AnalysisFactory(ABC):
    @abstractmethod
    def create_analysis(self):
        pass

class MonthlySalesAnalysisFactory(AnalysisFactory):
    def create_analysis(self):
        db = DatabaseSingleton().get_database()
        db.load_data('data/branches.csv', 'data/sales.csv', 'data/products.csv')
        return MonthlySalesAnalysis(db.get_branches())

# Strategy Pattern for Analysis Types
class SalesAnalysisStrategy(ABC):
    @abstractmethod
    def analyze(self, month, year):
        pass

# Observer Pattern for Reporting
class SalesReportObserver(ABC):
    @abstractmethod
    def update(self, data):
        pass

class PlotDailySalesReportObserver(SalesReportObserver):
    def update(self, data):
        daily_sales_report = data.get('daily_sales_report')
        plot_daily_sales_report(daily_sales_report)

class PlotHourlySalesReportObserver(SalesReportObserver):
    def update(self, data):
        hourly_sales_report = data.get('hourly_sales_report')
        plot_hourly_sales_report(hourly_sales_report)

class SalesReportNotifier:
    def __init__(self):
        self._observers = []

    def add_observer(self, observer):
        self._observers.append(observer)

    def notify_observers(self, data):
        for observer in self._observers:
            observer.update(data)

# User Authentication
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class Authentication:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        return {'admin': 'admin'}

    def login(self):
        print("\n=== Login ===")
        username = input("Username: ")
        password = input("Password: ")

        if self.users.get(username) == password:
            print("Login successful!")
            return User(username, password)
        else:
            print("Invalid username or password. Please try again.")
            return None

    def logout(self, user):
        print(f"User {user.username} logged out successfully.")

# Menu and Main Logic
def display_analysis_options():
    print("\n--- Monthly Sales Analysis ---")
    print("1. For All Branches")
    print("2. For Specific Branch")
    print("3. Return to Main Menu")
    return input("Please select an option: ")

def perform_monthly_sales_analysis(factory):
    analysis = factory.create_analysis()
    notifier = SalesReportNotifier()
    
    # Add observers to the notifier
    notifier.add_observer(PlotDailySalesReportObserver())
    notifier.add_observer(PlotHourlySalesReportObserver())
    
    while True:
        choice = display_analysis_options()

        if choice == '1':
            monthly_sales = analysis.analyze(month=6, year=2024)
            daily_sales_report = {}
            hourly_sales_report = {}

            for branch_id, data in monthly_sales.items():
                daily_sales_report[branch_id] = data['daily_sales_report']
                hourly_sales_report[branch_id] = data['hourly_sales_report']
                
                print(f"\nBranch ID: {branch_id}")
                print(f"Total Sales Amount: {data['total_sales_amount']}")
                print(f"Customer Count: {data['customer_count']}")
                print(f"Sales Volume: {data['sales_volume']}")
                print(f"Average Transaction Value: {data['average_transaction_value']:.2f}\n")
                
                print("Top-Selling Products:")
                print_table(
                    headers=["Product ID", "Sales Quantity", "Revenue"],
                    rows=[(pid, info['quantity'], info['revenue']) for pid, info in data['top_selling_products']]
                )

                print("\nLow-Selling Products:")
                print_table(
                    headers=["Product ID", "Sales Quantity", "Revenue"],
                    rows=[(pid, info['quantity'], info['revenue']) for pid, info in data['low_selling_products']]
                )

                print("\nSales by Product Category:")
                print_table(
                    headers=["Category", "Quantity", "Revenue"],
                    rows=[(category, info['quantity'], info['revenue']) for category, info in data['sales_by_product_category'].items()]
                )

            notifier.notify_observers({
                'daily_sales_report': daily_sales_report,
                'hourly_sales_report': hourly_sales_report
            })

        elif choice == '2':
            branch_id = input("Enter Branch ID: ")
            branch_data = analysis.analyze(month=6, year=2024).get(branch_id)

            if branch_data:
                print(f"\nBranch ID: {branch_id}")
                print(f"Total Sales Amount: {branch_data['total_sales_amount']}")
                print(f"Customer Count: {branch_data['customer_count']}")
                print(f"Sales Volume: {branch_data['sales_volume']}")
                print(f"Average Transaction Value: {branch_data['average_transaction_value']:.2f}\n")
                
                print("Top-Selling Products:")
                print_table(
                    headers=["Product ID", "Sales Quantity", "Revenue"],
                    rows=[(pid, info['quantity'], info['revenue']) for pid, info in branch_data['top_selling_products']]
                )

                print("\nLow-Selling Products:")
                print_table(
                    headers=["Product ID", "Sales Quantity", "Revenue"],
                    rows=[(pid, info['quantity'], info['revenue']) for pid, info in branch_data['low_selling_products']]
                )

                print("\nSales by Product Category:")
                print_table(
                    headers=["Category", "Quantity", "Revenue"],
                    rows=[(category, info['quantity'], info['revenue']) for category, info in branch_data['sales_by_product_category'].items()]
                )

                plot_specific_branch_daily_sales_report(branch_data['daily_sales_report'], branch_id)
                plot_specific_branch_hourly_sales_report(branch_data['hourly_sales_report'], branch_id)

            else:
                print("Branch ID not found. Please try again.")

        elif choice == '3':
            return

        else:
            print("Invalid choice. Please try again.")

def main_menu(auth, user):
    # Ensure the database is loaded before any analysis
    db = DatabaseSingleton().get_database()
    db.load_data('data/branches.csv', 'data/sales.csv', 'data/products.csv')
    
    while True:
        print("\n--- Menu ---")
        print("1. Monthly Sales Analysis")
        print("2. Product Price Analysis")
        print("3. Product Preference Analysis")
        print("4. Sales Distribution Analysis")
        print("5. Weekly Sales Analysis")
        print("6. Logout")
        print("7. Exit")

        choice = input("Please select an option: ")

        if choice == '1':
            factory = MonthlySalesAnalysisFactory()
            perform_monthly_sales_analysis(factory)
        elif choice == '2':
            product_id = input("Enter Product ID: ")
            avg_price_strategy = AverageSellingPriceAnalysis()
            avg_price = avg_price_strategy.analyze(product_id)
            
            price_variation_strategy = PriceVariationAnalysis()
            price_variation = price_variation_strategy.analyze(product_id)
            
            print_price_analysis_table(product_id, avg_price, price_variation)

            # fetch prices from the database again for plotting
            prices = [sale.item_price for branch in db.get_branches() for sale in branch.sales if sale.product.product_id == product_id]
            plot_price_variation(prices)
        elif choice == '3':
            branches = db.get_branches()
            strategy = PopularProductsAnalysis(branches)
            popular_products = strategy.analyze()
            print_popular_products_table(popular_products)
            plot_popular_products(popular_products)
        elif choice == '4':
            sales_distribution_analysis()
        elif choice == '5':
            branches = db.get_branches()
            strategy = WeeklySalesAnalysis(branches)  
            weekly_sales = strategy.analyze(year=2024)
            
            # Create Notifier and Plotter
            notifier = SalesReportNotifier()
            plotter = WeeklySalesPlotter()
            notifier.add_observer(plotter)
            
            # Notify observers
            notifier.notify_observers(weekly_sales)
        elif choice == '6':
            auth.logout(user)
            return False  
        elif choice == '7':
            print("Exiting the program. Goodbye!")
            return True  # Exit the program
        else:
            print("Invalid choice. Please try again.")

def welcome_screen():
    while True:
        print("\n=== Welcome to Sales Analyzer ===")
        print("1. Login")
        print("2. Exit")

        choice = input("Please select an option: ")

        if choice == '1':
            return True  # Proceed to login
        elif choice == '2':
            print("Exiting the program. Goodbye!")
            return False  # Exit the program
        else:
            print("Invalid choice. Please try again.")

def main():
    auth = Authentication()

    while True:
        if not welcome_screen():
            break

        user = None
        while user is None:
            user = auth.login()

        if main_menu(auth, user):
            break

if __name__ == "__main__":
    main()
