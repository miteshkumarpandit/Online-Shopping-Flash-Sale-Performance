import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

np.random.seed(42)
date_range = pd.date_range(start="2023-11-24", periods=48, freq="H")  
data = {
    'timestamp': date_range,
    'orders': np.random.poisson(lam=20, size=48),
    'revenue': np.random.uniform(500, 1000, size=48),
    'offer_type': ['None'] * 48
}
df = pd.DataFrame(data)

df.loc[10:12, 'orders'] = [150, 180, 120]
df.loc[10:12, 'offer_type'] = 'BOGO'

df.loc[30:33, 'orders'] = [220, 250, 210, 100]
df.loc[30:33, 'offer_type'] = '50% Discount'

print("--- Summary Statistics: Global vs. Sale Periods ---")
summary = df.groupby('offer_type')[['orders', 'revenue']].agg(['mean', 'sum', 'max'])
print(summary)

plt.figure(figsize=(14, 6))
sns.set_style("whitegrid")

sns.lineplot(data=df, x='timestamp', y='orders', marker='o', label='Orders per Hour', color='teal')

for offer in df['offer_type'].unique():
    if offer != 'None':
        offer_data = df[df['offer_type'] == offer]
        plt.fill_between(offer_data['timestamp'], offer_data['orders'], alpha=0.3, label=f'Active: {offer}')

plt.title('Flash Sale Performance Analysis: Identifying Spikes', fontsize=15)
plt.xlabel('Time (Hourly)', fontsize=12)
plt.ylabel('Number of Orders', fontsize=12)
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

print("\n--- Offer Effectiveness Index (Average Lift) ---")
baseline_avg = df[df['offer_type'] == 'None']['orders'].mean()
effectiveness = df.groupby('offer_type')['orders'].mean() / baseline_avg
print(effectiveness.sort_values(ascending=False))