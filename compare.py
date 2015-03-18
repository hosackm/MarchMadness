import sys
import stats
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
    elif ho < vo:
        print "WINNER = {} by {}".format(v, (vo-ho)*100)
    else:
        print "TIE?!?!!!???!!!!!!!"


def usage(filename):
    print "Usage: python {} home visitor".format(filename)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        usage(sys.argv[0])
        sys.exit(1)

    home, visitor = sys.argv[1:3]
    compare(home, visitor)
