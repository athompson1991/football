import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from football.analysis.analyzer import Analyzer

def predict_from_raw(main, analyzer):
    df = main.copy()
    df.columns = [col + "_prev" for col in df.columns]
    features = df[analyzer.features_names]
    predictions = analyzer.predict_tuned_models(features)
    names = df["player_prev"]
    names.index = range(len(names))
    predictions['name'] = names
    return predictions


home = "/Users/alex/google_drive/python_projects/football/football/"


passing_analyzer = Analyzer(home + "analysis/analysis_config.json")
passing_analyzer.set_analysis("passing")
passing_analyzer.create_main_df()
passing_analyzer.filter_main()
passing_analyzer.split_data()
passing_analyzer.create_models()
passing_analyzer.run_models()
passing_analyzer.tune_models()

passing = pd.read_csv(home + "data/passing.csv")
passing_2018 = passing[passing['season'] == 2018]
passing_2018 = passing_2018[passing_2018['pos'] == 'QB']
passing_2018 = passing_2018[passing_2018['pass_att'] >= 10]
passing_2018 = passing_2018[passing_2018['pass_att'] >= 10]

passing_td_predictions = predict_from_raw(passing_2018, passing_analyzer)

passing_analyzer.set_target("pass_yds_now")
passing_analyzer.create_models()
passing_analyzer.run_models()
passing_analyzer.tune_models()

passing_yds_predictions = predict_from_raw(passing_2018, passing_analyzer)


receiving_analyzer = Analyzer(home + "analysis/analysis_config.json")
receiving_analyzer.set_analysis("receiving")
receiving_analyzer.create_main_df()
receiving_analyzer.filter_main()
receiving_analyzer.split_data()
receiving_analyzer.create_models()
receiving_analyzer.run_models()
receiving_analyzer.tune_models()

receiving = pd.read_csv(home + "data/receiving.csv")
receiving_2018 = receiving[receiving['season'] == 2018]
receiving_2018 = receiving_2018[receiving_2018['pos'] == 'WR']
receiving_2018 = receiving_2018[receiving_2018['gs'] >= 8]
receiving_2018 = receiving_2018[receiving_2018['rec'] >= 10]

receiving_td_predictions = predict_from_raw(receiving_2018, receiving_analyzer)

receiving_analyzer.set_target("rec_yds_now")
receiving_analyzer.create_models()
receiving_analyzer.run_models()
receiving_analyzer.tune_models()

receiving_yds_predictions = predict_from_raw(receiving_2018, receiving_analyzer)

receiving_analyzer.set_target("rec_now")
receiving_analyzer.create_models()
receiving_analyzer.run_models()
receiving_analyzer.tune_models()

receiving_rec_predictions = predict_from_raw(receiving_2018, receiving_analyzer)

rushing_analyzer = Analyzer(home + "analysis/analysis_config.json")
rushing_analyzer.set_analysis("rushing")
rushing_analyzer.create_main_df()
rushing_analyzer.filter_main()
rushing_analyzer.split_data()
rushing_analyzer.create_models()
rushing_analyzer.run_models()
rushing_analyzer.tune_models()

rushing = pd.read_csv(home + "data/rushing.csv")
rushing_2018 = rushing[rushing['season'] == 2018]
rushing_2018 = rushing_2018[rushing_2018['pos'] == 'RB']
rushing_2018 = rushing_2018[rushing_2018['gs'] >= 8]
rushing_2018 = rushing_2018[rushing_2018['rush_att'] >= 100]

rushing_td_predictions = predict_from_raw(rushing_2018, rushing_analyzer)

rushing_analyzer.set_target("rush_yds_now")
rushing_analyzer.create_models()
rushing_analyzer.run_models()
rushing_analyzer.tune_models()

rushing_yds_predictions = predict_from_raw(rushing_2018, rushing_analyzer)


kicking = pd.read_csv(home + "data/kicking.csv")
kicking_2018 = kicking[kicking['season'] == 2018]
kicking_2018 = kicking_2018[kicking_2018['pos'] == 'K']
kicking_2018 = kicking_2018[kicking_2018['fgm'] >= 10]

kicking_analyzer = Analyzer(home + "analysis/analysis_config.json")
kicking_analyzer.set_analysis("kicking")
kicking_analyzer.create_main_df()
kicking_analyzer.main = kicking_analyzer.main.fillna(0)
kicking_analyzer.filter_main()
kicking_analyzer.split_data()
kicking_analyzer.create_models()
kicking_analyzer.run_models()
kicking_analyzer.tune_models()

kicking_predictions = predict_from_raw(kicking_2018, kicking_analyzer)

models = ['support_vector_machine', 'random_forest_regressor', 'ridge']
passing_fantasy_yds = passing_yds_predictions[models].div(25)
receiving_fantasy_yds = receiving_yds_predictions[models].div(10)
rushing_fantasy_yds = rushing_yds_predictions[models].div(10)

passing_fantasy_td = passing_td_predictions[models].mul(4)
receiving_fantasy_td = receiving_td_predictions[models].mul(6)
rushing_fantasy_td = rushing_td_predictions[models].mul(6)

receiving_fantasy_rec = receiving_rec_predictions[models]


def get_ranking(yds, td, main_df, rec=None):
    vote_yds = yds.apply(np.mean, axis=1)
    vote_yds.index = main_df['player_code']
    vote_td = td.apply(np.mean, axis=1)
    vote_td.index = main_df['player_code']
    if rec is not None:
        vote_rec = rec.apply(np.mean, axis=1)
        vote_rec.index = main_df['player_code']
        vote = vote_yds + vote_td + vote_rec
    else:
        vote = vote_yds + vote_td
    return vote

qb_rank = get_ranking(passing_fantasy_yds, passing_fantasy_td, passing_2018)
wr_rank = get_ranking(receiving_fantasy_yds, receiving_fantasy_td, receiving_2018, receiving_fantasy_rec)
rb_rank = get_ranking(rushing_fantasy_yds, rushing_fantasy_td, rushing_2018)

pos = np.concatenate([np.repeat('QB', qb_rank.size), np.repeat('WR', wr_rank.size), np.repeat('RB', rb_rank.size)])
points = np.concatenate([qb_rank, wr_rank, rb_rank])
codes = np.concatenate([qb_rank.index, wr_rank.index, rb_rank.index])
names = np.concatenate([passing_2018['player'], receiving_2018['player'], rushing_2018['player']])

final_rank = pd.DataFrame.from_dict({'points': points, 'position': pos, 'player': names})
final_rank.index = codes
final_rank = final_rank.sort_values('points', ascending=False)
final_rank.to_csv(home + "data/power_ranking.csv")