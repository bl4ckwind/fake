from sklearn import svm
import numpy as np
import tools

def main():
    clf = train()
    datasets = tools.csv_reader("CSV/test_Harry.csv")
    #print(datasets)
    for data in datasets:
        test(clf, data)

def train():
    training = tools.csv_reader("CSV/train2.csv")
    y = [t[0] for t in training]
    X = np.array([t[1:] for t in training])
    clf = svm.SVC(kernel='linear', C=1.0)
    clf.fit(X,y)

    return clf
    

def test(clf, testdata):
    print(clf.predict(np.array(testdata).reshape(1, -1)))


if __name__ == '__main__':
    main()