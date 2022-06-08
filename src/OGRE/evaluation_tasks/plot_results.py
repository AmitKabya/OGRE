"""
Create the plots, only when there are files of link prediction and node classification
"""
from .plots_utils import *
from .eval_utils import *

ONE_TEST_RATIO = 0.2


class PlotResults:

    def __init__(self, DATASET: dict, dataset_path: str, methods: list[str], initial_methods: list[str]):
        self.DATASET = DATASET
        self.dataset_path = dataset_path

        if self.DATASET["name"] != "Yelp":
            G = nx.read_edgelist(os.path.join(self.dataset_path, self.DATASET["name"] + ".txt"),
                                 create_using=nx.DiGraph(), delimiter=",")
            if G.number_of_nodes() == 0:
                G = nx.read_edgelist(os.path.join(self.dataset_path, self.DATASET["name"] + ".txt"),
                                     create_using=nx.DiGraph())
        else:
            with open(os.path.join(self.dataset_path, "yelp_data.p"), 'rb') as f:
                G = pickle.load(f)
            G = add_weights(G)
        self.number_of_nodes = G.number_of_nodes()

        list_keys = []
        # Our suggested embedding method
        methods_ = []
        for method in methods:
            if method in {"OGRE", "DOGRE", "WOGRE"}:
                methods_.append(method)
        # state-of-the-art embedding methods
        self.initial_methods_ = []
        for method in initial_methods:
            if method in {"node2vec", "GF", "HOPE", "GCN"}:
                self.initial_methods_.append(method)

        self.methods_mapping = {"OGRE": "OGRE", "DOGRE": "DOGRE", "WOGRE": "WOGRE"}
        for i in self.initial_methods_:
            for m in methods_:
                list_keys.append(i + " + " + m)
        self.keys_ours = list_keys
        self.keys_state_of_the_art = self.initial_methods_

        if not os.path.exists(os.path.join("plots")):
            os.makedirs(os.path.join("plots"))

        # colors to plot each method
        colors = ["indigo", "red", "olivedrab"]

        self.mapping = {}
        all_keys = self.keys_ours + self.keys_state_of_the_art
        for key in all_keys:
            if "node2vec" in key:
                self.mapping.update({key: colors[0]})
            elif "HOPE" in key:
                self.mapping.update({key: colors[1]})
            else:
                self.mapping.update({key: colors[2]})

    def plot_run_time(self):
        """
        Plot Running Time
        """

        # read times
        dict_times = read_times_file(self.DATASET["name"], "files_degrees", self.initial_methods_, self.methods_mapping)

        plot_running_time_after_run_all(self.DATASET, dict_times, self.mapping, self.number_of_nodes, 0)

    def __pre_lp_nc(self):
        dict_lp, _, initial_size, _, _ = read_results(self.DATASET["name"], "files_degrees", "Link Prediction",
                                                      self.initial_methods_, 0.2, self.methods_mapping)
        new_initial = []
        for i in initial_size:
            new_initial.append(i)
        new_initial.append(self.number_of_nodes)
        return dict_lp, initial_size, new_initial

    def plot_link_prediction(self, params_lp_dict: dict):
        """
        Link Prediction
        """

        num1 = 170
        num2 = 10
        save = "plots"

        dict_lp, initial_size, new_initial = self.__pre_lp_nc()

        self.DATASET["initial_embedding_size"] = initial_size

        plot_test_vs_score_all(self.DATASET["name"], "Link Prediction", dict_lp, self.keys_ours,
                               self.keys_state_of_the_art, params_lp_dict["test_ratio"],
                               self.DATASET["initial_embedding_size"], self.mapping, num2, save)

        plot_initial_vs_score_all(self.DATASET["name"], "Link Prediction", dict_lp, self.keys_ours,
                                  self.keys_state_of_the_art,
                                  self.DATASET["initial_embedding_size"], ONE_TEST_RATIO, params_lp_dict["test_ratio"],
                                  new_initial, self.mapping, num1, save)

    def plot_node_classification(self, params_nc_dict: dict):
        """
        Node Classification
        """

        num1 = 180
        num2 = 30
        save = "plots"
        dict_nc = read_results(self.DATASET["name"], "files_degrees", "Node Classification", self.initial_methods_, 0.2,
                               self.methods_mapping)
        _, initial_size, new_initial = self.__pre_lp_nc()

        plot_test_vs_score_all(self.DATASET["name"], "Node Classification", dict_nc, self.keys_ours,
                               self.keys_state_of_the_art,
                               params_nc_dict["test_ratio"],
                               self.DATASET["initial_embedding_size"], self.mapping, num2, save)

        plot_initial_vs_score_all(self.DATASET["name"], "Node Classification", dict_nc,
                                  self.keys_ours, self.keys_state_of_the_art,
                                  self.DATASET["initial_embedding_size"], ONE_TEST_RATIO,
                                  params_nc_dict["test_ratio"], new_initial, self.mapping, num1, save)
