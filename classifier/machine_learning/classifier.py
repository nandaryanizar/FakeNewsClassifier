import numpy as np
import pandas as pd
import warnings
import os.path
import logging
logging.basicConfig(filename="process.log", level=logging.INFO)

from sklearn import metrics
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from classifier.machine_learning.data_preprocessor import DataPrerocessor

news_labels = {1: "Satire", 2: "Hoax", 3: "Propaganda", 4: "Trusted"}

class Classifier:
    classifier = None
    model_path = None
    tfidf_path = None
    tfidf_vect_ngram = None

    def __init__(self, model, model_path, tfidf_path, learning_rate=5e-5, max_iters=1000, estimators=1000, rnd_state=42, add_intercept=True):
        try:
            model_path += ".pkl"
            tfidf_path += ".pkl"
            logging.info("Initializing classifier")
            if not model:
                raise Exception("Classifier model must be specified")

        
            if os.path.isfile(self.model_path):
                self.classifier = joblib.load(self.model_path)
            if os.path.isfile(self.tfidf_path):
                self.tfidf_vect_ngram = joblib.load(self.tfidf_path)

            if not self.classifier:
                if model.lower() == "logistic_regression":
                    self.classifier = LogisticRegression(max_iter=max_iters, fit_intercept=add_intercept, multi_class="multinomial", solver="newton-cg")
                elif model.lower() == "random_forest":
                    self.classifier = RandomForestClassifier(n_estimators=estimators, random_state=rnd_state)

            logging.info("Classifier created")
        except Exception as e:
            logging.exception(str(e))

    def train(self):
        try:
            logging.info("initializing classifier training")
            logging.info("Loading training and test data")
            train_data = pd.read_csv('newsfiles/fulltrain.csv', header=None)
            test_data = pd.read_csv('newsfiles/balancedtest.csv', header=None)

            logging.info("Splitting training and test label and text")
            train_X = train_data[1]
            train_Y = train_data[0]
            test_X = test_data[1]
            test_Y = test_data[0]

            logging.info("Creating TF-IDF N-gram vector")
            self.tfidf_vect_ngram, tfidf_ngram_train, tfidf_ngram_test = DataPrerocessor.generate_tfidf_ngrams(train_X, test_X, 100)

            logging.info("Training classifier")
            self.classifier.fit(tfidf_ngram_train, train_Y)
            
            logging.info("Get classifier accuracy")
            predictions = self.classifier.predict(tfidf_ngram_test)
            result = metrics.accuracy_score(predictions, test_Y)

            logging.info("Saving classifier")
            joblib.dump(self.classifier, self.model_path)
            joblib.dump(self.tfidf_vect_ngram, self.tfidf_path)

            logging.info("Finish training classifier")
            return result
        except Exception as e:
            logging.exception(str(e))

    def predict(self, X):
        try:
            if self.classifier == None or self.tfidf_vect_ngram == None:
                self.train()

            logging.info("Predicting")
            test_X = self.tfidf_vect_ngram.transform(X)

            result = self.classifier.predict(test_X)

            return news_labels[result[0]]
        except Exception as e:
            logging.exception(str(e))



def sigmoid(x):
    return 1 / (1 + np.exp(-x)) # Here we use np.exp() as exponential of Euler's

class Model:
    theta = None # theta attribute of the model
    accuracy = 0 # Accuracy of the trained model
    
    # Constructor of our model
    """
    initialize a few attributes for later use
    learning_rate = learning_rate, how should the model change every iteration
    max_iters = max iteration when training
    add_intercept = add intercept to the training and test dataset
    """
    def __init__(self, learning_rate=5e-5, max_iters=1000, add_intercept=True):
        self.learning_rate = learning_rate
        self.max_iters = max_iters
        self.add_intercept = add_intercept

    # Here's the train method
    """
    X = features
    y = class
    max_iter (optional) = maximum iteration we want
    """
    def train(self, X, y, maxIter=100000):
        new_X = X.copy() # Get copy of X
        logging.info("Training model...")

        # Initialize theta attribute with matrix containing 1
        # and make it ((features columns + 1) x 1) size
        self.theta = np.ones((new_X.shape[1] + 1, 1))

        if self.add_intercept:
            intercept = np.ones((len(new_X), 1)) # Create matrix containing intercept with (training rows x 1) size
            new_X = np.hstack((intercept, new_X)) # Concatenate the intercept with the new_X

        # Loop until reach maximum iteration count
        for i in range(maxIter):
            p = sigmoid(new_X.dot(self.theta)) # Create the probability matrix
            gradient = new_X.T.dot(y-p) # Compute the gradient
            self.theta -= self.learning_rate * gradient # Update our model weights

            logging.info("Iteration " + str(i) + " weights: {}".format(self.theta))

        # Indicate training completed and logging.info weight results
        logging.info("Training completed\n")
        logging.info("Weights: {}\n".format(self.theta))

    # Here's the predict method
    def predict(self, X):
        new_X = X.copy() # Get copy of X

        # Return warning if the trained features and the current features do not have the same size
        if not (new_X.shape[1]+1) == len(self.theta):
            return warnings.warn('The model trained with ' + str(len(self.theta)) + ' features')

        if self.add_intercept:
            intercept = np.ones((len(new_X), 1)) # Create matrix containing intercept with (training rows x 1) size
            new_X = np.hstack((intercept, new_X)) # Concatenate the intercept with the new_X
        
        predictions = np.hstack(np.round(sigmoid(new_X.dot(self.theta)))) # Predict the test dataset

        # Return as dataframe
        pred_dataframe = pd.DataFrame({'labels':predictions})
        return pred_dataframe


    def get_accuracy(self, predicted_Y, actual_Y):
        # Compute the accuracy
        predictions = np.hstack(predicted_Y.values)
        actual = np.hstack(actual_Y.values)
        
        return (predictions == actual).sum() / len(predictions)