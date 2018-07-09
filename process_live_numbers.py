from sklearn.externals import joblib
import pandas as pd
import sys

# assert(len(sys.argv) > 1)
classes = joblib.load('live_numbers.pkl').iloc[1:]
# print(classes)
classes = classes.drop(['ID Slug', 'Product Sales ID', 'Class Name', 'Location: Location Name'], axis=1)
