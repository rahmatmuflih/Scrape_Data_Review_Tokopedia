import pandas as pd

n = 5000

try:
    df = pd.read_csv('hasil\scrape_tokopedia.csv') 
    df = df[df['review'].notna()]
    df = df[df['user_id'] != 0]
    df.rename(columns = {'review': 'comment', 'product_id': 'item_id', 'user_id': 'userid'}, inplace=True)
    df.drop(['anonymous', 'author_username', 'id','nama_produk', 'rating'], axis=1, inplace=True)

    # df_copy = df.head(5000)
    df.drop(index=df.index[:n], inplace=True)
    print(df)

    df.to_csv('hasil\\scrape_tokopedia_clean.csv', index=False)
    print('\nData Telah Tersimpan')
except:
    print('Data Tidak Ditemukan')