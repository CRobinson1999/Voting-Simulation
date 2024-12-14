from math import dist
from numpy import nanargmin, signedinteger, nan
from typing import Self, Any


class Voter(object):
    _p = [0, 0] # Preference space

    def __init__(self, p):
        self._p = p

    def __getitem__(self, key):
        return self._p[key]

    def dist_to(self, other : Self) -> float:
        return dist(self._p, other._p) if other is not None else nan

    def pick_nearest(self, candidates : list[Self]) -> signedinteger[Any]:
        return nanargmin([self.dist_to(c) for c in candidates]) # For now, candidates are Voter as well
