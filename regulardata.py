#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 00:19:47 2024

@author: kangkyeongmo
"""

##- Scoring Efficiency (eFG%+): 
# The effective field goal percentage (eFG%) adjusts for 
# the fact that three-point shots are worth more than two-point shots.

##- Playmaking (AST and TOV): Playmaking is based on assists (AST) and turnovers (TOV).

# Since assists are positive and turnovers are negative, 
# we’ll calculate a Playmaking Score that combines both, with a slight emphasis on assists. 

## Playmaking Score=(0.7×AST)+(0.3×TOV)

##- Rebounding (TRB): Rebounding impact is measured using total rebounds per game (TRB).
#- Defensive Impact (STL, BLK, and PF): Defense includes steals (STL), blocks (BLK), and personal fouls (PF).

##Defensive Score=(0.4*STL)+(0.4*BLK)+(0.2*PF)

#Impact Plus=(0.4*eFG%)+(0.3*PM Score)+(0.2*TRB)+(0.1*DF Score)

import pandas as pd
import numpy as np

# load Regular season data 
rg_df = pd.read_csv("RegularSeasonStats_Cleaned.csv")

# Column Names
print("column names:", rg_df.columns.tolist())

# Filter players with median games played
threshold_games = rg_df["G"].median()
if 'G' in rg_df.columns:  # Ensure 'GP' (Games Played) column exists
    rg_df = rg_df[rg_df['G'] >= threshold_games]
    print(f"Filtered DataFrame with players having >= {threshold_games} games:")
    print(rg_df)
else:
    print("The 'G' column (Games Played) is not found in the dataset.")
    rg_df # If no GP column, use the original DataFrame

### Scoring Efficiency
R_avg_eFGP = rg_df["eFG%"].mean()
print(f"Average of eFG% is: {R_avg_eFGP}")

### Playmaking Score = (AST*0.7) + (TOV*0.3)

# AST
avg_AST = rg_df["AST"].mean()
print(f"AST07 is: {avg_AST}")
# TOV 
avg_TOV = rg_df["TOV"].mean()
print(f"TOV03 is: {avg_TOV}")

R_PMS = (0.7 * avg_AST) + (0.3 * avg_TOV)
print(f"Regular Season League Average Playmaking Score is:{R_PMS:.2f}")

### Defensive Score = (0.4*STL)+(0.4*BLK)+(0.2*PF)

# STL
avg_STL = rg_df["STL"].mean()
print(avg_STL)
# BLK
avg_BLK = rg_df["BLK"].mean()
print(avg_BLK)
# PF
avg_PF = rg_df["PF"].mean()
print(avg_PF)

R_DS = (0.4 * avg_STL) + (0.4 * avg_BLK) + (0.2 * avg_PF)
print(f"Regular Season League Average Defensive Score is:{R_DS:.2f}")

### TRB 
R_avg_TRB = rg_df["TRB"].mean()
print(R_avg_TRB)

### Impact Plus=(0.4*eFG%)+(0.3*PM Score)+(0.2*TRB)+(0.1*DF Score)
R_IP = (0.4*R_avg_eFGP)+(0.3*R_PMS)+(0.2*R_avg_TRB)+(0.1*R_DS) 
print(f"Regular Season Impact Plus is:{R_IP:.2f}")

# Normalize Impact Plus to set league average at 100
scaling_factor = 100 / R_IP
normalized_league_avg_IP = R_IP * scaling_factor
print(f"Scaling Factor: {scaling_factor:.2f}")
print(f"Normalized League Average Impact Plus is: {normalized_league_avg_IP:.2f}")


### Example for Player A
# Set the player names as the index 
if 'Player' in rg_df.columns:  
    rg_df = rg_df.set_index('Player')

# Example: Extract stats for a specific player
Kobe_Bufkin = "Kobe Bufkin"  # Replace with the desired player's name
if Kobe_Bufkin in rg_df.index:
    Kobe_Bufkin_stats = rg_df.loc[Kobe_Bufkin]
    print(f"Stats for {Kobe_Bufkin}:\n{Kobe_Bufkin_stats}")
else:
    print(f"Player '{Kobe_Bufkin}' not found in the dataset.")

# Calculate Player A's raw Impact Plus
Kobe_Bufkin_PM = (0.7 * Kobe_Bufkin_stats["AST"]) + (0.3 * Kobe_Bufkin_stats["TOV"])
Kobe_Bufkin_DS = (0.4 * Kobe_Bufkin_stats["STL"]) + (0.4 * Kobe_Bufkin_stats["BLK"]) + (0.2 * Kobe_Bufkin_stats["PF"])

Kobe_Bufkin_IP_raw = (
    (0.4 * Kobe_Bufkin_stats["eFG%"]) +
    (0.3 * Kobe_Bufkin_PM) +
    (0.2 * Kobe_Bufkin_stats["TRB"]) +
    (0.1 * Kobe_Bufkin_DS)
)

# Normalize Player A's Impact Plus
Kobe_Bufkin_IP = Kobe_Bufkin_IP_raw * scaling_factor
print(f"Kobe_Bufkin's Impact Plus (normalized) is: {Kobe_Bufkin_IP:.2f}")

# Interpretation: How much better/worsen Player A is than league average
if Kobe_Bufkin_IP < normalized_league_avg_IP:
    difference = normalized_league_avg_IP - Kobe_Bufkin_IP
    print(f"Kobe Bufkin is {difference:.2f}% worse than the league average.")
elif Kobe_Bufkin_IP > normalized_league_avg_IP:
    difference = Kobe_Bufkin_IP - normalized_league_avg_IP
    print(f"Kobe Bufkin is {difference:.2f}% better than the league average.")
else:
    print("Kobe Bufkin is performing at the league average.")

### Identify top 5 and bottom 5 players 
# Function to calculate Impact Plus for a player
def calculate_impact_plus(row):
    PM = (0.7 * row["AST"]) + (0.3 * row["TOV"])
    DS = (0.4 * row["STL"]) + (0.4 * row["BLK"]) + (0.2 * row["PF"])
    IP_raw = (0.4 * row["eFG%"]) + (0.3 * PM) + (0.2 * row["TRB"]) + (0.1 * DS)
    return IP_raw * scaling_factor

# Apply the function to all players
rg_df["Impact Plus"] = rg_df.apply(calculate_impact_plus, axis=1)

# Sort players by Impact Plus
rg_df_sorted = rg_df.sort_values(by="Impact Plus", ascending=False)

# Top 5 players
top_5_players = rg_df_sorted.head(5)
print("Top 5 Players by Impact Plus:")
print(top_5_players[["Player", "Impact Plus"]])

# Bottom 5 players
bottom_5_players = rg_df_sorted.tail(5)
print("\nBottom 5 Players by Impact Plus:")
print(bottom_5_players[["Player", "Impact Plus"]])


# Access multiple rows by positions
row_indices = [437, 374, 338, 155, 351]  # Replace with desired row positions
rows_data = rg_df.iloc[row_indices]
print(rows_data)

# Access multiple rows by labels
player_names = ["LeBron James", "Kevin Durant"]  # Replace with desired player names
rows_data = df.loc[player_names]
print(rows_data)





