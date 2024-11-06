import pandas as pd
import glob
import random
import os
from sklearn.preprocessing import MinMaxScaler

# مسیر پوشه‌ای که فایل‌های اکسل روزانه در آن قرار دارند
folder_path = "I:\\IOT\\HW2\\For Me\\Data\\"
file_pattern = os.path.join(folder_path, "*.xlsx")

# لیست تمام فایل‌های اکسل در پوشه
all_files = glob.glob(file_pattern)

# خواندن و ترکیب فایل‌های اکسل
df_list = [pd.read_excel(file) for file in all_files]
combined_df = pd.concat(df_list, ignore_index=True)

# 1. بررسی داده‌های گمشده و نادرست
# حذف ردیف‌هایی که مقادیر گمشده دارند در ستون‌های خاص
combined_df.dropna(subset=["Temperature", "Humidity"], inplace=True)

# بررسی و حذف داده‌های نادرست (برای مثال، مقادیر غیرواقعی)
combined_df = combined_df[(combined_df["Temperature"] >= -50) & (combined_df["Temperature"] <= 50)]
combined_df = combined_df[(combined_df["Humidity"] >= 0) & (combined_df["Humidity"] <= 100)]

# 2. انتخاب ستون‌های مورد نظر: زمان، تاریخ، دما، رطوبت
combined_df = combined_df[["Time", "Date", "Temperature", "Humidity"]]

# بررسی اینکه آیا داده‌ها تهی نیستند
if combined_df.empty:
    print("Error: The data is empty after preprocessing.")
else:
    # 3. نرمال‌سازی داده‌ها
    # نرمال‌سازی دما و رطوبت بین 0 و 1
    scaler = MinMaxScaler()
    combined_df[["Temperature", "Humidity"]] = scaler.fit_transform(combined_df[["Temperature", "Humidity"]])

    # اضافه کردن ستون مصرف برق با توجه به دما و رطوبت
    combined_df["Power Consumption (kw)"] = combined_df.apply(
        lambda row: row["Temperature"] * 20 + row["Humidity"] * 10 + random.randint(0, 50), axis=1
    )

    # مسیر فایل خروجی
    output_path = os.path.join(folder_path, "combined_output_with_power_Normall.xlsx")
    combined_df.to_excel(output_path, index=False)

    print("Data processed and saved successfully.")

# input("Done\nEnter To Exit")
