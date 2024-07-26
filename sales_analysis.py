from abc import ABC, abstractmethod
from collections import defaultdict
import matplotlib.pyplot as plt

class SalesAnalysisStrategy(ABC):
    @abstractmethod
    def analyze(self, month, year):
        pass

class MonthlySalesAnalysis(SalesAnalysisStrategy):
    def __init__(self, branches):
        self.branches = branches

    def analyze(self, month, year):
        analysis = {}
        for branch in self.branches:
            branch_data = self._initialize_branch_data()

            for sale in branch.sales:
                if sale.date.month == month and sale.date.year == year:
                    self._process_sale(branch_data, sale)

            self._finalize_branch_data(branch_data)
            analysis[branch.branch_id] = branch_data

        return analysis

    def _initialize_branch_data(self):
        return {
            'total_sales_amount': 0.0,
            'sales_volume': 0,
            'weekly_sales': defaultdict(float),
            'product_sales': defaultdict(lambda: {'quantity': 0, 'revenue': 0.0, 'item_price': 0.0}),
            'category_sales': defaultdict(lambda: {'quantity': 0, 'revenue': 0.0}),
            'transaction_values': [],
            'customer_count': 0,
            'daily_sales': defaultdict(lambda: {'quantity': 0, 'revenue': 0.0}),
            'hourly_sales': defaultdict(int)
        }

    def _process_sale(self, branch_data, sale):
        branch_data['total_sales_amount'] += sale.total_price
        branch_data['sales_volume'] += sale.quantity
        week_number = sale.date.isocalendar()[1]
        branch_data['weekly_sales'][week_number] += sale.total_price
        branch_data['product_sales'][sale.product.product_id]['quantity'] += sale.quantity
        branch_data['product_sales'][sale.product.product_id]['revenue'] += sale.total_price
        branch_data['product_sales'][sale.product.product_id]['item_price'] = sale.item_price
        branch_data['category_sales'][sale.product.category]['quantity'] += sale.quantity
        branch_data['category_sales'][sale.product.category]['revenue'] += sale.total_price
        branch_data['transaction_values'].append(sale.total_price)
        branch_data['customer_count'] += 1
        sale_date_str = sale.date.strftime('%Y/%m/%d')
        branch_data['daily_sales'][sale_date_str]['quantity'] += sale.quantity
        branch_data['daily_sales'][sale_date_str]['revenue'] += sale.total_price
        hour = sale.date.hour
        branch_data['hourly_sales'][hour] += sale.quantity

    def _finalize_branch_data(self, branch_data):
        sorted_products = sorted(branch_data['product_sales'].items(), key=lambda x: x[1]['quantity'], reverse=True)
        branch_data['top_selling_products'] = sorted_products[:10]
        branch_data['low_selling_products'] = sorted_products[-10:]
        branch_data['sales_by_product_category'] = branch_data['category_sales']
        branch_data['average_transaction_value'] = branch_data['total_sales_amount'] / branch_data['customer_count'] if branch_data['customer_count'] > 0 else 0.0
        branch_data['daily_sales_report'] = branch_data['daily_sales']
        branch_data['hourly_sales_report'] = branch_data['hourly_sales']

def print_table(headers, rows):
    col_widths = [max(len(str(item)) for item in column) for column in zip(headers, *rows)]
    row_format = "| " + " | ".join(f"{{:<{width}}}" for width in col_widths) + " |"
    header_divider = "+-" + "-+-".join("-" * width for width in col_widths) + "-+"

    print(header_divider)
    print(row_format.format(*headers))
    print(header_divider)
    for row in rows:
        print(row_format.format(*row))
    print(header_divider)

def plot_daily_sales_report(daily_sales_report):
    plt.figure(figsize=(12, 6))
    for branch_id, data in daily_sales_report.items():
        dates = sorted(data.keys())
        quantities = [data[date]['quantity'] for date in dates]
        plt.plot(dates, quantities, marker='o', label=f'Branch {branch_id}')
    
    plt.title('Daily Sales Report for All Branches')
    plt.xlabel('Date')
    plt.ylabel('Sales Quantity')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_hourly_sales_report(hourly_sales_report):
    plt.figure(figsize=(12, 6))
    for branch_id, data in hourly_sales_report.items():
        hours = sorted(data.keys())
        quantities = [data[hour] for hour in hours]
        plt.plot(hours, quantities, marker='o', label=f'Branch {branch_id}')
    
    plt.title('Hourly Sales Report for All Branches')
    plt.xlabel('Hour')
    plt.ylabel('Sales Quantity')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_specific_branch_daily_sales_report(daily_sales_report, branch_id):
    plt.figure(figsize=(12, 6))
    dates = sorted(daily_sales_report.keys())
    quantities = [daily_sales_report[date]['quantity'] for date in dates]
    plt.plot(dates, quantities, marker='o', label=f'Branch {branch_id}')
    
    plt.title(f'Daily Sales Report for Branch {branch_id}')
    plt.xlabel('Date')
    plt.ylabel('Sales Quantity')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45) 
    plt.tight_layout()
    plt.show()

def plot_specific_branch_hourly_sales_report(hourly_sales_report, branch_id):
    plt.figure(figsize=(12, 6))
    hours = sorted(hourly_sales_report.keys())
    quantities = [hourly_sales_report[hour] for hour in hours]
    plt.plot(hours, quantities, marker='o', label=f'Branch {branch_id}')
    
    plt.title(f'Hourly Sales Report for Branch {branch_id}')
    plt.xlabel('Hour')
    plt.ylabel('Sales Quantity')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45) 
    plt.tight_layout()
    plt.show()
