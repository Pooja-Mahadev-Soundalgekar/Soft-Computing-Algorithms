import csv
import random
from kmodes import KModes

# read the data into a 2-dimensional array
z = []
with open('data/soybeans.csv','r') as f:
    reader = csv.reader(f,delimiter=',')
    z = list(reader)
        
c = KModes(z,4)
mindistance = 0
for i in range(1,8):
    oldclustervalues = c.clustervalues
    rand = random.randrange(c.numobjects)
    epoch = c.BuildInitialClusters(rand)
    if epoch[0] < mindistance or mindistance == 0:
        c.clustervalues = epoch[1]
        mindistance = epoch[0]
    else:
        c.clustervalues = oldclustervalues
    print("{}: Cost => {}".format(i, epoch[0]))

i = 0
moves = [1,0]
while moves[0] > 0:
    i += 1
    print("<{}> Rebuilding clusters...".format(i))
    moves = c.BuildClusters()
    print("{} moves that time ({} didn't move)...".format(moves[0],moves[1]-moves[0]))
    
# write the clusters to a csv file
print("Writing clusters to file...")
with open ('data/clusters.csv','w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    writer.writerows(c.clustervalues)
