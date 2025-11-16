import random
from collections import Counter

#how many wins and losses a team starts with, ten calculate expected value of wins

TEAM_P = { # we can get the P for each team using Pythag Expectation
    "ARI": 0.503,
    "OAK": 0.451,
    "ATL": 0.494,
    "BAL": 0.431,
    "BOS": 0.569,
    "CUB": 0.591,
    "CWS": 0.438,
    "CIN": 0.523,
    "CLE": 0.496,
    "WAS": 0.433,
    #stuff below here is not yet calulated, as in just random vals
    "LAD": 0.58,
    "NYM": 0.52,
    "CHC": 0.51,
    "SDP": 0.53,
    "COL": 0.27,
    "DET": 0.54,
    "HOU": 0.51,
    "KAN": 0.51,
    "LAA": 0.40,
    "LAD": 0.59,
    "MIM": 0.45,
    "MIB": 0.61,
    "MNT": 0.44,
    "NYM": 0.53,
    "NYY": 0.60,
    "PHP": 0.58,
    "PTP": 0.45,
    "SDP": 0.45,
    "STM": 0.55,
    "SFG": 0.57,
    "SLC": 0.46,
    "TBR": 0.54,
    "TRG": 0.56,
    "TBJ": 0.55,
    "WNA": 0.38
    # "TOR": random.betavariate(25, 31),
}

GAMESPLAYED=40
PRIORS = {}                       # Create an empty dictionary to store priors

# Loop through each key–value pair in TEAM
for item in TEAM_P.items():      # TEAM_P.items() returns pairs like ("ATL", 0.494)

    team = item[0]                   # team name, e.g., "ATL"
    pythagwin = item[1]                  # that team's Pythagorean win percentage, e.g., 0.494

    # Compute alpha = μ * κ
    alpha_value = pythagwin * GAMESPLAYED

    # Compute beta = (1 − μ) * κ
    one_minus_mu = 1 - pythagwin
    beta_value = one_minus_mu * GAMESPLAYED

    # Create a tuple containing (alpha, beta)
    alpha_beta_tuple = (alpha_value, beta_value)

    # Store it in the PRIORS dictionary under the key = team name
    PRIORS[team] = alpha_beta_tuple

GAMES = 150 #games in a seson
TRIALS = 2000  # trial count

first_place = Counter() #to count first place finishes, it auto-adds a key if the jey doesnt exist yet 
win_sums = Counter() #same as above, but for wins
#we use counter here cuz it makes it easy to count things without initializing keys

#found most of this monte carlo sim online and will work on it 
for _ in range(TRIALS): #<- use _ to ignore loop var
    wins = {}   # create an empty dictionary to store win totals

# TEAM_P.items() gives pairs like ("ATL", 0.494)
    for team_probability_pair in TEAM_P.items():

    # Extract the team name (t) and its probability value (p)
        t = team_probability_pair[0]   # e.g. "ATL"
        # p = team_probability_pair[1]   # e.g. 0.494 (win probability)
        alpha_for_team, beta_for_team = PRIORS[t]
        p = random.betavariate(alpha_for_team, beta_for_team)

    # Simulate indpendent games for this team

        win_count = 0   # start this team's win count at 0

    # Loop through every simulated game
        for game_index in range(GAMES):

        # Generate a random number between 0 and 1
            random_value = random.random()

        # Compare to the team's win probability
            if random_value < p:
            # If true, this is a simulated win
                win_count = win_count + 1

    # After finishing all the simulated games, store the win total
        wins[t] = win_count
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
