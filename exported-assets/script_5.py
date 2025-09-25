# Let's examine the generated CSV files to show the parsed output
import pandas as pd
import os

print("Examining generated CSV files:")
print("=" * 50)

csv_files = ['oplogs/apache_access.csv', 'oplogs/nginx_access.csv', 'oplogs/syslog.csv', 'oplogs/custom_app.csv']

for csv_file in csv_files:
    if os.path.exists(csv_file):
        print(f"\n📄 {csv_file}:")
        print("-" * 40)
        df = pd.read_csv(csv_file)
        print(df.to_string(max_rows=5, max_cols=10))
        print(f"Columns: {list(df.columns)}")
        print(f"Rows: {len(df)}")
    else:
        print(f"❌ {csv_file} not found")

print(f"\n✅ Successfully parsed log files and generated CSV outputs!")