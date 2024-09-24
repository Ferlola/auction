import pytest


@pytest.mark.django_db()
def test_article(create_article, create_user, create_category, create_subcategory):
    assert create_article.user == create_user
    assert create_article.article == "article_test"
    assert create_article.description == "description_test"
    assert create_article.location == "location_test"
    assert create_article.category == create_category
    assert create_article.subcategory == create_subcategory
    assert create_article.slug == "article-test"
    assert create_article.notification_winner == True  # noqa:E712
    assert create_article.notification_no_bid == True  # noqa:E712
    assert create_article.publish == False  # noqa:E712


@pytest.mark.django_db()
def test_date_time(create_article):
    assert create_article.from_date < create_article.date_time
