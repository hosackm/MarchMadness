from __future__ import print_function
import stats
import scraper


def compare(h, v):
    """Compare home team stats vs visitor team stats
    """
    hs = scraper.get_stats(h)
    vs = scraper.get_stats(v)

    # local references to functions
    gos = stats.get_overall_score
    gsh = stats.get_shooting
    gto = stats.get_turnovers
    grb = stats.get_rebounds
    gft = stats.get_freethrows

    # print(out some info for the user.  update this to use logging module)
    print("******** {} ********\t******** {} ********".format(h, v))
    print("OVERALL : {}\tOVERALL : {}".format(gos(hs), gos(vs)))
    print("shooting: {}\tshooting: {}".format(gsh(hs), gsh(vs)))
    print("turnover: {}\tturnover: {}".format(gto(hs), gto(vs)))
    print("rebounds: {}\trebounds: {}".format(grb(hs), grb(vs)))
    print("freethro: {}\tfreethro: {}\n\n".format(gft(hs), gft(vs)))

    # get overall home and visitor stats
    ho = gos(hs)
    vo = gos(vs)

    # finally do the comparison
    if ho > vo:
        print("WINNER = {} by {}".format(h, (ho-vo)*100))
        return h
    elif ho < vo:
        print("WINNER = {} by {}".format(v, (vo-ho)*100))
        return v
    else:
        print("TIE?!?!!!???!!!!!!!")
        return h


if __name__ == "__main__":
    with open("matchups.txt", "r") as f:
        for line in f:
            home, visitor = line.split()
            try:
                compare(home, visitor)
            except Exception as e:
                print("Exception thrown", e)
