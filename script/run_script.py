from sys import path

home = "../../"
path.append(home)


import pandas as pd
import numpy as np

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

def run_all(analysis):
    analyzer = Analyzer(config_file)
    analyzer.set_analysis(analysis)
    analyzer.create_main_df()
    analyzer.filter_main()
    analyzer.split_data()
    analyzer.create_models()
    analyzer.run_models()
    analyzer.tune_models()
    return analyzer


if __name__ == "__main__":

    script_dir = home + "football/script/"
    config_file = script_dir + "analysis_config.json"
    data_dir = script_dir + "data/"

    passing_analyzer = run_all("passing")

    passing = pd.read_csv(data_dir + "passing.csv")
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


    receiving_analyzer = run_all("receiving")

    receiving = pd.read_csv(data_dir + "receiving.csv")
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

    rushing_analyzer = run_all("rushing")

    rushing = pd.read_csv(data_dir + "rushing.csv")
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

    models = ['support_vector_machine', 'random_forest_regressor', 'ridge']
    passing_fantasy_yds = passing_yds_predictions[models].div(25)
    receiving_fantasy_yds = receiving_yds_predictions[models].div(10)
    rushing_fantasy_yds = rushing_yds_predictions[models].div(10)

    passing_fantasy_td = passing_td_predictions[models].mul(4)
    receiving_fantasy_td = receiving_td_predictions[models].mul(6)
    rushing_fantasy_td = rushing_td_predictions[models].mul(6)

    receiving_fantasy_rec = receiving_rec_predictions[models]

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
    final_rank.to_csv(data_dir + "power_ranking.csv")