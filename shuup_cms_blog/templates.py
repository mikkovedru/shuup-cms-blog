# -*- coding: utf-8 -*-
# This file is part of Shuup CMS Blog Addon.
#
# Copyright (c) 2012-2018, Shuup Inc. All rights reserved.
#
# This source code is licensed under the OSL-3.0 license found in the
# LICENSE file in the root directory of this source tree.
from django.utils.translation import ugettext as _


class BlogArticleTemplate(object):
    name = _("Blog Article Page")
    template_path = "shuup_cms_blog/blog_page.jinja"
