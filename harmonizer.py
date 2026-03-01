import pandas as pd
import numpy as np

# Pull in 2 CSV's
df_account = pd.read_csv('system_accounting.csv')
df_warehouse = pd.read_csv('system_warehouse.csv')

# Merge the CSV's
df_merge = pd.merge(df_account, df_warehouse, left_on='item_id', right_on='sku_reference', how='outer')

# If item_id, do nothing but if no sku then put item_id
df_merge['final_id'] = df_merge['item_id'].fillna(df_merge['sku_reference'])

# confirm there's no blanks in the final_id column
missing_count = df_merge['final_id'].isnull().sum()

def categorize(row):
    if pd.isna(row['sku_reference']): return 'In Accounting, Missing from WMS'
    if pd.isna(row['item_id']): return 'In WMS, Missing from Accounting'
    return 'Fully Synchronized'

df_merge['match_type'] = df_merge.apply(categorize, axis=1)
print(df_merge.head())

# 1. Clean up the mess: Remove the redundant 'link' columns
df_final = df_merge.drop(columns=['item_id', 'sku_reference'])
print(df_final.head())

# 2. Export the "Single Source of Truth" to a new CSV
df_final.to_csv('master_inventory_reconciliation.csv', index=False)

# 3. Print the Final Report to the Terminal
print("\n" + "="*40)
print("RECONCILIATION SUMMARY REPORT")
print("="*40)
print(df_final['match_type'].value_counts())
print("-" * 40)
health_score = (df_final['match_type'] == 'Fully Synchronized').mean() * 100
print(f"System Data Health: {health_score:.2f}%")
print("="*40)
print("File Exported: master_inventory_reconciliation.csv")

# 1. THE WAREHOUSE TASK LIST (Items they have but aren't on the books)
wms_action = df_merge[df_merge['match_type'] == 'In WMS, Missing from Accounting']
wms_action[['final_id', 'stock_count', 'location']].to_csv('FIX_Warehouse_Audit.csv', index=False)

# 2. THE ACCOUNTING TASK LIST (Items they paid for but aren't in the building)
acct_action = df_merge[df_merge['match_type'] == 'In Accounting, Missing from WMS']
acct_action[['final_id', 'price_accounting', 'department']].to_csv('FIX_Accounting_Audit.csv', index=False)

print(f"\n✅ REMEDIATION FILES GENERATED:")
print(f"   - FIX_Warehouse_Audit.csv ({len(wms_action)} items to verify)")
print(f"   - FIX_Accounting_Audit.csv ({len(acct_action)} items to verify)")


