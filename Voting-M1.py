import numpy as np
import matplotlib.pyplot as plt
import math

##User Inputs##
#Number of candidates
candN = 10 #int(input("Number of candidates = "))
#Number of voters
voterN = 5000 #int(input("Number of voters = "))

##Random Candidate Distribution##
canddist = np.random.normal(5,1.5,size=(2,candN))
##Random Voter Distribution##
voterdist = np.random.normal(5,1.5,size=(2,voterN))
voter_proximity = [[0 for i in range(candN)] for j in range(voterN)]
ffpvote = [0 for i in range(voterN)]

##First Past The Post##
for i in range(voterN):
    for j in range(candN):
        voter_proximity[i][j] = math.dist(voterdist[:,i],canddist[:,j])
    ffpvote[i] = np.argmin(voter_proximity[i])

ffp = [0]*candN

for x in range(candN):
    ffp[x] = len([i for i in ffpvote if i==x])


##Instant Runoff##
canddistir = canddist
candir = [list(range(candN))] * candN
candNir = candN
irvotes = []
for h in range(candN-1):
    voter_proximity = [[0 for i in range(candNir)] for j in range(voterN)]
    for i in range(voterN):
        for j in range(candNir):
            voter_proximity[i][j] = math.dist(voterdist[:,i],canddistir[:,j])
        ffpvote[i] = np.argmin(voter_proximity[i])
    irsub = [0 for i in range(candNir)]
    for x in range(candNir):
        irsub[x] = len([i for i in ffpvote if i==x])
    irvotes.append(irsub)
    irindex = np.argmin(irvotes[h])
    canddistir = np.delete(canddistir,irindex,1)
    candNir = candNir-1
    candir[h+1]= np.delete(candir[h],irindex,0)

##Weighted Average##
voter_proximity = [[0 for i in range(candN)] for j in range(voterN)]
for i in range(voterN):
    for j in range(candN):
        voter_proximity[i][j] =  math.dist(voterdist[:,i],canddist[:,j])

for i in range(voterN):
    for j in range(candN):
        voter_proximity[i][np.argmin(voter_proximity[i])] = 100 * (j + 1)

weighted = [sum(col) for col in zip(*voter_proximity)]

##Plotting##
#Baseline Votes
fig = plt.figure(figsize = (10,5))
plt.bar(list(range(candN)),ffp,width = 0.7)
plt.xlabel("Candidate")
plt.ylabel("Number of Votes")
plt.title("Voting Distribution")
plt.show

#Instant Runoff Results
fig = plt.figure(figsize = (10,5))
irlegend=[]
for x in range(len(irvotes)):
    plt.bar(candir[-(x+2)],irvotes[-(x+1)],width=0.7)
    irlegend.append("Round "+str(len(candir)-x-1))
plt.legend(irlegend)
plt.xlabel("Candidate")
plt.ylabel("Number of Votes")
plt.title("Instant Runoff Voting Distribution")
plt.show

#Weight Average Results
fig = plt.figure(figsize = (10,5))
plt.bar(list(range(candN)),weighted)
plt.bar(np.argmin(weighted),weighted[np.argmin(weighted)])
plt.xlabel("Candidate")
plt.ylabel("Proximity Score")
plt.title("Weighted Average Results")
plt.show

fig = plt.figure(figsize = (20,20))
for x in range(candN):
    plt.text(canddist[0,x],canddist[1,x],str(x), color="red", fontsize=30)
plt.scatter(voterdist[0],voterdist[1])
plt.xlim(0,10)
plt.ylim(0,10)
plt.grid()
plt.show
