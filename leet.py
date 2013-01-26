#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import, division
import codecs
from os import mkdir
from os.path import dirname, exists, join, realpath
from shutil import rmtree

import yaml


CURRENT_DIR = dirname(realpath(__file__))
BUILD_DIR = join(CURRENT_DIR, 'build')
TEMPLATES_DIR = join(CURRENT_DIR, 'templates')


def render(template, context):
    result = template

    for k, v in context.iteritems():
        result = result.replace('{{ %s }}' % k, v)

    return result


def _main():
    # read yaml
    with open(join(CURRENT_DIR, 'leet.yaml')) as f:
        leet_list = yaml.load(f)

    # create empty build dir
    if exists(BUILD_DIR):
        rmtree(BUILD_DIR)
    mkdir(BUILD_DIR)

    # create index
    src = join(TEMPLATES_DIR, 'index.html')
    dst = join(BUILD_DIR, 'index.html')
    ctx = {'inner_ul': '\n'.join(
        '<li><a href="%(name)s.html">%(name)s</a></li>' % dct \
        for dct in leet_list)}
    with open(src) as f1, open(dst, 'w') as f2:
        f2.write(render(f1.read(), ctx))

    # create leet files
    with open(join(TEMPLATES_DIR, 'leet.html')) as f:
        template = f.read()

    for dct in leet_list:
        dst = join(BUILD_DIR, '%(name)s.html' % dct)
        with codecs.open(dst, encoding='utf-8', mode='w') as f:
            f.write(render(template, dct))

if __name__ == '__main__':
    _main()
