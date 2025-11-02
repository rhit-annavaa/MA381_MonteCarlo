import random
from collections import Counter

TEAM_P = { # we can get the P for each team using Bayes Theorem 
    "ATL": 0.60,
    "LAD": 0.58,
    "NYM": 0.52,
    "CHC": 0.51,
    "SDP": 0.53,
}

GAMES = 150 #games in a seson
TRIALS = 2000  # trial count

first_place = Counter() #to count first place finishes, it auto-adds a key if the jey doesnt exist yet 
win_sums = Counter() #same as above, but for wins
#we use counter here cuz it makes it easy to count things without initializing keys

#found most of this monte carlo sim online and will work on it 
for _ in range(TRIALS): #<- use _ to ignore loop var
    wins = {t: sum(1 for _ in range(GAMES) if random.random() < p)
            for t, p in TEAM_P.items()}
    # random tiebreaker for ties at the top
    top = max(wins.values())
    tied = [t for t, w in wins.items() if w == top]
    first_place[random.choice(tied)] += 1
    for t, w in wins.items():
        win_sums[t] += w

print("=== Chance to finish 1st ===")
for t in TEAM_P:
    print(f"{t}: {first_place[t]/TRIALS:.2%}")

print("\n=== Mean wins over trials ===")
for t in TEAM_P:
    print(f"{t}: {win_sums[t]/TRIALS:.1f}")
