import yaml
import logging
from math import log
from scraper import Scraper
from stats import Statistics

logging.basicConfig()
logger = logging.getLogger("march.maddness.log")
logger.setLevel(logging.DEBUG)


class Runner:
    def __init__(self, ymlfile="matchups.yml"):
        self.scraper = Scraper()
        self.matchups = yaml.load(open(ymlfile))
        self.finalfour = {}
        self.winner = None

    def compare(self, home, visitor):
        "Compare home team stats vs visitor team stats"
        # get overall home and visitor stats
        homestats = Statistics(self.scraper.get_stats(home))
        visitorstats = Statistics(self.scraper.get_stats(visitor))

        homeoverall = homestats.get_overall_score()
        visitoroverall = visitorstats.get_overall_score()

        # finally do the comparison
        return home if homeoverall >= visitoroverall else visitor

    def simulate(self, region, teams):
        """
        Recursively compare teams next to their neighbor.  The winner is kept
        int the list and the loser is removed.  Run this until there is only
        one team left in the list.
        """
        if len(teams) < 2:
            return teams[0]

        rnd = 5 - log(len(teams), 2)
        logger.info("{} Round {}: {}".format(region, rnd, teams))

        # zip matchups from what's left in the teams list
        # [1, 2, 3, 4] => [(1, 2), (3, 4)]
        matchups = list(zip(teams[::2], teams[1::2]))
        # empty teams so that we can replace it with the winners
        teams = []

        # simulate each matchup and put the winner back into teams list
        for match in matchups:
            home, visitor = match
            winner = self.compare(home, visitor)

            teams.append(winner)

            logger.info("simulating: {} vs. {} ==> {}".format(
                home,
                visitor,
                winner))

        return self.simulate(region, teams)

    def simulate_regions(self):
        for region, teams in self.matchups.items():
            self.finalfour[region] = self.simulate(region, teams)

    def simulate_final_four(self):
        if self.finalfour:
            self.winner = self.simulate((self.finalfour["west"],
                                         self.finalfour["south"],
                                         self.finalfour["midwest"],
                                         self.finalfour["east"]))
            return self.winner

if __name__ == "__main__":
    r = Runner()
    r.simulate_regions()
    print(r.finalfour)
