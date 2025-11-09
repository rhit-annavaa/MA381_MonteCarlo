import random
from collections import Counter

#how many wins and losses a team starts with, ten calculate expected value of wins

TEAM_P = { # we can get the P for each team using Pythag Expectation
    "ATL": 0.60,
    "LAD": 0.58,
    "NYM": 0.52,
    "CHC": 0.51,
    "SDP": 0.53,
    # "TOR": random.betavariate(25, 31),
}

GAMES = 150 #games in a seson
TRIALS = 2000  # trial count

first_place = Counter() #to count first place finishes, it auto-adds a key if the jey doesnt exist yet 
win_sums = Counter() #same as above, but for wins
#we use counter here cuz it makes it easy to count things without initializing keys

#found most of this monte carlo sim online and will work on it 
for _ in range(TRIALS): #<- use _ to ignore loop var
    wins = {t: sum(1 for _ in range(GAMES) if random.random() < p) #simulate wins based on probability
            for t, p in TEAM_P.items()} #dict comprehension to create a dict of team wins
    # random tiebreaker for ties at the top
    top = max(wins.values()) #determine the team with max wins
    tied = [t for t, w in wins.items() if w == top] #list of teams that are tied for first
    first_place[random.choice(tied)] += 1 #randomly choose one of the tied teams to get first place credit
    for t, w in wins.items(): #add each teams wins to their total win count
        win_sums[t] += w #add wins to total

print("=== Chance to finish 1st ===")
for t in TEAM_P:
    print(f"{t}: {first_place[t]/TRIALS:.2%}")

print("\n=== Mean wins over trials ===")
for t in TEAM_P:
    print(f"{t}: {win_sums[t]/TRIALS:.1f}")
