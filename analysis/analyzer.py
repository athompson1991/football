import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from . import core

import json
import warnings

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV

from sklearn.linear_model import Ridge

from .core import plot_learning_curve
import warnings
import numpy as np

class Analyzer(object):

    def __init__(self, config_file):
        self.analysis = None
        self.analysis_config = None
        self.target_name = None
        self.features_names = None
        self.main = None
        self.target = None
        self.features = None
        self.hyper_tune = None
        self.models = {}
        self.tuned_models = {}

        self.train_test = {}

        warnings.simplefilter(action='ignore', category=FutureWarning)
        warnings.simplefilter(action='ignore', category=DeprecationWarning)
        warnings.simplefilter(action='ignore', category=UserWarning)

        with open(config_file) as config_file:
            self.config = json.load(config_file)

    def set_analysis(self, analysis):
        code = analysis + "_analysis"
        self.analysis = analysis
        self.analysis_config = self.config[code]
        self.target_name = self.analysis_config["target"]
        self.features_names = self.analysis_config["features"]
        self.print_summary_analysis()

    def print_summary_analysis(self):
        features_string = ", ".join(self.features_names)
        print("Analysis: " + self.analysis)
        print("Target: " + self.target_name)
        print("Features: " + features_string)

    def create_main_df(self):
        if self.main is None:
            self.main = core.make_main_df(self.config['home_dir'] + self.analysis_config["main_df"])
        self.target = self.main[self.target_name]
        self.features = self.main[self.features_names]
        self.print_main_size()

    def create_plots(self):
        plot_config = self.analysis_config["plots"]
        for plot in plot_config.keys():
            if "scatter" in plot:
                specs = plot_config[plot]
                core.scatter_plot(
                    self.main,
                    specs["x"],
                    specs["y"],
                    labels_dict=specs["labels"],
                    output=self.config["home_dir"] + specs["output_dir"]
                )

    def split_data(self):
        features_train, features_test, target_train, target_test = train_test_split(
            self.features,
            self.target,
            test_size=0.2,
            random_state=42
        )
        self.train_test['train'] = {'target': target_train, 'features': features_train}
        self.train_test['test'] = {'target': target_test, 'features': features_test}

    def filter_main(self):
        filters = self.analysis_config['filters']
        for filter in filters:
            logic_string = str(filter[0]) + " " + str(filter[1]) + " " + str(filter[2])
            self.main = self.main.query(logic_string)
            print("After logic: " + logic_string)
            self.print_main_size()
        self.create_main_df()

    def print_main_size(self):
        size_strings = (str(self.main.shape[0]), str(self.main.shape[1]))
        print_string = "Main DataFrame shape: " + size_strings[0] + " Rows, " + size_strings[1] + " Columns"
        print(print_string)

    def set_target(self, target):
        self.target_name = target
        self.print_summary_analysis()
        self.create_main_df()
        self.split_data()
        self.models = {}
        self.tuned_models = {}

    def create_model(self, model):
        model_data = self.analysis_config['models'][model]
        pipe_names = [pipe for pipe in model_data['pipeline'].keys()]
        pipe_objs = [eval(model_data['pipeline'][pipe])() for pipe in pipe_names]
        pipeline_arg = list(zip(pipe_names, pipe_objs))
        self.model = Pipeline(pipeline_arg)

    def create_models(self):
        models_data = self.analysis_config['models']
        model_names = models_data.keys()
        for model in model_names:
            print("Initializing: " + model)
            model_spec = models_data[model]
            pipe_names = [pipe for pipe in model_spec['pipeline'].keys()]
            pipes = [eval(model_spec['pipeline'][pipe])() for pipe in pipe_names]
            pipeline_arg = list(zip(pipe_names, pipes))
            self.models[model] = Pipeline(pipeline_arg)

    def run_model(self, model):
        print("Fitting: " + model)
        self.models[model].fit(self.features, self.target)

    def run_models(self):
        for model in self.models.keys():
            self.run_model(model)

    def cross_val_predict(self):
        self.predictions = cross_val_predict(
            self.model,
            self.train_test['train']['features'],
            self.train_test['train']['target'],
            cv=10
        )
        score = np.sqrt(mean_squared_error(self.predictions, self.train_test['train']['target']))
        print("SVR MSE: " + str(score))

    def tune_model(self, model):
        print("Tuning model: " + model)
        hypertune_params = self.analysis_config['hypertune_params']
        param_grid = self.analysis_config['models'][model]['search_params']
        search_class = eval(hypertune_params['search_class'])
        self.tuned_models[model] = search_class(
            estimator=self.models[model],
            param_distributions=param_grid,
            cv=hypertune_params['cv'],
            scoring=hypertune_params['scoring']
        )
        print("Search class created, fitting model now...")
        self.tuned_models[model].fit(
            self.train_test['train']['features'],
            self.train_test['train']['target']
        )

    def tune_models(self):
        for model in self.models.keys():
            self.tune_model(model)

    def plot_learning_curve(self, model, filename, tuned=False):
        if tuned:
            plot_model = self.tuned_models[model].best_estimator_
        else:
            plot_model = self.models[model]
        plot_learning_curve(
            plot_model,
            self.train_test['train']['features'],
            self.train_test['train']['target'],
            output=self.config['home_dir'] + self.analysis_config['plots']['output_dir'] + filename
        )

    def predict_model(self, model, features):
        return self.models[model].predict(features)

    def predict_models(self, features):
        predictions = {}
        for model in self.models.keys():
            predictions[model] = self.predict_model(model, features)
        predictions_df = pd.DataFrame.from_dict(predictions)
        return predictions_df

    def predict_tuned_model(self, model, features):
        return self.tuned_models[model].best_estimator_.predict(features)

    def predict_tuned_models(self, features):
        predictions = {}
        for model in self.models.keys():
            predictions[model] = self.predict_tuned_model(model, features)
        predictions_df = pd.DataFrame.from_dict(predictions)
        return predictions_df
