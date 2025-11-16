import random
from collections import Counter

#how many wins and losses a team starts with, ten calculate expected value of wins

TEAM_P = { # we can get the P for each team using Pythag Expectation
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
TRIALS = 3000  # trial count

 
TEAM_WINS_CONDITIONAL = 20 #Wins for the given conditional
STARTING_GAMES_CONDITIONAL = 30 # Number of wins when the conditional is checked

probability_of_conditional = {} #Chances for the conditional to be true
conditional_met = {} #Keeps track of when a conditional is meet in a trial
first_place_with_conditional = {} #Chance of winning first place and conditional being true

for team in TEAM_P:
    if (TEAM_WINS_CONDITIONAL == 0 and STARTING_GAMES_CONDITIONAL == 0): ## Basecase - Every teams has 0 wins in zero games
        conditional_met[team] = True
        probability_of_conditional[team] = TRIALS
    else:
        conditional_met[team] = False
        probability_of_conditional[team] = 0.0
    first_place_with_conditional[team] = 0.0

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

            # Adds to the Baye wins if this team has x amount of wins in the first y games
            if (game_index == STARTING_GAMES_CONDITIONAL - 1):
                if (TEAM_WINS_CONDITIONAL == win_count):
                    probability_of_conditional[t] += 1
                    conditional_met[t] = True
                else:
                    conditional_met[t] = False
                

            

    # After finishing all the simulated games, store the win total
        wins[t] = win_count
    # random tiebreaker for ties at the top
    top = max(wins.values()) #determine the team with max wins
    tied = [t for t, w in wins.items() if w == top] #list of teams that are tied for first
    winningTeam = random.choice(tied) #randomly choose one of the tied teams to get first place credit
    first_place[winningTeam] += 1 
    for t, w in wins.items(): #add each teams wins to their total win count
        win_sums[t] += w #add wins to total
    if (conditional_met[winningTeam]): 
        first_place_with_conditional[winningTeam] += 1 #add a points for the wining team if the baye condition was met

winning_with_conditional_probability = {} #Dictionary containing the probabilies of a team winning if the conditional property is true
for t in TEAM_P:
    if (probability_of_conditional[t] != 0 and first_place[t] != 0): #Prevents a divide by zero
        bayeChanceWhenWinning = first_place_with_conditional[t] / first_place[t] #Chance the conditional is meet in a winning season
        winning_with_conditional_probability[t] = (first_place[t] * bayeChanceWhenWinning) / (probability_of_conditional[t]) # Bayes Theroem
    else:
        winning_with_conditional_probability[t] = 0.0 
    


print("\n=== Chance to finish 1st ===")
for t in TEAM_P:
    print(f"{t}: {first_place[t]/TRIALS:.2%}")

print("\n=== Conditional: Chance for a team to win " + str(TEAM_WINS_CONDITIONAL) + " games out of the first " + str(STARTING_GAMES_CONDITIONAL) + " games ===")
for t in TEAM_P:
    print(f"{t}: {probability_of_conditional[t]/TRIALS:.2%}")

print("\n=== Chance for conditional to be true when finishing 1st ===")
for t in TEAM_P:
    if (first_place[t] != 0):
        print(f"{t}: {first_place_with_conditional[t] / first_place[t]:.2%}")
    else:
        print(f"{t}: {0.0:.2%}")

print("\n=== Chance of finishing 1st with conditional true ===")
for t in TEAM_P:
    print(f"{t}: {winning_with_conditional_probability[t]:.2%}")

print("\n=== Mean wins over trials ===")
for t in TEAM_P:
    print(f"{t}: {win_sums[t]/TRIALS:.1f}")
