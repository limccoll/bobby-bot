import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from filtering import Place, in_wisdom_range, local_credibility, recommend

garden = Place("Dr Neil's Garden", "culture", 90, 5.0, 103, 1)
castle = Place("Edinburgh Castle", "culture", 5, 4.0, 22841, 3)
cafe = Place("Independent cafe", "dining", 70, 4.6, 240, 2)
shop = Place("Gift shop", "shopping", 80, 4.8, 50, 1)


def test_default_slider_hides_mainstream():
    assert in_wisdom_range(garden)
    assert not in_wisdom_range(castle)


def test_low_slider_shows_mainstream():
    assert in_wisdom_range(castle, slider=10)


def test_local_credibility_prefers_hidden_gems():
    assert local_credibility(garden) > local_credibility(castle)


def test_recommend_filters_category_and_budget():
    names = [p.name for p in recommend([garden, castle, cafe, shop], max_price=1)]
    assert names == ["Dr Neil's Garden"]
