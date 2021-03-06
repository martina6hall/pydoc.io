# -*- coding: utf-8 -*-

import os
import environ
import json
import copy
import logging

log = logging.getLogger(__name__)


#  Whitelist keys that we want to output
KEYS = [
    u'body',
    u'prev',
    u'display_toc',
    u'title',
    u'sourcename',
    u'customsidebar',
    u'current_page_name',
    u'next',
    u'sidebars',
    u'metatags',
    u'meta',
    u'parents',
    u'toc',
    u'alabaster_version',
    u'page_source_suffix'
]


def update_body(app, pagename, templatename, context, doctree):
    outdir = environ.Path(app.config.html_context['output_directory'])
    project = app.config.project
    version = app.config.version
    if not os.path.exists(outdir.root):
        os.makedirs(outdir.root)
    directory_name = "{name}-{version}".format(name=project, version=version)
    json_dir = outdir.path(directory_name)
    if not os.path.exists(json_dir.root):
        os.makedirs(json_dir.root)
    try:
        out_dir = json_dir.path('/'.join(pagename.split('/')[:-1]))
        if not os.path.exists(out_dir()):
            os.makedirs(out_dir())
        out_file = json_dir.path(pagename + '.json')
        to_write = open(out_file(), 'w+')
        to_context = copy.copy(context)
        # Use list here so we don't get an error on changing dict during iteration
        for key in list(context):
            if key not in KEYS:
                del to_context[key]
        to_write.write(json.dumps(to_context, indent=4))
    except Exception:
        log.exception('Failure in JSON search dump')


def add_ga_javascript(app, pagename, templatename, context, doctree):
    """
    From the sphinxcontrib.googleanalytics package
    """
    if not app.config.googleanalytics_enabled:
        return

    metatags = context.get('metatags', '')
    metatags += """<script type="text/javascript">

      var _gaq = _gaq || [];
      _gaq.push(['_setAccount', '%s']);
      _gaq.push(['_trackPageview']);

      (function() {
        var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
        ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + \
            '.google-analytics.com/ga.js';
        var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
      })();
    </script>""" % app.config.googleanalytics_id
    context['metatags'] = metatags


def setup(app):
    app.connect('html-page-context', update_body)
    app.add_config_value('googleanalytics_id', '', 'html')
    app.add_config_value('googleanalytics_enabled', True, 'html')
    app.connect('html-page-context', add_ga_javascript)
