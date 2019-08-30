import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from football.analysis.analyzer import Analyzer

from sklearn.model_selection import cross_val_predict

from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.impute import SimpleImputer

def impute_column(colname):
    imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
    imputed = imputer.fit_transform(np.array(analyzer.main[colname]).reshape(-1, 1))
    return imputed.reshape(-1)


imputer = SimpleImputer(missing_values=np.nan, strategy='mean')

home = "/Users/alex/google_drive/python_projects/football/football/"


analyzer = Analyzer(home + "analysis/analysis_config.json")
analyzer.set_analysis("passing")
analyzer.create_main_df()
analyzer.filter_main()
analyzer.split_data()
analyzer.create_model("ridge")
analyzer.run_model()
analyzer.create_plots()
analyzer.cross_val_predict()
analyzer.tune_parameters("ridge")
analyzer.plot_learning_curve('ridge.png')
analyzer.plot_learning_curve('tuned_svr.png', True)


def predict_from_raw(main, analyzer):
    main.columns = [col + "_prev" for col in main.columns]
    predictions = analyzer.predict(main[analyzer.features_names], True)
    names = main["player_prev"]
    names.index = range(len(names))
    predictions = pd.Series(predictions)
    ranks = pd.concat({"name": names, "predict": predictions}, axis=1)
    ranks = ranks.sort_values(by=['predict'], ascending=False)
    print(ranks)
    return ranks


passing = pd.read_csv(home + "data/passing.csv")
passing_2018 = passing[passing['season'] == 2018]
passing_2018 = passing_2018[passing_2018['pos'] == 'QB']
passing_2018 = passing_2018[passing_2018['pass_att'] >= 10]
passing_2018 = passing_2018[passing_2018['pass_att'] >= 10]

predict_from_raw(passing_2018)

main_df_2018.columns = [col + "_prev" for col in main_df_2018.columns]
predictions = analyzer.predict(main_df_2018[analyzer.features_names], True)
names = main_df_2018["player_prev"]
names.index = range(len(names))
predictions = pd.Series(predictions)
ranks = pd.concat({"name": names, "predict": predictions}, axis=1)
ranks = ranks.sort_values(by=['predict'], ascending=False)
print(ranks)





main_2018 = main[main['season_now'] == 2018]
main_2018['y_hat'] = best_model.predict(main_2018[features_names])
main_2018['y_hat_rank'] = main_2018['y_hat'].rank()
main_2018[target_name + '_rank'] = main_2018[target_name].rank()
main_2018 = main_2018.sort_values(target_name + '_rank')
plt.scatter(main_2018[target_name + '_rank'], main_2018['y_hat_rank'])
