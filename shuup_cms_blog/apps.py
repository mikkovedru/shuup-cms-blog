# -*- coding: utf-8 -*-
# This file is part of Shuup CMS Blog Addon.
#
# Copyright (c) 2012-2018, Shuup Inc. All rights reserved.
#
# This source code is licensed under the OSL-3.0 license found in the
# LICENSE file in the root directory of this source tree.
import shuup.apps


class AppConfig(shuup.apps.AppConfig):
    name = "shuup_cms_blog"
    label = "shuup_cms_blog"
    verbose_name = "Shuup CMS Blog"
    required_installed_apps = (
        "shuup.simple_cms",
    )
    provides = {
        "simple_cms_template": [
            "shuup_cms_blog.templates:BlogArticleTemplate"
        ],
        "admin_page_form_part": [
            "shuup_cms_blog.admin_module.form_parts:BlogFormPart"
        ],
        "xtheme_plugin": [
            "shuup_cms_blog.plugins:ShuupCMSBlogArticleListPlugin",
            "shuup_cms_blog.plugins:ShuupCMSBlogSaveArticleButtonPlugin"
        ],
        "front_urls_pre": [
            "shuup_cms_blog.urls:urlpatterns"
        ],
        "customer_dashboard_items": [
            "shuup_cms_blog.dashboard_items:SavedArticlesDashboardItem"
        ]
    }
