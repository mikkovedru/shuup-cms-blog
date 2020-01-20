# -*- coding: utf-8 -*-
# This file is part of Shuup CMS Blog Addon.
#
# Copyright (c) 2012-2018, Shuup Inc. All rights reserved.
#
# This source code is licensed under the OSL-3.0 license found in the
# LICENSE file in the root directory of this source tree.
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView, View

from shuup.front.views.dashboard import DashboardViewMixin
from shuup.simple_cms.models import Page


class SavedArticlesView(DashboardViewMixin, TemplateView):
    template_name = "shuup_cms_blog/saved_articles_dashboard_item.jinja"

    def get_context_data(self, **kwargs):
        context = super(SavedArticlesView, self).get_context_data()
        context["saved_articles"] = []
        request = self.request

        if request.customer and request.customer.options and request.customer.options.get("saved_articles"):
            context["saved_articles"] = Page.objects.filter(pk__in=request.customer.options["saved_articles"])

        return context


class RemoveSavedArticlesView(View):
    def get(self, request, **kwargs):
        if not request.customer or not kwargs.get("pk"):
            return HttpResponseRedirect(reverse("shuup:index"))

        pk = int(kwargs.get("pk"))
        saved_articles = (request.customer.options and request.customer.options.get("saved_articles")) or []

        if pk and pk in saved_articles:
            saved_articles.remove(pk)
            request.customer.options["saved_articles"] = saved_articles
            request.customer.save()
            messages.success(request, _("Article removed."))

        if request.GET.get("next"):
            return HttpResponseRedirect(request.GET.get("next"))

        return HttpResponseRedirect(reverse("shuup:shuup-cms-blog.saved-articles"))


class AddSavedArticlesView(View):
    def get(self, request, **kwargs):
        if not request.customer or not kwargs.get("pk"):
            return HttpResponseRedirect(reverse("shuup:index"))

        pk = int(kwargs.get("pk"))
        saved_articles = (request.customer.options and request.customer.options.get("saved_articles")) or []

        if pk and pk not in saved_articles:
            saved_articles.append(pk)
            request.customer.options = request.customer.options or {}
            request.customer.options["saved_articles"] = saved_articles
            request.customer.save()
            messages.success(request, _("Article saved."))

        if request.GET.get("next"):
            return HttpResponseRedirect(request.GET.get("next"))

        return HttpResponseRedirect(reverse("shuup:shuup-cms-blog.saved-articles"))
