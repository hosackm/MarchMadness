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

    def run(self):
        self.simulate_regions()
        self.simulate_final_four()
        return self.winner

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

        if region == "Final Four":
            rnd = "Quarterfinals" if len(teams) == 4 else "Finals"
        else:
            rnd = "Round {}".format(str(5 - int(log(len(teams), 2))))
        logger.info("{} {}: {}".format(region, rnd, teams))

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
        "Simulate each of the 4 regions and put winners into self.finalfour"
        for region, teams in self.matchups.items():
            self.finalfour[region] = self.simulate(region, teams)
        return self.finalfour

    def simulate_final_four(self):
        "Simulate the final four and return the winner"
        if self.finalfour:
            self.winner = self.simulate("Final Four",
                                        (self.finalfour["west"],
                                         self.finalfour["south"],
                                         self.finalfour["midwest"],
                                         self.finalfour["east"]))
            return self.winner

if __name__ == "__main__":
    r = Runner()
    print(r.run())
