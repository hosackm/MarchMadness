import sys
import stats
import teams
import scraper


def compare(h, v):
    """Compare home team stats vs visitor team stats
    """
    hs = scraper.get_stats(h)
    vs = scraper.get_stats(v)

    gos = stats.get_overall_score
    gsh = stats.get_shooting
    gto = stats.get_turnovers
    grb = stats.get_rebounds
    gft = stats.get_freethrows

    print "******** {} ********\t******** {} ********".format(h, v)
    print "OVERALL : {}\tOVERALL : {}".format(gos(hs), gos(vs))
    print "shooting: {}\tshooting: {}".format(gsh(hs), gsh(vs))
    print "turnover: {}\tturnover: {}".format(gto(hs), gto(vs))
    print "rebounds: {}\trebounds: {}".format(grb(hs), grb(vs))
    print "freethro: {}\tfreethro: {}\n\n".format(gft(hs), gft(vs))

    ho = gos(hs)
    vo = gos(vs)

    if ho > vo:
        print "WINNER = {} by {}".format(h, (ho-vo)*100)
        return h
    elif ho < vo:
        print "WINNER = {} by {}".format(v, (vo-ho)*100)
        return v
    else:
        print "TIE?!?!!!???!!!!!!!"
        return h


def sim_bracket():
    """Run through matchups and simulate the bracket while printing
    out the results.  This may be rewritten as a recursive function
    """
    matchups = teams.matchups
    while len(matchups):
        winners = []
        for matchup in matchups:
            print "Matchup: {} vs {}".format(matchup[0], matchup[1])
            winner = compare(matchup[0], matchup[1])
            winners.append(winner)
            print "Winner: {}".format(winner)
        if len(winners) == 1:
            return winners[0]
        print "winners: {}".format(winners)
        matchups = zip(winners)
        print "zipped to: {}".format(matchups)


def usage(filename):
    print "Usage: python {} home visitor".format(filename)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        usage(sys.argv[0])
        sys.exit(1)

    home, visitor = sys.argv[1:3]
    compare(home, visitor)
