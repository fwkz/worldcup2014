from collections import namedtuple
from itertools import chain
import os
import urllib2
from bs4 import BeautifulSoup


URL = "http://www.fifa.com/worldcup/matches/index.html"
Match = namedtuple("Match", "home, away, result, status, date")


class MatchFactory(object):
    def __init__(self):
        self.soup = BeautifulSoup(urllib2.urlopen(URL).read())
        self.matches = []

        # Prevent double match entries by extracting specific DOM node from menu.
        [hidden.extract() for hidden in self.soup.findAll(attrs={"class": "megamenu-contentwrap"})]

        matches_full_time = self.soup.find_all(attrs={"class": "mu result"})
        matches_live = self.soup.find_all(attrs={"class": "mu live"})

        for match in chain(matches_full_time, matches_live):
            self.matches.append(Match(home=match.find(attrs={"class": "t home"}).find(attrs={"class": "t-nText"}).text,
                                      away=match.find(attrs={"class": "t away"}).find(attrs={"class": "t-nText"}).text,
                                      result=match.find(attrs={"class": "s-scoreText"}).text,
                                      status=match.find(attrs={"class": "s-status-abbr"}).text.strip() or "LIVE!",
                                      date=match.find(attrs={"class": "mu-i-datetime"}).text[:-11],
                                      ))

    def __iter__(self):
        """ Infinite generator. Updating it's state every iteration. """
        while 1:
            os.system('cls' if os.name == 'nt' else 'clear')
            for match in self.matches:
                yield match
            self.__init__()


if __name__ == "__main__":
    for match in MatchFactory():
        print u"{} {}\n{} {} {}\n".format(match.date, match.status, match.home, match.result, match.away)