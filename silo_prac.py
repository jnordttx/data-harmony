import pandas as pd
import numpy as np

# Create 1,000 IDs
ids = np.arange(1000, 2000)

# System A (Accounting): Missing 50 random items
acct_ids = np.random.choice(ids, size=950, replace=False)
data_a = {
    'item_id': acct_ids,
    'price_accounting': np.random.uniform(10, 500, size=950).round(2),
    'department': np.random.choice(['Tools', 'Hardware', 'Elec', 'Garden'], size=950)
}

# System B (Warehouse): Missing 50 DIFFERENT random items
wms_ids = np.random.choice(ids, size=950, replace=False)
data_b = {
    'sku_reference': wms_ids,
    'stock_count': np.random.randint(0, 100, size=950),
    'location': [f"Bin-{i}" for i in range(950)]
}

pd.DataFrame(data_a).to_csv('system_accounting.csv', index=False)
pd.DataFrame(data_b).to_csv('system_warehouse.csv', index=False)

print("Large-Scale Silos Generated (1,000 records each)")