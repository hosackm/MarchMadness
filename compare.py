import sys
import stats
import scraper


def compare(h, v):
    """Compare home team stats vs visitor team stats
    """
    hs = scraper.get_stats(h)
    vs = scraper.get_stats(v)

    gts = stats.get_team_score
    gsh = stats.get_shooting
    gto = stats.get_turnovers
    grb = stats.get_rebounds
    gft = stats.get_freethrows

    print "******** {} ********\t******** {} ********".format(h, v)
    print "OVERALL : {}\tOVERALL : {}".format(gts(hs), gts(vs))
    print "shooting: {}\tshooting: {}".format(gsh(hs), gsh(vs))
    print "turnover: {}\tturnover: {}".format(gto(hs), gto(vs))
    print "rebounds: {}\trebounds: {}".format(grb(hs), grb(vs))
    print "freethro: {}\tfreethro: {}\n".format(gft(hs), gft(vs))


def usage(filename):
    print "Usage: python {} home visitor".format(filename)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        usage(sys.argv[0])
        sys.exit(1)

    home, visitor = sys.argv[1:3]
    compare(home, visitor)
