import pytest
from unittest.mock import patch, MagicMock
from main import (
    DatabaseSingleton, MonthlySalesAnalysisFactory, SalesReportNotifier,
    PlotDailySalesReportObserver, PlotHourlySalesReportObserver,
    User, Authentication, main_menu, perform_monthly_sales_analysis
)

# Test Database Singleton
def test_database_singleton():
    db1 = DatabaseSingleton().get_database()
    db2 = DatabaseSingleton().get_database()
    assert db1 is db2, "DatabaseSingleton should return the same instance"

# Test Authentication
def test_login_success():
    auth = Authentication()
    with patch('builtins.input', side_effect=['admin', 'password123']):
        user = auth.login()
        assert user is not None
        assert user.username == 'admin'

def test_login_failure():
    auth = Authentication()
    with patch('builtins.input', side_effect=['admin', 'wrongpassword']):
        user = auth.login()
        assert user is None

def test_logout(capsys):
    auth = Authentication()
    user = User('admin', 'password123')
    auth.logout(user)
    captured = capsys.readouterr()
    assert "User admin logged out successfully." in captured.out

# Test Monthly Sales Analysis
def test_monthly_sales_analysis_creation():
    factory = MonthlySalesAnalysisFactory()
    db = DatabaseSingleton().get_database()
    db.load_data = MagicMock()
    db.load_data('data/branches.csv', 'data/sales.csv', 'data/products.csv')
    analysis = factory.create_analysis()
    assert analysis is not None

def test_perform_monthly_sales_analysis(monkeypatch):
    factory = MonthlySalesAnalysisFactory()
    analysis = factory.create_analysis()

    notifier = SalesReportNotifier()
    notifier.add_observer(PlotDailySalesReportObserver())
    notifier.add_observer(PlotHourlySalesReportObserver())

    monkeypatch.setattr('builtins.input', lambda _: '1')
    monkeypatch.setattr('main.display_analysis_options', lambda: '3')

    with patch('main.MonthlySalesAnalysis.analyze', return_value={
        'branch1': {
            'daily_sales_report': {},
            'hourly_sales_report': {},
            'total_sales_amount': 1000,
            'customer_count': 100,
            'sales_volume': 200,
            'average_transaction_value': 10.0,
            'top_selling_products': [('product1', {'quantity': 50, 'revenue': 500})],
            'low_selling_products': [('product2', {'quantity': 5, 'revenue': 50})],
            'sales_by_product_category': {'category1': {'quantity': 50, 'revenue': 500}}
        }
    }):
        perform_monthly_sales_analysis(factory)

def test_main_menu(monkeypatch):
    auth = Authentication()
    user = User('admin', 'password123')

    monkeypatch.setattr('builtins.input', lambda _: '7')
    exit_program = main_menu(auth, user)
    assert exit_program is True

if __name__ == '__main__':
    pytest.main()
