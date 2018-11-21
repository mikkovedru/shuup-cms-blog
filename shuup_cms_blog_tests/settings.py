# -*- coding: utf-8 -*-
# This file is part of Shuup CMS Blog Addon.
#
# Copyright (c) 2012-2018, Shuup Inc. All rights reserved.
#
# This source code is licensed under the OSL-3.0 license found in the
# LICENSE file in the root directory of this source tree.
import os
import tempfile

from shuup_workbench.settings.utils import get_disabled_migrations
from shuup_workbench.test_settings import *  # noqa

INSTALLED_APPS = list(locals().get('INSTALLED_APPS', [])) + [
    'shuup_cms_blog'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(tempfile.gettempdir(), 'shuup_cms_blog_tests.sqlite3')
    }
}

MIGRATION_MODULES = get_disabled_migrations()
MIGRATION_MODULES.update({
    'shuup_cms_blog': None
})
