#!/usr/bin/env python3

import os
"""
    Minifies json database file
    Uses third party tool jsmin
    Typical reduction from 30 MB -> 8 MB!
"""

# need third party minifier
try:
    from jsmin import jsmin
except:
    print("Requires third party lib - jsmin, do 'pip3 install jsmin'")


jsondir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
    '..', 'reference')
jsonmindir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
    '..', 'actigamma', 'data')
jsonfilename = 'lines_decay_2012.json'

if jsonfilename.endswith('.json') and not jsonfilename.endswith(".min{}".format('.json')):
    # minify
    print("minifying...")
    with open(os.path.join(jsondir, jsonfilename)) as js_file:
        with open(os.path.join(jsonmindir, "{}.min{}".format(jsonfilename[:-5], '.json')), "w") as min_file:
            min_file.write(jsmin(js_file.read()))
