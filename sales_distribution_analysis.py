import matplotlib.pyplot as plt
from database import Database

def sales_distribution_analysis():
    db = Database()
    db.load_data('data/branches.csv', 'data/sales.csv', 'data/products.csv')

    sales = [sale.total_price for branch in db.get_branches() for sale in branch.sales]

    if not sales:
        print("No sales data available.")
        return

    print("\n=== Sales Distribution Analysis ===\n")

    # Sales Distribution: Histogram
    plt.figure(figsize=(12, 6))
    plt.hist(sales, bins=20, edgecolor='black', color='skyblue')
    plt.title('Sales Distribution')
    plt.xlabel('Total Sales Amount (LKR)')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()

    # Average Purchase Value
    average_value = sum(sales) / len(sales)
    print("\n--- Average Purchase Value ---")
    print(f"Average Purchase Value: {average_value:.2f} LKR")

    # Value Segmentation
    below_1000 = len([x for x in sales if x < 1000])
    between_1000_and_5000 = len([x for x in sales if 1000 <= x <= 5000])
    above_5000 = len([x for x in sales if x > 5000])

    print("\n--- Purchase Value Segmentation ---")
    print(f"Purchases below 1000 LKR: {below_1000}")
    print(f"Purchases between 1000 and 5000 LKR: {between_1000_and_5000}")
    print(f"Purchases above 5000 LKR: {above_5000}")

if __name__ == "__main__":
    sales_distribution_analysis()
