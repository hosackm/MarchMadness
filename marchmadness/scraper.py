from __future__ import print_function
import pickle
import requests
import time
import os
from bs4 import BeautifulSoup as Soup
from .teams import teams


def load_cache(filename):
    "Return a dictionary from a pickle file or return an empty dictionary."
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            return pickle.load(f)
    else:
        return {}


def get_team_ext(team):
    """Give url extension for team's espn.com page"""
    return teams.get(team)


def list_teams():
    """Print out list of all available teams"""
    for t in sorted(teams.keys()):
        yield t


class Cache:
    """
    The Cache object acts like a dictionary but stores it's state in a pickle
    file so that it can retain it's state over each execution.
    """
    def __init__(self, filename):
        self.filename = filename
        self.cache = load_cache(filename)

    def __getitem__(self, key):
        """
        Attempt to retrieve a team's entry from the cache.  If the entry
        does not exist or is not recent enough, return None
        """
        team_dict = self.cache.get(key)

        # if the team does not have an entry return None
        if team_dict is None:
            return None

        # check if the cache for this team was updated within a day ago
        # if it wasn't return None.
        lastupdate = team_dict["lastupdate"]
        if time.time() - lastupdate > 86400:
            return None

        # return an entry that exists and is recent
        return self.cache.get(key)

    def __setitem__(self, key, value):
        # add the lastupdate entry to the value passed in
        value["lastupdate"] = time.time()
        self.cache.update({key: value})
        # write the cache to the pickle file
        with open(self.filename, "wb") as f:
            f.write(pickle.dumps(self.cache))


class Scraper:
    """
    The Scraper class scrapes team's stats from espn.go.com.  It has an
    internal cache of team's stats.  If the cache has not recently been updated
    the Scraper will retrieve new stats from espn.go.com.
    """
    base = "http://espn.go.com/mens-college-basketball/team/stats/_/id"

    def __init__(self, picklename="marchmadness.pickle"):
        self.cache = Cache(picklename)

    def _get_from_internet(self, team):
        # Get the url suffix from teams.py
        team_ext = get_team_ext(team)
        if not team_ext:
            raise Exception("Unable to find URL extension for this team.")

        # make a GET request and parse the response using Beautiful Soup
        r = requests.get(self.base + team_ext)
        soup = Soup(r.text, "html.parser")

        # all stats are within <tr class="total"></tr> tags
        game, season = soup.findAll("tr", "total")[:2]

        # get HTML inner text
        game = [t.text for t in game.findAll("td")]
        season = [t.text for t in season.findAll("td")]

        # Pull out the important stats from the list of various stats
        (_, GP, _, PPG, RPG, APG,
            SPG, BPG, TPG, FGP, FTP, TPP) = game
        (_, _, FGM, FGA, FTM, FTA,
            TPM, TPA, PTS, OFFR, DEFR, REB, AST, TO, STL, BLK) = season

        # Create a dictionary containing all the stats.  Save it to the cache
        # before returning it
        teamstats = dict(gp=float(GP), ppg=float(PPG), rpg=float(RPG),
                         apg=float(APG), spg=float(SPG), bpg=float(BPG),
                         tpg=float(TPG), fgp=float(FGP), ftp=float(FTP),
                         tpp=float(TPP), fgm=float(FGM), fga=float(FGA),
                         ftm=float(FTM), fta=float(FTA), tpm=float(TPM),
                         tpa=float(TPA), pts=float(PTS), offr=float(OFFR),
                         defr=float(DEFR), reb=float(REB), ast=float(AST),
                         to=float(TO), stl=float(STL), blk=float(BLK))
        self.cache[team] = teamstats
        return teamstats

    def get_stats(self, team):
        """
        Attempt to grab the stats from the cache.
        Otherwise resort to the Internet
        """
        cache_try = self.cache[team]
        if cache_try is not None:
            return cache_try
        return self._get_from_internet(team)

if __name__ == "__main__":
    import stats
    scr = Scraper()
    for team in list_teams():
        s = scr.get_stats(team)
        msg = ("******* {} ******\n"
               "OVERALL : {}\n"
               "shooting: {}\n"
               "turnover: {}\n"
               "rebounds: {}\n"
               "freethrows: {}\n")
        print(msg.format(team,
                         stats.get_overall_score(s),
                         stats.get_shooting(s),
                         stats.get_turnovers(s,),
                         stats.get_rebounds(s),
                         stats.get_freethrows(s)))
