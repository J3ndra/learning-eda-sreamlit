import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

tourism_rating = pd.read_csv('tourism_rating.csv')
tourism_with_id = pd.read_csv('tourism_with_id.csv')
user = pd.read_csv('https://raw.githubusercontent.com/andhikappratamaa/indonesia-tourism-destination/main/Data/user.csv')

# Add new column
user["Age_group"] = user.Age.apply(lambda x: "Youth" if x <= 20 else "Adults")
tourism_with_id["Place_Status"] = tourism_with_id["Price"].apply(lambda x: "Paid" if x > 0 else "Free")

# Drop duplicate rows
tourism_rating[tourism_rating.duplicated(keep=False)]
tourism_rating.drop_duplicates(inplace=True)
print("Duplication data: ", tourism_rating.duplicated().sum())

# Remove unused columns
tourism_with_id = tourism_with_id.drop(["Time_Minutes","Unnamed: 11","Unnamed: 12","Description","Coordinate","Lat","Long"], axis =1)

# Save cleaned data
# Create directory if it does not exist
output_dir = 'cleaned_data'
os.makedirs(output_dir, exist_ok=True)

tourism_rating.to_csv(os.path.join(output_dir, 'tourism_rating_clean.csv'), index=False)
tourism_with_id.to_csv(os.path.join(output_dir, 'tourism_with_id_clean.csv'), index=False)
user.to_csv(os.path.join(output_dir, 'user_clean.csv'), index=False)