# This file is part of Shuup CMS Blog Addon.
#
# Copyright (c) 2012-2019, Shuup Inc. All rights reserved.
#
# This source code is licensed under the OSL-3.0 license found in the
# LICENSE file in the root directory of this source tree.
from django.utils.translation import ugettext_lazy as _

from shuup.simple_cms.models import Page
from shuup.xtheme.plugins.forms import GenericPluginForm
from shuup.xtheme.plugins.widgets import XThemeModelChoiceField


class BlogConfigForm(GenericPluginForm):
    def populate(self):
        super(BlogConfigForm, self).populate()
        self.fields["blog_page"] = XThemeModelChoiceField(
            label=_("Blog page"),
            queryset=Page.objects.filter(children__blog_article__is_blog_article=True).distinct(),
            required=False,
        )

    def clean(self):
        cleaned_data = super(BlogConfigForm, self).clean()
        blog_page = cleaned_data.get("blog_page")
        cleaned_data["blog_page"] = blog_page.pk if hasattr(blog_page, "pk") else None
        return cleaned_data
