from numpy import mean
from time import time

from sklearn import tree, neighbors
from sklearn.datasets import load_svmlight_file
from sklearn.ensemble import AdaBoostClassifier,  RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import cross_val_score


test_split = .5

class Classifier:
    def __init__(self, name, all_data):
        self.clf = None
        self.name = name
        self.data, self.target, self.test_data, self.test_target = all_data
        self.predictions = []

        self.clf = self.build_classifier()


    def build_classifier(self):
        """Build and fit a classifier based on the name and predict one value"""
        if self.name == "DecisionTree":
            clf = tree.DecisionTreeClassifier()

        elif self.name == "KNeighbors":
            clf = neighbors.KNeighborsClassifier(5)

        elif self.name == "ADABoost":
            clf = AdaBoostClassifier(n_estimators=35)

        elif self.name == "MultilayerPerceptron":
            clf = MLPClassifier(solver='lbfgs',
                                     alpha=1e-5,
                                     hidden_layer_sizes=(5,2),
                                     random_state=1)

        elif self.name == "RandomForest":
            clf = RandomForestClassifier(n_estimators=10,
                                              max_depth=None,
                                              min_samples_split=2,
                                              random_state=0)
        return clf

    def fit(self):
        self.clf= self.clf.fit(self.data, self.target)

    def make_all_predictions(self):
        # Make predictions:
        for i in self.test_data:
            self.predictions.append(self.clf.predict(i))


    def make_one_prediction(self):
        print("\t|\n\t|\tprediction:", self.clf.predict(self.test_data[0]))
        print("\t|\ttarget:", self.test_target[0])

    def confusion(self):
        return confusion_matrix(self.test_target, self.predictions)

    def class_report(self):
        return classification_report(self.test_target, self.predictions)

    def cross_val(self):
        return cross_val_score(self.clf, self.data, self.target, cv=5)



def get_data():
    """Load the data from the file and split it based on the test_split"""
    print("Loading data...")
    data, target = load_svmlight_file("sensorReadings24.libsvm")
    print("Data Loaded")

    test_data = data[:int(data.shape[0] * test_split)]
    test_target = target[:int(target.shape[0] * test_split)]

    return data, target, test_data, test_target

if __name__ == '__main__':
    all_data = get_data()
    classifiers = ["DecisionTree", "KNeighbors", "ADABoost", "MultilayerPerceptron", "RandomForest"]
    print("Building and testing", len(classifiers), "classifiers...")

    for n in classifiers:
        string = "_" * 9 + n
        string += "_" * (36 - len(string) + 1)
        print("\t" + string)
        s_time = time()

        clf = Classifier(n, all_data)
        clf.fit()
        t_time = time() - s_time
        print("Runtime:", t_time)

        clf.make_all_predictions()

        print("Confusion:\n", clf.confusion())
        print("\nClassification Report:\n", clf.class_report())

        cv = clf.cross_val()
        print("\nCross Val Scores:",cv, "mean:", mean(cv))

        print("\n\t_"+36*"_"+"\n")
