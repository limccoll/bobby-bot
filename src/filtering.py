"""Bobby.Bot recommendation filtering.

Three layers, as described in the project report:
1. Wisdom Level slider: each place has a wisdom score (0-100) for how far
   it is from mainstream algorithmic recommendations. A place is shown when
   its score is within +/-45 of the slider position (default 85).
2. Review-count signal: few reviews + high rating = local credibility.
   Places are ranked so that hidden, well-loved spots come first.
3. Category and budget: Culture / Dining / Entertainment (the niche found
   in the wheel survey), plus a budget from 1 (GBP) to 4 (GBPGBPGBPGBP).
"""
from dataclasses import dataclass
import math

DEFAULT_WISDOM = 85
TOLERANCE = 45
NICHE = {"culture", "dining", "entertainment"}


@dataclass
class Place:
    name: str
    category: str
    wisdom_score: int   # 0 = mainstream, 100 = deeply local
    rating: float       # 0-5 stars
    review_count: int
    price_level: int    # 1-4


def in_wisdom_range(place: Place, slider: int = DEFAULT_WISDOM, tolerance: int = TOLERANCE) -> bool:
    return abs(place.wisdom_score - slider) <= tolerance


def local_credibility(place: Place) -> float:
    """High rating with low review volume scores highest.

    Rating is weighted up; log review count is weighted down so a
    103-review, 5-star garden beats a 22,841-review, 4-star castle.
    """
    return place.rating * 2 - math.log10(place.review_count + 1)


def recommend(places, slider=DEFAULT_WISDOM, categories=NICHE, max_price=4, limit=10):
    shown = [
        p for p in places
        if in_wisdom_range(p, slider)
        and p.category in categories
        and p.price_level <= max_price
    ]
    return sorted(shown, key=local_credibility, reverse=True)[:limit]
