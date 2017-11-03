from __future__ import division
import csv, math, random
class K_Means:
    filename = 'accident.csv'
    MAX_ITERATIONS = 100
    ATTRIBUTES = -1
    TUPLES = -1
    FOLD_LENGTH = -1
    feature_set = []
    data = []
    testing_data = []
    actual_output = []
    offset = 0.1 
    FOLDS = 1
    ACCURACY = 0.0
    K = 5
    true_positives = 0
    true_negatives = 0
    false_positives = 0
    false_negatives = 0

    def __init__(self):
        print("K_Means")
        self.data = []

    def loadDataSet(self):
        tuples = 0
        flag = False
        with open(self.filename, 'rt') as f:
            reader = csv.reader(f)
            for row in reader:
                if flag == False:
                    if not row[0].isdigit():
                        flag = True
                        continue
                tuples += 1
                self.data.append(row)
        self.setParameters(tuples)

        self.formatDataSet()

    def setParameters(self, tuples):
        self.TUPLES = tuples
        self.ATTRIBUTES = len(self.data[0]) - 1
        self.FOLD_LENGTH = math.ceil(self.offset * self.TUPLES)

    def formatDataSet(self):
        for i in range(len(self.data)):
            if self.data[i][-1] == 'Yes' or self.data[i][-1] == '1':
                self.data[i][-1] = 1
            elif self.data[i][-1] == 'No' or self.data[i][-1] == '0':
                self.data[i][-1] = 0

            self.data[i][:-1] = [float(x) for x in self.data[i][:-1]] 

    def findDistance(self, x, y):
        return math.sqrt(sum([(i-j)**2 for i,j in zip(x,y)]))

    def findMean(self, a):
        rows = len(a)
        cols = len(a[0])
        column_sums = [sum(row[i] for row in a) for i in range(0, cols)]
        mean_values = [i/rows for i in column_sums]
        return mean_values

    def terminate(self, oldCentroids, newCentroids):
        if not newCentroids:
            return False
        for i in range(0, len(newCentroids)):
            if oldCentroids[i] != newCentroids[i]:
                return False
        return True

    def trainModel(self):
        iterations = 1
        oldCentroids = []
        newCentroids = []
        randoms = [random.randrange(0, self.TUPLES) for i in range(0, self.K)]
        oldCentroids.extend([self.data[i] for i in randoms])

        while iterations <= self.MAX_ITERATIONS and not self.terminate(oldCentroids, newCentroids):
            if iterations != 1:
                oldCentroids = newCentroids
            iterations += 1
            clusters = {}
            for row in range(0, len(self.data)):
                distance = []
                for i in range(0, self.K):
                    dist = self.findDistance(self.data[row][:-1], oldCentroids[i])
                    distance.append(dist)
                c = distance.index(min(distance))
                if c not in clusters:
                    clusters[c] = []
                clusters[c].append(row)
            newCentroids=[]
            for cluster in clusters:
                a = []
                for i in clusters[cluster]:
                    a.append(self.data[i][:-1])

                newCentroids.append(self.findMean(a))

        self.display(clusters, newCentroids, iterations)
        self.predict(clusters)

    def display(self, clusters, newCentroids, iterations):
        print "Number of iterations :", iterations
        print "Centroids :"
        print "\t        Cluster 0\t        Cluster 1"
        for i in range(0, len(newCentroids[0])):
            print "Attr", i+1, "        ", newCentroids[0][i], "        ", newCentroids[1][i]

        print "\nClustered Intances :"
        print "0 : ", len(clusters[0])
        print "1 : ", len(clusters[1])

    def predict(self, clusters):
        for row in clusters[0]:
            if self.data[row][-1] == 0:
                self.true_negatives += 1
            elif self.data[row][-1] == 1:
                self.false_negatives += 1

        for row in clusters[1]:
            if self.data[row][-1] == 1:
                self.true_positives += 1
            elif self.data[row][-1] == 0:
                self.false_positives += 1

        print "\nCluster 1 : No , Cluster 2 : Yes"
        accuracy = self.findAccuracy()
        print "ACCCURACY = %s %%\n" %accuracy

        self.true_positives = 0
        self.true_negatives = 0
        self.false_positives = 0
        self.false_negatives = 0
        # 'first_cluster' : 1 'second_cluster' : 0
        for row in clusters[0]:
            if self.data[row][-1] == 1:
                self.true_positives += 1
            elif self.data[row][-1] == 0:
                self.false_positives += 1

        for row in clusters[1]:
            if self.data[row][-1] == 0:
                self.true_negatives += 1
            elif self.data[row][-1] == 1:
                self.false_negatives += 1

        print "\nCluster 1 : Yes , Cluster 2 : No"
        accuracy = self.findAccuracy()
        print "ACCCURACY = %s %%\n" %accuracy

    def findAccuracy(self):
        print("tp:%s fp:%s tn:%s fn:%s" %(self.true_positives, self.false_positives, self.true_negatives, self.false_negatives))
        precision_positive = -1.0
        recall_positive = -1.0
        if self.true_positives + self.false_positives != 0.0:
            precision_positive = self.true_positives / (self.true_positives + self.false_positives)
        if self.true_positives + self.false_negatives != 0.0:
            recall_positive = self.true_positives / (self.true_positives + self.false_negatives)
        print("Positive_Precision = %s  Positive_Recall = %s" %(precision_positive, recall_positive))
        precision_negative = -1.0
        recall_negative = -1.0
        if self.true_negatives + self.false_negatives != 0.0:
            precision_negative = self.true_negatives / (self.true_negatives + self.false_negatives)
        if self.false_positives + self.true_negatives != 0.0:
            recall_negative = self.true_negatives / (self.false_positives + self.true_negatives)
        print("Negative_Precision = %s  Negative_Recall = %s" %(precision_negative, recall_negative))
        return (self.true_positives + self.true_negatives) / (self.true_positives + self.false_positives + self.false_negatives + self.true_negatives) * 100

if __name__ == "__main__":
	model = K_Means()
	model.loadDataSet()
	model.trainModel()
