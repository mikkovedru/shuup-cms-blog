# -*- coding: utf-8 -*-
# This file is part of Shuup CMS Blog Addon.
#
# Copyright (c) 2012-2018, Shuup Inc. All rights reserved.
#
# This source code is licensed under the OSL-3.0 license found in the
# LICENSE file in the root directory of this source tree.
from django.utils.translation import ugettext_lazy as _

from shuup.front.utils.dashboard import DashboardItem


class SavedArticlesDashboardItem(DashboardItem):
    template_name = None
    title = _("Saved Articles")
    icon = "fa fa-bookmark"
    _url = "shuup:shuup-cms-blog.saved-articles"

    def show_on_dashboard(self):
        return False
