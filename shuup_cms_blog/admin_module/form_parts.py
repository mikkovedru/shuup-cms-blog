# -*- coding: utf-8 -*-
# This file is part of Shuup CMS Blog Addon.
#
# Copyright (c) 2012-2018, Shuup Inc. All rights reserved.
#
# This source code is licensed under the OSL-3.0 license found in the
# LICENSE file in the root directory of this source tree.
from __future__ import unicode_literals

from django.conf import settings

from shuup.admin.form_part import FormPart, TemplatedFormDef
from shuup.admin.forms import ShuupAdminForm
from shuup_cms_blog.models import BlogArticle


class BlogForm(ShuupAdminForm):
    class Meta:
        model = BlogArticle
        fields = ("is_blog_article", "small_description", "image")


class BlogFormPart(FormPart):
    priority = 10
    name = "blog"
    form = BlogForm

    def get_form_defs(self):
        if self.object.pk:
            instance = BlogArticle.objects.get_or_create(page=self.object)[0]
        else:
            instance = BlogArticle(page=self.object)

        yield TemplatedFormDef(
            name=self.name,
            form_class=self.form,
            template_name="shuup_cms_blog/blog_form_part.jinja",
            required=True,
            kwargs={
                "instance": instance,
                "languages": settings.LANGUAGES
            })

    def form_valid(self, form):
        form[self.name].instance.page = self.object
        form[self.name].save()
