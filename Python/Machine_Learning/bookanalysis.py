import pandas as pd
import numpy as np
import re

book_ratings = pd.read_csv('book_rental_datasets/book_ratings.csv')
# print(book_ratings.head())

n_users = book_ratings.user_id.unique().shape[0]
n_items = book_ratings.isbn.unique().shape[0]
n_items = book_ratings['isbn'].max()
n_items = re.sub('[^0-9]', '', n_items)
n_items = int(n_items)
A = np.zeros((n_users,n_items))
for line in book_ratings.itertuples():
    A[line[1]-1,line[2]-1] = line[3]
print("Original rating matrix : ",A)
