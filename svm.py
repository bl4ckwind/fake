from sklearn import svm
import numpy as np
import tools

def main():
    clf = train()
    data = [[0.08275862068965517, 0.1643835616438356, 0.08275862068965517, 0.16666666666666666, 0.011494252873563218, 0.041666666666666664, 1]]
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