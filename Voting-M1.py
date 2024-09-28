import numpy as np
import matplotlib.pyplot as plt
from voter import *

##User Inputs##
#Number of candidates
candN = 10 #int(input("Number of candidates = "))
#Number of voters
voterN = 5000 #int(input("Number of voters = "))

##Random Candidate Distribution##
candidates = [Voter(c) for c in np.random.normal(5,1.5,(candN, 2))]

##Random Voter Distribution##
voters = [Voter(c) for c in np.random.normal(5,1.5,(voterN, 2))]

##First Past The Post##
ffp_vote = [v.pick_nearest(candidates) for v in voters] # How each voter voted
ffp_counts = [ffp_vote.count(i) for i in range(len(candidates))] # Votes per candidate

##Instant Runoff##
ir_pool = candidates.copy()
ir_vote = list() # How each voter voted, per round
ir_counts = list() # Votes per candidate, per round
while len(ir_pool) > 1 + ir_pool.count(None):
    ir_vote += [[v.pick_nearest(ir_pool) for v in voters]]
    ir_counts += [[ir_vote[-1].count(i) if ir_pool[i] else np.nan for i in range(len(ir_pool))]]
    ir_pool[np.nanargmin(ir_counts[-1])] = None

##Weighted Average##
tfer_func = lambda x: 1/x
weighted_vote = [[tfer_func(v.dist_to(c)) for c in candidates] for v in voters] # How each voter voted
# Normalize so each voter gets a total of 1 vote, split between candidates
weighted_vote_normed = [[v/sum(votelist) for v in votelist] for votelist in weighted_vote]
weighted_counts = [sum(l) for l in zip(*weighted_vote_normed)] # Sum of (fractional) votes per candidate

##Plotting##
#Baseline Votes
fig = plt.figure(figsize = (10,5))
plt.bar(list(range(candN)), ffp_counts, width=0.7)
plt.xlabel("Candidate")
plt.ylabel("Number of Votes")
plt.title("Voting Distribution")
plt.show()

#Instant Runoff Results
fig = plt.figure(figsize = (10,5))
bx = np.arange(len(candidates))
by = np.zeros(len(candidates))
for irc in ir_counts:
    plt.bar(bx, irc, bottom=by, width=0.7)
    by += [y if not np.isnan(y) else 0 for y in irc] # np.nan propogates in addition
plt.legend([f"Round {i}" for i in range(len(candidates))])
plt.xlabel("Candidate")
plt.ylabel("Number of Votes")
plt.title("Instant Runoff Voting Distribution")
plt.show()

#Weight Average Results
fig = plt.figure(figsize = (10,5))
plt.bar(list(range(candN)), weighted_counts)
# plt.bar(np.argmin(weighted_counts), weighted_counts[np.argmin(weighted_counts)]) ?
plt.xlabel("Candidate")
plt.ylabel("Proximity Score")
plt.title("Weighted Average Results")
plt.show()

fig = plt.figure(figsize = (20,20))
for idx, candidate in enumerate(candidates):
    plt.text(*candidate._p, str(idx), color="red", fontsize=30)
plt.scatter(*zip(*voters), c=ffp_vote)
plt.scatter(*zip(*candidates), c='red')
plt.xlim(0,10)
plt.ylim(0,10)
plt.grid()
plt.show()
