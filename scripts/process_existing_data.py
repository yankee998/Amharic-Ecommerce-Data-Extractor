import pandas as pd
import os

# Load telegram_data.xls
df = pd.read_excel('output/data/telegram_data.xlsx')

# Ensure consistent columns
expected_columns = ['channel', 'message_id', 'date', 'text', 'views', 'sender_id', 'photo_path']
for col in expected_columns:
    if col not in df.columns:
        df[col] = None

# Save to CSV
os.makedirs('output/processed', exist_ok=True)
df.to_csv('output/processed/existing_telegram_data.csv', index=False, encoding='utf-8')
print("Existing data saved to output/processed/existing_telegram_data.csv")