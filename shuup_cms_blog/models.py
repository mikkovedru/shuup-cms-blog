# -*- coding: utf-8 -*-
# This file is part of Shuup CMS Blog Addon.
#
# Copyright (c) 2012-2018, Shuup Inc. All rights reserved.
#
# This source code is licensed under the OSL-3.0 license found in the
# LICENSE file in the root directory of this source tree.
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from filer.fields.image import FilerImageField
from parler.models import TranslatableModel, TranslatedFields


class BlogArticle(TranslatableModel):
    page = models.OneToOneField("shuup_simple_cms.Page", verbose_name=_("page"), related_name="blog_article")
    is_blog_article = models.BooleanField(
        default=False,
        verbose_name=_("This is a blog article"),
        help_text=_("Indicates whether this is a blog article and it should appear on articles list.")
    )
    image = FilerImageField(
        verbose_name=_("Image"),
        blank=True, null=True,
        on_delete=models.SET_NULL,
        help_text=_("The image for the article."),
        related_name="blog_article"
    )
    translations = TranslatedFields(
        small_description=models.TextField(
            blank=True,
            verbose_name=_("Small description"),
            help_text=_(
                "Define a small description to be shown in article list. "
                "This is the text that should capture users attention."
            )
        )
    )

    class Meta:
        verbose_name = _("blog article")
        verbose_name_plural = _("blog articles")
