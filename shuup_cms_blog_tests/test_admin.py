# -*- coding: utf-8 -*-
# This file is part of Shuup CMS Blog Addon.
#
# Copyright (c) 2012-2018, Shuup Inc. All rights reserved.
#
# This source code is licensed under the OSL-3.0 license found in the
# LICENSE file in the root directory of this source tree.
import pytest
from django.core.urlresolvers import reverse

from shuup.simple_cms.models import Page
from shuup.testing import factories
from shuup.testing.soup_utils import extract_form_fields

from .utils import SmartClient


@pytest.mark.django_db
def test_admin_form_part(admin_user):
    factories.get_default_shop()
    client = SmartClient()
    client.login(username=admin_user.username, password="password")

    assert Page.objects.count() == 0
    response, soup = client.response_and_soup(reverse("shuup_admin:simple_cms.page.new"))
    assert response.status_code == 200
    payload = extract_form_fields(soup)

    # do some cleaning
    for key in payload.keys():
        if payload[key] is None:
            payload[key] = ""

    # create 9 articles
    for i in range(9):
        payload.update({
            "base-title__en": "My Article %d" % i,
            "base-url__en": "my-article-%d" % i,
            "base-available_from": "0%s/01/2018 00:00:00" % (i+1),
            "base-available_to": "0%s/01/2019 00:00:00" % (i+1),
            "base-content__en": "Some content here %d" % i,
            "base-template_name": "shuup_cms_blog/blog_page.jinja",
            "blog-is_blog_article": True,
            "blog-image": factories.get_random_filer_image().pk,
            "blog-small_description__en": "small description %d" % i
        })
        response = client.post(reverse("shuup_admin:simple_cms.page.new"), data=payload)
        assert response.status_code == 302
        assert Page.objects.count() == (i + 1)

        response, soup = client.response_and_soup(reverse("shuup:cms_page", kwargs=dict(url=payload["base-url__en"])))
        assert response.status_code == 200
        assert soup.find("div", {"class": "article-features"})

    # update blog image of the last page
    payload.update({
        "blog-image": factories.get_random_filer_image().pk,
    })
    response = client.post(
        reverse("shuup_admin:simple_cms.page.edit", kwargs=dict(pk=Page.objects.last().pk)),
        data=payload
    )
    assert response.status_code == 302
