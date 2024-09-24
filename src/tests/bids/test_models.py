import pytest

from src.bids.models import BidsHistory
from src.bids.models import BidsWinner


@pytest.fixture()
def add_bids_history(create_user, create_article):
    return BidsHistory(user=create_user, article=create_article, bids=20)


@pytest.mark.django_db()
def test_add_bids_history(add_bids_history, create_user, create_article):
    assert add_bids_history.user == create_user
    assert add_bids_history.article == create_article
    assert add_bids_history.bids == 20  # noqa:PLR2004


@pytest.fixture()
def update_bids_winner(create_user, create_article):
    return BidsWinner(user=create_user, article=create_article, bids=21)


@pytest.mark.django_db()
def test_update_bids_winner(update_bids_winner, create_user, create_article):
    assert update_bids_winner.user == create_user
    assert update_bids_winner.article == create_article
    assert update_bids_winner.bids == 21  # noqa:PLR2004


@pytest.mark.django_db()
def test_user_bidswinner(create_bidswinner):
    assert isinstance(create_bidswinner, BidsWinner)


@pytest.mark.django_db()
def test_user_bidshistory(create_bidshistory):
    assert isinstance(create_bidshistory, BidsHistory)
