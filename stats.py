import math
# The following stats are pulled for all teams:
# =============================================
# Avg. per Game
# =============
# GP    = Games Played
# PPG   = Points per Game
# RPG   = Rebounds per Game
# APG   = Assists per Game
# SPG   = Steals per Game
# BPG   = Blocks per Game
# TPG   = Turnovers per Game
# FGP   = Field Goal % per Game
# FTP   = Free Throw % per Game
# TPP   = Three Point % per Game
# Season Long
# ===========
# FGM   = Field Goals Made
# FGA   = Field Goals Attempted
# FTM   = Free Throws Made
# FTA   = Free Throws Attempted
# TPM   = Three Pointers Made
# TPA   = Three Pointers Attempted
# PTS   = Points
# OFFR  = Offensive Rebounds
# DEFR  = Defensive Rebounds
# REB   = Rebounds (OFFR + DEFR)
# AST   = Assists
# TO    = Turnovers
# STL   = Steals
# BLK   = Blocks


def get_shooting(teamstats):
    """Calculate a team's Effective Field Goal Percentage (EFGP)
    For offense and defense the formula is:
        EFGP = (FGM + (TPM / 2)) / FGA
    Maximize this
    """
    tg = teamstats.get  # local function ref
    try:
        return (tg("fgm") + 0.5 * tg("tpm")) / tg("fga")
    except Exception as e:
        print type(e), "exception during shooting calc"
        return 0.0


def get_turnovers(teamstats):
    """Calculate a team's Turnover Percentage (TOVP)
    For offense and defense the formula is:
        TOVP = TO / (FGA + 0.44 * FTA + TO)
    Minimize this
    """
    tg = teamstats.get  # local function ref
    try:
        return tg("to") / (tg("fga") + 0.44 * tg("fta") + tg("to"))
    except Exception as e:
        print type(e), "exception during turnovers calc"
        return 0.0


def get_rebounds(teamstats):
    """Calculate a team's rebound effectiveness (RB)
        RB = (OFFR + REB) / (REB)
    Maximize this
    """
    tg = teamstats.get  # local function ref
    try:
        return (tg("offr") + tg("reb")) / tg("reb")
    except Exception as e:
        print type(e), "exception during rebounds calc"
        return 0.0


def get_freethrows(teamstats):
    """Calculate a team's Free Throw Percentage (FTP)
        FTP = FTM / FTA
    Maximize this
    """
    tg = teamstats.get  # local function ref
    try:
        return tg("ftm") / tg("fta")
    except Exception as e:
        print type(e), "exception during freethrows calc"
        return 0.0