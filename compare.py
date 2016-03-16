from __future__ import print_function, division
import stats
import scraper
import logging

logging.basicConfig()
logger = logging.getLogger("march.maddness.log")
logger.setLevel(logging.DEBUG)


def compare(home, visitor):
    "Compare home team stats vs visitor team stats"
    # get overall home and visitor stats
    homestats = scraper.get_stats(home)
    visitorstats = scraper.get_stats(visitor)
    homeoverall = stats.get_overall_score(homestats)
    visitoroverall = stats.get_overall_score(visitorstats)

    # finally do the comparison
    return home if homeoverall >= visitoroverall else visitor


def simulate(region, teams):
    """
    Takes a list of team names and delivers the winner after comparing each
    pair of teams two at a time.
    For example, a bracket of ["team1", "team2", "team3", "team4"] would
    be simulated as:
        compare("team1", "team2") => winner "team2"
        compare("team3", "team4") => winner "team3"

        teams_left = ["team2", "team3"]
        compare("team2", "team3") => winner "team3"
    """
    if len(teams) < 2:
        return teams[0]

    rnd = 16 // len(teams)
    logger.info("{} Round {}: {}".format(region, rnd, teams))

    # zip matchups from what's left in the teams list
    # [1, 2, 3, 4] => [(1, 2), (3, 4)]
    matchups = list(zip(teams[::2], teams[1::2]))
    # empty teams so that we can replace it with the winners
    teams = []

    # simulate each matchup and put the winner back into teams list
    for match in matchups:
        home, visitor = match
        winner = compare(home, visitor)

        teams.append(winner)

        logger.info("simulating: {} vs. {} ==> {}".format(
            home,
            visitor,
            winner))

    return simulate(region, teams)

if __name__ == "__main__":
    import yaml
    matchups = yaml.load(open("matchups.yml"))
    winners = {}

    for region, teams in matchups.items():
        winners[region] = simulate(region, teams)

    # create new bracket of 4 regional champions
    finalfour = [winners["west"], winners["west"],
                 winners["midwest"], winners["east"]]

    # simulate final four bracket
    champ = simulate("finalfour", finalfour)
