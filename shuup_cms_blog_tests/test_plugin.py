# -*- coding: utf-8 -*-
# This file is part of Shuup CMS Blog Addon.
#
# Copyright (c) 2012-2018, Shuup Inc. All rights reserved.
#
# This source code is licensed under the OSL-3.0 license found in the
# LICENSE file in the root directory of this source tree.
from datetime import timedelta

import pytest
from django.core.urlresolvers import reverse
from django.utils.timezone import now

from shuup.simple_cms.layout import PageLayout
from shuup.simple_cms.models import Page
from shuup.testing import factories
from shuup.themes.classic_gray.theme import ClassicGrayTheme
from shuup.xtheme import get_current_theme, set_current_theme
from shuup.xtheme.layout.utils import get_layout_data_key
from shuup.xtheme.view_config import ViewConfig
from shuup_cms_blog.models import BlogArticle
from shuup_cms_blog.plugins import ShuupCMSBlogArticleListPlugin

from .utils import SmartClient


@pytest.mark.django_db
def test_plugin():
    shop = factories.get_default_shop()
    set_current_theme(ClassicGrayTheme.identifier, shop)

    blog_page = Page.objects.create(
        shop=shop,
        title="Blog",
        url="blog",
        available_from=(now() - timedelta(days=10)),
        available_to=(now() + timedelta(days=10)),
        content=""
    )

    # create 10 blog pages
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

    # create 3 non blog post pages
    for i in range(3):
        article = Page.objects.create(
            shop=shop,
            title="Nothing %d" % i,
            url="non-%d" % i,
            available_from=(now() - timedelta(days=10)),
            available_to=(now() + timedelta(days=10)),
            content="content %i" % i
        )

    theme = get_current_theme(shop)
    view_config = ViewConfig(theme=theme, shop=shop, view_name="PageView", draft=True)

    placeholder_name = "cms_page"
    context = {"page": blog_page}
    layout = view_config.get_placeholder_layout(PageLayout, placeholder_name, context=context)
    assert isinstance(layout, PageLayout)
    assert layout.get_help_text({}) == ""
    assert blog_page.title in layout.get_help_text(context)
    serialized = layout.serialize()
    assert len(serialized["rows"]) == 0
    assert serialized["name"] == placeholder_name

    layout.begin_column({"sm": 12})
    layout.add_plugin(ShuupCMSBlogArticleListPlugin.identifier, {})
    view_config.save_placeholder_layout(get_layout_data_key(placeholder_name, layout, context), layout)
    view_config.publish()

    client = SmartClient()
    response, soup = client.response_and_soup(reverse("shuup:cms_page", kwargs={"url": blog_page.url}))
    assert response.status_code == 200
    assert len(soup.find_all("a", {"class": "article-card"})) == 10
