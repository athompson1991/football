from football.analysis import core
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

from football.analysis.core import plot_learning_curve
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

        self.train_test = {}

        warnings.simplefilter(action='ignore', category=FutureWarning)

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

    def create_model(self, model):
        model_data = self.analysis_config['models'][model]
        pipe_names = [pipe for pipe in model_data['pipeline'].keys()]
        pipe_objs = [eval(model_data['pipeline'][pipe])() for pipe in pipe_names]
        pipeline_arg = list(zip(pipe_names, pipe_objs))
        self.model = Pipeline(pipeline_arg)

    def run_model(self):
        self.model.fit(self.features, self.target)

    def cross_val_predict(self):
        self.predictions = cross_val_predict(
            self.model,
            self.train_test['train']['features'],
            self.train_test['train']['target'],
            cv=10
        )
        score = np.sqrt(mean_squared_error(self.predictions, self.train_test['train']['target']))
        print("SVR MSE: " + str(score))

    def tune_parameters(self, model):
        hypertune_params = self.analysis_config['hypertune_params']
        param_grid = self.analysis_config['models'][model]['search_params']
        search_class = eval(hypertune_params['search_class'])
        self.hyper_tune = search_class(
            estimator=self.model,
            param_distributions=param_grid,
            cv=hypertune_params['cv'],
            scoring=hypertune_params['scoring']
        )
        print("Search class created, fitting model now...")
        self.hyper_tune.fit(
            self.train_test['train']['features'],
            self.train_test['train']['target']
        )

    def plot_learning_curve(self, filename, tuned=False):
        if tuned:
            plot_model = self.hyper_tune.best_estimator_
        else:
            plot_model = self.model
        plot_learning_curve(
            plot_model,
            self.train_test['train']['features'],
            self.train_test['train']['target'],
            output=self.config['home_dir'] + self.analysis_config['plots']['output_dir'] + filename
        )

    def predict(self, features, tuned=False):
        if tuned:
            return self.hyper_tune.best_estimator_.predict(features)
        else:
            return self.model.predict(features)


