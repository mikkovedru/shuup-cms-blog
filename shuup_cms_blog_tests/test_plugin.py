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

    blog_one_page = Page.objects.create(
        shop=shop,
        title="Blog One",
        url="blog_one",
        available_from=(now() - timedelta(days=10)),
        available_to=(now() + timedelta(days=10)),
        content=""
    )

    blog_two_page = Page.objects.create(
        shop=shop,
        title="Blog Two",
        url="blog_two",
        available_from=(now() - timedelta(days=10)),
        available_to=(now() + timedelta(days=10)),
        content=""
    )
    # create 10 blog pages
    for page in [blog_one_page, blog_two_page]:
        for i in range(10):
            article = Page.objects.create(
                shop=shop,
                title="Article %d %s" % (i, page.title),
                url="blog-%d-%s" % (i, page.url),
                available_from=(now() - timedelta(days=10)),
                available_to=(now() + timedelta(days=10)),
                content="Content %d" % i,
                template_name="shuup_cms_blog/blog_page.jinja",
                parent=page
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
    context_one = {"page": blog_one_page}
    context_two = {"page": blog_two_page}

    layout_one = view_config.get_placeholder_layout(PageLayout, placeholder_name, context=context_one)
    layout_two = view_config.get_placeholder_layout(PageLayout, placeholder_name, context=context_two)

    assert isinstance(layout_one, PageLayout)
    assert isinstance(layout_two, PageLayout)

    assert layout_one.get_help_text({}) == ""
    assert layout_two.get_help_text({}) == ""

    assert blog_one_page.title in layout_two.get_help_text(context_one)
    assert blog_two_page.title in layout_two.get_help_text(context_two)

    serialized_one = layout_one.serialize()
    serialized_two = layout_two.serialize()

    assert len(serialized_one["rows"]) == 0
    assert len(serialized_two["rows"]) == 0

    assert serialized_one["name"] == placeholder_name
    assert serialized_two["name"] == placeholder_name

    layout_one.begin_column({"sm": 12})
    layout_two.begin_column({"sm": 12})

    layout_one.add_plugin(ShuupCMSBlogArticleListPlugin.identifier, {"blog_page": blog_one_page.pk})
    layout_two.add_plugin(ShuupCMSBlogArticleListPlugin.identifier, {"blog_page": blog_two_page.pk})

    view_config.save_placeholder_layout(get_layout_data_key(placeholder_name, layout_one, context_one), layout_one)
    view_config.save_placeholder_layout(get_layout_data_key(placeholder_name, layout_two, context_two), layout_two)
    view_config.publish()

    client = SmartClient()
    response, soup = client.response_and_soup(reverse("shuup:cms_page", kwargs={"url": blog_one_page.url}))
    assert response.status_code == 200
    assert len(soup.find_all("a", {"class": "article-card"})) == 10

    response, soup = client.response_and_soup(reverse("shuup:cms_page", kwargs={"url": blog_two_page.url}))
    assert response.status_code == 200
    assert len(soup.find_all("a", {"class": "article-card"})) == 10

    article = Page.objects.create(
        shop=shop,
        title="Article test",
        url="blog-test",
        available_from=(now() - timedelta(days=10)),
        available_to=(now() + timedelta(days=10)),
        content="Content test",
        template_name="shuup_cms_blog/blog_page.jinja",  # Add an article without a parent
    )
    BlogArticle.objects.create(
        page=article,
        is_blog_article=True,
        image=factories.get_random_filer_image(),
        small_description="description test"
    )
    view_config = ViewConfig(theme=theme, shop=shop, view_name="PageView", draft=True)

    # No blog page set means that only articles with no parent will be shown
    layout_two.add_plugin(ShuupCMSBlogArticleListPlugin.identifier, {})
    view_config.save_placeholder_layout(get_layout_data_key(placeholder_name, layout_two, context_two), layout_two)
    view_config.publish()

    response, soup = client.response_and_soup(reverse("shuup:cms_page", kwargs={"url": blog_two_page.url}))
    assert response.status_code == 200
    assert len(soup.find_all("a", {"class": "article-card"})) == 1

    article.soft_delete()  # Delete the article that has no parent

    response, soup = client.response_and_soup(reverse("shuup:cms_page", kwargs={"url": blog_two_page.url}))
    assert response.status_code == 200
    assert len(soup.find_all("a", {"class": "article-card"})) == 0
