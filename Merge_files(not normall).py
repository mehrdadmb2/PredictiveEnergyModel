import pandas as pd
import glob
import random
import os

# مسیر پوشه‌ای که فایل‌های اکسل روزانه در آن قرار دارند
folder_path = "I:\\IOT\\HW2\\For Me\\Data\\"
file_pattern = os.path.join(folder_path, "*.xlsx")

# لیست تمام فایل‌های اکسل در پوشه
all_files = glob.glob(file_pattern)

# خواندن و ترکیب فایل‌های اکسل
df_list = [pd.read_excel(file) for file in all_files]
combined_df = pd.concat(df_list, ignore_index=True)

# انتخاب ستون‌های مورد نظر: زمان، تاریخ، دما، رطوبت
combined_df = combined_df[["Time", "Date", "Temperature", "Humidity"]]

# اضافه کردن ستون مصرف برق با توجه به دما و رطوبت
combined_df["Power Consumption (kw)"] = combined_df.apply(
    lambda row: row["Temperature"] * 20 + row["Humidity"] * 10 + random.randint(0, 50), axis=1
)

# مسیر فایل خروجی
output_path = os.path.join(folder_path, "combined_output_with_power.xlsx")
combined_df.to_excel(output_path, index=False)

# input("Done\nEnter To Exit")