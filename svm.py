from sklearn import svm
import numpy as np
import tools

def main():
    clf = train()
    data = [[0.1264, 1.0, 0.0032, 0.0, 0.009933774834437087, 0.0, 0]]
    test(clf, data)

def train():
    training = tools.csv_reader("CSV/train.csv")
    y = [t[0] for t in training]
    X = np.array([t[1:] for t in training])
    clf = svm.SVC(kernel='linear', C=1.0)
    clf.fit(X,y)

    return clf
    

def test(clf, testdata):
    for test in testdata:
        print(clf.predict(np.array(test).reshape(1, -1)))


if __name__ == '__main__':
    main()