import pandas as pd
import matplotlib.pyplot as plt
from sklearn.svm import SVR

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_predict, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV, learning_curve
from sklearn.ensemble import RandomForestRegressor

players = pd.read_csv("/Users/alex/google_drive/python_projects/football/football/data/players.csv")
prev_season = players.copy()
prev_season['lookup'] = prev_season['season'] + 1
prev_season

main = pd.merge(
    players,
    prev_season,
    left_on=['player_code', 'season'],
    right_on=['player_code', 'lookup'],
    suffixes=('_now', '_prev')
)

print('prior shape: ' + str(main.shape[0]))
main = main[main['pass_att_prev'] > 100]
main = main[main['pass_att_now'] > 100]
main = main[main['pos_prev'] == 'QB']
print('post shape: ' + str(main.shape[0]))

plt.scatter(main['pass_int_perc_prev'], main['pass_yds_now'], alpha=0.7)


target = main['pass_yds_now']
features = main[[
    'age_prev',
    'pass_cmp_prev',
    'pass_att_prev',
    'pass_cmp_perc_prev',
    'pass_yds_prev',
    'pass_yds_per_att_prev',
    'pass_adj_yds_per_att_prev',
    'pass_yds_per_cmp_prev',
    'pass_yds_per_g_prev',
    'pass_net_yds_per_att_prev',
    'pass_adj_net_yds_per_att_prev',
    'pass_td_prev',
    'pass_td_perc_prev',
    'pass_int_prev',
    'pass_int_perc_prev',
    'pass_sacked_yds_prev',
    'pass_sacked_prev'
]]


features_train, features_test, target_train, target_test = train_test_split(features, target, test_size=0.2, random_state=42)

svr_pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('polyfeatures', PolynomialFeatures()),
    ('svr', SVR())
])

svr_pipeline.fit(features_train, target_train)
predictions = cross_val_predict(
    svr_pipeline,
    features_train,
    target_train,
    cv=10
)

score = np.sqrt(mean_squared_error(predictions, target_train))
print("SVR MSE: " + str(score))

train_sizes, train_scores, test_scores = learning_curve(
    svr_pipeline,
    features_train,
    target_train,
    train_sizes=np.linspace(0.01, 1, 20),
    scoring='neg_mean_squared_error'
)

fig = plt.figure()
ax = plt.axes()
ax.plot(train_sizes, np.sqrt(-1 * np.mean(train_scores, axis=1)))
ax.plot(train_sizes, np.sqrt(-1 * np.mean(test_scores, axis=1)))

param_grid = [{
    'polyfeatures__degree': [1, 2, 3],
    'svr__epsilon': np.linspace(1, 1000, 10),
    'svr__kernel': ['linear', 'poly', 'sigmoid', 'rbf'],
    'svr__C': [0.1, 1, 10],
}]

grid_search = GridSearchCV(
    svr_pipeline,
    param_grid,
    cv=10,
    scoring='neg_mean_squared_error'
)

grid_search.fit(features_train, target_train)

best_model = grid_search.best_estimator_
predictions = cross_val_predict(
    best_model,
    features_train,
    target_train,
    cv=10
)
score = np.sqrt(mean_squared_error(predictions, target_train))
print('Grid Search SVR MSE: ' + str(score))


random_forest_pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('polyfeatures', PolynomialFeatures()),
    ('random_forest', RandomForestRegressor())
])

random_forest_pipeline.fit(features_train, target_train)
predictions = cross_val_predict(
    random_forest_pipeline,
    features_train,
    target_train,
    cv=10
)

score = np.sqrt(mean_squared_error(predictions, target_train))
print("Random Forest MSE: " + str(score))

param_grid = [{
    'polyfeatures__degree': [1, 2],
    'random_forest__max_depth': [2, 3, 5, None]
}]


grid_search = GridSearchCV(
    random_forest_pipeline,
    param_grid,
    cv=10,
    scoring='neg_mean_squared_error'
)

grid_search.fit(features_train, target_train)

best_model = grid_search.best_estimator_

predictions = cross_val_predict(
    best_model,
    features_train,
    target_train,
    cv=10
)
score = np.sqrt(mean_squared_error(predictions, target_train))
print("Random Forest Grid Search MSE: " + str(score))



train_sizes, train_scores, test_scores = learning_curve(
    best_model,
    features_train,
    target_train,
    train_sizes=np.linspace(0.01, 1, 20),
    scoring='neg_mean_squared_error'
)


fig = plt.figure()
ax = plt.axes()
ax.plot(train_sizes, np.sqrt(-1 * np.mean(train_scores, axis=1)))
ax.plot(train_sizes, np.sqrt(-1 * np.mean(test_scores, axis=1)))
