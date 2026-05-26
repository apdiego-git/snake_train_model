import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import numpy as np

connection  = sqlite3.connect("snake_info.db")

query = """
SELECT * FROM snake_info
ORDER BY attempt ASC 
LIMIT 5000;
"""

df = pd.read_sql_query(query, connection)

connection.close()
df = df.iloc[::50]
plt.scatter(df['attempt'], df['length'], color='blue', s=10)

x = df['attempt']
y = df['length']


slope_and_intercept = np.polyfit(x, y, 1) 
trend_formula = np.poly1d(slope_and_intercept)
plt.plot(x, trend_formula(x), color='red', linewidth=2, label='Trend Line')

rolling_avg = df['length'].rolling(window=100, min_periods=1).mean()


plt.title('Snake Agent Progression')
plt.xlabel('Attempt')
plt.ylabel('Length')
plt.grid(True)

plt.savefig('learning_curve.png')