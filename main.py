from emoji_scapping import *

df = scraping_data()
df = normalize_data(df)
save(df)