from __future__ import print_function
import requests
import teams
from bs4 import BeautifulSoup as Soup


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
        print("Fix your team name: {}".format(team))
        return None

    r = requests.get(url_base + team_ext)
    soup = Soup(r.text, "html.parser")
    game, season = soup.findAll("tr", "total")[:2]
    game = [t.text for t in game.findAll("td")]
    season = [t.text for t in season.findAll("td")]
    # unpack values
    (_, GP, _, PPG, RPG, APG,
        SPG, BPG, TPG, FGP, FTP, TPP) = game
    (_, _, FGM, FGA, FTM, FTA,
        TPM, TPA, PTS, OFFR, DEFR, REB, AST, TO, STL, BLK) = season

    return dict(gp=float(GP),
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
    for t in sorted(teams.teams.keys()):
        yield t


if __name__ == "__main__":
    import stats
    for team in list_teams():
        s = get_stats(team)
        print("******* {} *******".format(team))
        print("OVERALL : {}".format(stats.get_overall_score(s)))
        print("shooting: {}".format(stats.get_shooting(s)))
        print("turnover: {}".format(stats.get_turnovers(s)))
        print("rebounds: {}".format(stats.get_rebounds(s)))
        print("freethro: {}\n".format(stats.get_freethrows(s)))
