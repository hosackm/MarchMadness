from __future__ import print_function
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
# These statistics have been pulled from:
# http://www.basketball-reference.com/about/factors.html
# However, it is common knowledge in the basketball world that
# Rebounds, Turnovers, Shooting, and Free Throws are the most
# important stats for a team's success


class Statistics():
    def __init__(self, stats):
        self.stats = stats

    def get_shooting(self):
        """Calculate a team's Effective Field Goal Percentage (EFGP)
        For offense and defense the formula is:
            EFGP = (FGM + (TPM / 2)) / FGA
        Maximize this
        """
        tg = self.stats.get  # local function ref
        try:
            return (tg("fgm") + 0.5 * tg("tpm")) / tg("fga")
        except Exception as e:
            print(type(e), "exception during shooting calc")
            return 0.0

    def get_turnovers(self):
        """Calculate a team's Turnover Percentage (TOVP)
        For offense and defense the formula is:
            TOVP = TO / (FGA + 0.44 * FTA + TO)
        Minimize this
        """
        tg = self.stats.get  # local function ref
        try:
            return tg("to") / (tg("fga") + 0.44 * tg("fta") + tg("to"))
        except Exception as e:
            print(type(e), "exception during turnovers calc")
            return 0.0

    def get_rebounds(self):
        """Calculate a team's rebound effectiveness (RB)
            RB = (OFFR + REB) / (REB * 550)
        Maximize this
        """
        tg = self.stats.get  # local function ref
        try:
            return (tg("offr") * tg("reb")) / (tg("reb") * 550.0)
        except Exception as e:
            print(type(e), "exception during rebounds calc")
            return 0.0

    def get_freethrows(self):
        """Calculate a team's Free Throw Percentage (FTP)
            FTP = FTM / FTA
        Maximize this
        """
        tg = self.stats.get  # local function ref
        try:
            return tg("ftm") / tg("fta")
        except Exception as e:
            print(type(e), "exception during freethrows calc")
            return 0.0

    def get_overall_score(self):
        """The weights of the previous 4 stats (in NBA) are:
            Shooting: 40%
            Turnovers: 25%
            Rebounding: 20%
            Free Throws: 15%
        I would adjust these for college to:
            Shooting: 30%
            Turnovers: 22%
            Rebounding: 30%
            Free Throws: 18%
        """
        s, t, r, f = .4, .25, .2, .15
        return s*self.get_shooting() + \
            t * (1.0 - self.get_turnovers()) + \
            r * self.get_rebounds() + \
            f * self.get_freethrows()
