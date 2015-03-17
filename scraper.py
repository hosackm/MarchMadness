import requests
import teams
import pprint
from BeautifulSoup import BeautifulSoup as Soup


def get_team_ext(team):
    """Give url extension for team's espn.com page"""
    return teams.teams.get(team)


def get_stats(team):
    """Provide a teamname (str) and this function will scrape that team's
    stats from espn.com.
    Return: dictionary containing all stats
    """
    url_base = "http://espn.go.com/mens-college-basketball/team/stats/_/id"
    team_ext = get_team_ext(team)
    if not team_ext:
        print "Fix your team name: {}".format(team)
        return None

    r = requests.get(url_base + team_ext)
    soup = Soup(r.text)
    game, season = soup.findAll("tr", "total")[:2]
    game = [t.text for t in game.findAll("td")]
    season = [t.text for t in season.findAll("td")]
    # unpack values
    (_, GP, _, PPG, RPG, APG,
        SPG, BPG, TPG, FGP, FTP, TPP) = game
    (_, _, FGM, FGA, FTM, FTA,
        TPM, TPA, PTS, OFFR, DEFR, REB, AST, TO, STL, BLK) = season

    return dict(
        gp=float(GP),
        ppg=float(PPG),
        rpg=float(RPG),
        apg=float(APG),
        spg=float(SPG),
        bpg=float(BPG),
        tpg=float(TPG),
        fgp=float(FGP),
        ftp=float(FTP),
        tpp=float(TPP),
        fgm=float(FGM),
        fga=float(FGA),
        ftm=float(FTM),
        fta=float(FTA),
        tpm=float(TPM),
        tpa=float(TPA),
        pts=float(PTS),
        offr=float(OFFR),
        defr=float(DEFR),
        reb=float(REB),
        ast=float(AST),
        to=float(TO),
        stl=float(STL),
        blk=float(BLK))


def list_teams():
    """Print out list of all available teams"""
    pprint.pprint(sorted(teams.teams.keys()))


if __name__ == "__main__":
    #list_teams()
    pprint.pprint(get_stats("wisconsin"))
