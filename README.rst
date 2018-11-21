Shuup CMS Blog
==============

CMS Blog addon for Shuup Platform.

Shuup is an Open Source E-Commerce Platform based on Django and Python.

https://shuup.com/


Usage
-----

To use this addon, follow the steps:

- Make sure the addon is installed and enabled.
- Go to admin and create a new CMS Page and put some title e.g. 'Blog' and URL 'blog'. This CMS page will contain the articles list.
- Go to the storefront and access the brand new created blog page.
- As admin user, Edit the page layout using the editor.
- Select the placeholder 'Content in this placeholder is shown for [PAGE TITLE] only.' and from the plugins dropdown select 'Blog Articles List'
- Save and Publish. After this, all blog articles will be listed here.
- Go to admin and start creating blog posts. To do this, create a new CMS page, select the 'Blog Article Page' as the Template and from 'Blog Article' section, check 'This is a blog article'. Put all the relevant informantion you want in the blog post and save.
- The blog post might be accessible from the blog page.

Copyright
---------

Copyright (C) 2012-2018 by Shuup Inc. <support@shuup.com>

Shuup is International Registered Trademark & Property of Shuup Inc.,
Business Address: 1013 Centre Road, Suite 403-B,
Wilmington, Delaware 19805,
United States Of America

License
-------

Shuup CMS Blog is published under Open Software License version 3.0 (OSL-3.0).
See the LICENSE file distributed with Shuup.

Some external libraries and contributions bundled with Shuup may be
published under other compatible licenses. For these, please
refer to the licenses included within each package.

Running tests
-------------

You can run tests with `py.test <http://pytest.org/>`_.

Requirements for running tests:

* Your virtualenv needs to have Shuup installed.
* Project root must be in the Python path.  This can be done with:

  .. code:: sh

     pip install -e .

To run tests, use command:

.. code:: sh

   py.test -v shuup_cms_blog_tests
