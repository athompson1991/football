import pandas as pd
import matplotlib.pyplot as plt

import numpy as np
from sklearn.model_selection import learning_curve


def make_main_df(filename):
    raw_data = pd.read_csv(filename)
    prev_season = raw_data.copy()
    prev_season['lookup'] = prev_season['season'] + 1
    main = pd.merge(
        raw_data,
        prev_season,
        left_on=['player_code', 'season'],
        right_on=['player_code', 'lookup'],
        suffixes=('_now', '_prev')
    )
    return main

def scatter_plot(main, x, y, labels_dict, output):
    plt.scatter(main[x], main[y], alpha=0.7)
    if 'xlab' in labels_dict.keys():
        plt.xlabel(labels_dict['xlab'])
    if 'ylab' in labels_dict.keys():
        plt.ylabel(labels_dict['ylab'])
    plt.title(labels_dict['title'], bbox={'facecolor': '0.8', 'pad': 5})
    plt.savefig(output)
    plt.close()

def plot_learning_curve(estimator, X, y, output, **kwargs):
    train_sizes, train_scores, test_scores = learning_curve(
        estimator, X, y,
        train_sizes=np.linspace(0.01, 1, 20),
        scoring='neg_mean_squared_error'
    )

    plt.plot(train_sizes, np.sqrt(-1 * np.mean(train_scores, axis=1)), label="In Sample")
    plt.plot(train_sizes, np.sqrt(-1 * np.mean(test_scores, axis=1)), label="Out of Sample")
    plt.legend(['in sample', 'out of sample'])
    plt.title(kwargs['title'])
    plt.xlabel("Sample Size")
    plt.show()
    plt.savefig(output)
    plt.close()

