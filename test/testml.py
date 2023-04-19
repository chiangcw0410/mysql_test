# The data set used in this example is from http://archive.ics.uci.edu/ml/datasets/Wine+Quality
# P. Cortez, A. Cerdeira, F. Almeida, T. Matos and J. Reis.
# Modeling wine preferences by data mining from physicochemical properties. In Decision Support Systems, Elsevier, 47(4):547-553, 2009.
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet
import mlflow
import mlflow.sklearn
def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2
    
alphas = [0.5, 0.7, 0.9]
l1_ratios = [0.3, 0.5, 0.9]
np.random.seed(40)
# Read the wine-quality csv file from the URL
csv_url ='http://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv'
try:
    data = pd.read_csv(csv_url, sep=';')
except Exception as e:
    print("Unable to download training & test CSV, check your internet connection. Error: %s", e)
# Split the data into training and test sets. (0.75, 0.25) split.
train, test = train_test_split(data)
# The predicted column is "quality" which is a scalar from [3, 9]
train_x = train.drop(["quality"], axis=1)
test_x = test.drop(["quality"], axis=1)
train_y = train[["quality"]]
test_y = test[["quality"]]
for alpha in alphas:
    for l1_ratio in l1_ratios:
        with mlflow.start_run():
            lr = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=42)
            lr.fit(train_x, train_y)
            predicted_qualities = lr.predict(test_x)
            (rmse, mae, r2) = eval_metrics(test_y, predicted_qualities)
            #mlflow.set_tracking_uri(<uri_of_remote_workspace>)
            mlflow.set_experiment("path to experiment in remote workspace")