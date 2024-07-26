class Branch:
    def __init__(self, branch_id, name, location):
        self.branch_id = branch_id
        self.name = name
        self.location = location
        self.sales = []

    def add_sale(self, sale):
        self.sales.append(sale)

    def __repr__(self):
        return f'Branch(id={self.branch_id}, name={self.name}, location={self.location}, sales={self.sales})'
