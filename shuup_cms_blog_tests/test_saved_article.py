# -*- coding: utf-8 -*-
# This file is part of Shuup CMS Blog Addon.
#
# Copyright (c) 2012-2018, Shuup Inc. All rights reserved.
#
# This source code is licensed under the OSL-3.0 license found in the
# LICENSE file in the root directory of this source tree.
import json
from datetime import timedelta

import pytest
from django.utils.timezone import now

from shuup.core.models import get_person_contact
from shuup.simple_cms.models import Page
from shuup.testing import factories
from shuup.testing.utils import apply_request_middleware
from shuup_cms_blog.models import BlogArticle
from shuup_cms_blog.views import (
    AddSavedArticlesView, RemoveSavedArticlesView, SavedArticlesView
)


@pytest.mark.django_db
def test_saved_articles(rf):
    shop = factories.get_default_shop()
    articles = []

    # create 3 blog pages
    for i in range(10):
        article = Page.objects.create(
            shop=shop,
            title="Article %d" % i,
            url="blog-%d" % i,
            available_from=(now() - timedelta(days=10)),
            available_to=(now() + timedelta(days=10)),
            content="Content %d" % i,
            template_name="shuup_cms_blog/blog_page.jinja"
        )
        BlogArticle.objects.create(
            page=article,
            is_blog_article=True,
            image=factories.get_random_filer_image(),
            small_description="description %d" % i
        )
        articles.append(article)

    user = factories.create_random_user()
    user.set_password("pass")
    contact = get_person_contact(user)

    assert not contact.options
    request = apply_request_middleware(rf.get("/"), user=user)

    # save article #1
    response = AddSavedArticlesView.as_view()(request, pk=articles[0].pk)
    assert response.status_code == 302
    contact.refresh_from_db()
    options = json.loads(contact.options) if isinstance(contact.options, str) else contact.options
    assert options["saved_articles"] == [articles[0].pk]

    # save article #3
    response = AddSavedArticlesView.as_view()(request, pk=articles[2].pk)
    assert response.status_code == 302
    contact.refresh_from_db()
    options = json.loads(contact.options) if isinstance(contact.options, str) else contact.options
    assert options["saved_articles"] == [articles[0].pk, articles[2].pk]

    # list saved articles
    response = SavedArticlesView.as_view()(request)
    assert response.status_code == 200
    response.render()
    content = response.content.decode("utf-8")
    assert 'data-article="%d"' % articles[0].pk in content
    assert 'data-article="%d"' % articles[2].pk in content

    # removed saved article #3
    response = RemoveSavedArticlesView.as_view()(request, pk=articles[2].pk)
    assert response.status_code == 302
    contact.refresh_from_db()
    options = json.loads(contact.options) if isinstance(contact.options, str) else contact.options
    assert options["saved_articles"] == [articles[0].pk]
