import os
import sys
from pprint import pformat

from matrix import Entry
from matrix import from_file
from matrix import from_string
from matrix import parse_config
from matrix.cli import main


def here(path):
    return os.path.join(os.path.dirname(__file__), path)


def strip_stupid_unicode_prefix(gunk):
    if sys.version_info[:2] == (2, 7):
        return gunk.replace("u'", "'")
    else:
        return gunk


def test_cli(monkeypatch, tmpdir):
    monkeypatch.setattr(sys, 'argv', ['matrix-render', '-c', 'tests/sample.cfg', '-s', 'config', 'tests/template.txt', '-d', str(tmpdir)])
    main()
    output = tmpdir.join('template.txt').read()
    print(output)
    assert set(strip_stupid_unicode_prefix(output).splitlines()) == set(
        (
            "-13: [('bar', '3'), ('foo', '1')]",
            "-14: [('bar', '4'), ('foo', '1')]",
            "-23: [('bar', '3'), ('foo', '2')]",
            "-24: [('bar', '4'), ('foo', '2')]",
        )
    )


def test_parse_1():
    assert str(Entry("alias: val1 val2 val3")) == "Entry('val1 val2 val3', alias='alias')"


def test_parse_2():
    assert (
        str(Entry("alias: val1 val2 val3 !exclude1[eglob1] &include1[iglob1] !exclude2[eglob2] &include2[iglob2]"))
        == "Entry('val1 val2 val3', exclude(exclude1[eglob1]), include(include1[iglob1]), exclude(exclude2[eglob2]),"
        " include(include2[iglob2]), alias='alias')"
    )


def test_parse_3():
    assert (
        str(Entry("alias: val1 val2 val3 !exclude1[eglob1!&] &include1[iglob1!&]"))
        == "Entry('val1 val2 val3', exclude(exclude1[eglob1!&]), include(include1[iglob1!&]), alias='alias')"
    )


def test_parse_4():
    assert str(Entry("alias: val1 val2 val3 !exclude1[] &include1[]")) == "Entry('val1 val2 val3', alias='alias')"


def test_parse_file_1():
    with open(here('config_1.ini')) as fh:
        assert (
            strip_stupid_unicode_prefix(pformat(dict(parse_config(fh))))
            == """{'coverage_flags': [Entry('true', alias='cover'),
                    Entry('false', alias='nocover')],
 'dependencies': [Entry('python-signalfd', alias='python-signalfd'),
                  Entry('python-signalfd gevent', exclude(python_versions[3.*]), alias='python-signalfd_gevent'),
                  Entry('python-signalfd eventlet', exclude(python_versions[3.*]), alias='python-signalfd_eventlet'),
                  Entry('eventlet', exclude(python_versions[3.*]), alias='eventlet'),
                  Entry('gevent', exclude(python_versions[3.*]), alias='gevent'),
                  Entry('', alias='')],
 'environment_variables': [Entry('PATCH_THREAD=yes', include(dependencies[*event*]), alias='patchthread'),
                           Entry('', alias='')],
 'python_versions': [Entry('2.7', alias='2.7'),
                     Entry('2.6', alias='2.6'),
                     Entry('3.2', alias='3.2'),
                     Entry('3.3', alias='3.3'),
                     Entry('3.4', alias='3.4'),
                     Entry('pypy', alias='pypy')]}"""
        )


def test_parse_file_2():
    with open(here('config_2.ini')) as fh:
        assert (
            strip_stupid_unicode_prefix(pformat(dict(parse_config(fh)), width=100))
            == """{'coverage_flags': [Entry('true', alias=''), Entry('false', alias='nocover')],
 'depencencies': [Entry('Django==1.3.7', exclude(python_versions[3.*]), alias='1.3'),
                  Entry('Django==1.4.13', exclude(python_versions[3.*]), alias='1.4'),
                  Entry('Django==1.5.8', alias='1.5'),
                  Entry('Django==1.6.5', alias='1.6'),
                  Entry('https://www.djangoproject.com/download/1.7.b4/tarball/', exclude(python_versions[2.6]), alias='1.7')],
 'environment_variables': [Entry('', alias='')],
 'python_versions': [Entry('2.6', alias='2.6'),
                     Entry('2.7', alias='2.7'),
                     Entry('3.3', alias='3.3'),
                     Entry('3.4', alias='3.4'),
                     Entry('pypy', alias='pypy')]}"""
        )


def test_parse_file_3():
    with open(here('config_3.ini')) as fh:
        assert (
            strip_stupid_unicode_prefix(pformat(dict(parse_config(fh)), width=100))
            == """{'coverage_flags': [Entry('true', alias=''), Entry('false', alias='nocover')],
 'depencencies': [Entry('Django==1.3.7', exclude(python_versions[3.*]), alias='Django==1.3.7'),
                  Entry('Django==1.4.13', exclude(python_versions[3.*]), alias='Django==1.4.13'),
                  Entry('Django==1.5.8', alias='Django==1.5.8'),
                  Entry('Django==1.6.5', alias='Django==1.6.5'),
                  Entry('https://www.djangoproject.com/download/1.7.b4/tarball/', exclude(python_versions[2.6]), alias='Django==1.7')],
 'environment_variables': [Entry('', alias='')],
 'python_versions': [Entry('2.6', alias='2.6'),
                     Entry('2.7', alias='2.7'),
                     Entry('3.3', alias='3.3'),
                     Entry('3.4', alias='3.4'),
                     Entry('pypy', alias='pypy')]}"""
        )


def test_make_matrix_1():
    assert from_file(here('config_1.ini')) == {
        '2.6-cover': {'coverage_flags': 'true', 'dependencies': '', 'environment_variables': '', 'python_versions': '2.6'},
        '2.6-eventlet-cover': {'coverage_flags': 'true', 'dependencies': 'eventlet', 'environment_variables': '', 'python_versions': '2.6'},
        '2.6-eventlet-cover-patchthread': {
            'coverage_flags': 'true',
            'dependencies': 'eventlet',
            'environment_variables': 'PATCH_THREAD=yes',
            'python_versions': '2.6',
        },
        '2.6-eventlet-nocover': {
            'coverage_flags': 'false',
            'dependencies': 'eventlet',
            'environment_variables': '',
            'python_versions': '2.6',
        },
        '2.6-eventlet-nocover-patchthread': {
            'coverage_flags': 'false',
            'dependencies': 'eventlet',
            'environment_variables': 'PATCH_THREAD=yes',
            'python_versions': '2.6',
        },
        '2.6-gevent-cover': {'coverage_flags': 'true', 'dependencies': 'gevent', 'environment_variables': '', 'python_versions': '2.6'},
        '2.6-gevent-cover-patchthread': {
            'coverage_flags': 'true',
            'dependencies': 'gevent',
            'environment_variables': 'PATCH_THREAD=yes',
            'python_versions': '2.6',
        },
        '2.6-gevent-nocover': {'coverage_flags': 'false', 'dependencies': 'gevent', 'environment_variables': '', 'python_versions': '2.6'},
        '2.6-gevent-nocover-patchthread': {
            'coverage_flags': 'false',
            'dependencies': 'gevent',
            'environment_variables': 'PATCH_THREAD=yes',
            'python_versions': '2.6',
        },
        '2.6-nocover': {'coverage_flags': 'false', 'dependencies': '', 'environment_variables': '', 'python_versions': '2.6'},
        '2.6-python-signalfd-cover': {
            'coverage_flags': 'true',
            'dependencies': 'python-signalfd',
            'environment_variables': '',
            'python_versions': '2.6',
        },
        '2.6-python-signalfd-nocover': {
            'coverage_flags': 'false',
            'dependencies': 'python-signalfd',
            'environment_variables': '',
            'python_versions': '2.6',
        },
        '2.6-python-signalfd_eventlet-cover': {
            'coverage_flags': 'true',
            'dependencies': 'python-signalfd eventlet',
            'environment_variables': '',
            'python_versions': '2.6',
        },
        '2.6-python-signalfd_eventlet-cover-patchthread': {
            'coverage_flags': 'true',
            'dependencies': 'python-signalfd eventlet',
            'environment_variables': 'PATCH_THREAD=yes',
            'python_versions': '2.6',
        },
        '2.6-python-signalfd_eventlet-nocover': {
            'coverage_flags': 'false',
            'dependencies': 'python-signalfd eventlet',
            'environment_variables': '',
            'python_versions': '2.6',
        },
        '2.6-python-signalfd_eventlet-nocover-patchthread': {
            'coverage_flags': 'false',
            'dependencies': 'python-signalfd eventlet',
            'environment_variables': 'PATCH_THREAD=yes',
            'python_versions': '2.6',
        },
        '2.6-python-signalfd_gevent-cover': {
            'coverage_flags': 'true',
            'dependencies': 'python-signalfd gevent',
            'environment_variables': '',
            'python_versions': '2.6',
        },
        '2.6-python-signalfd_gevent-cover-patchthread': {
            'coverage_flags': 'true',
            'dependencies': 'python-signalfd gevent',
            'environment_variables': 'PATCH_THREAD=yes',
            'python_versions': '2.6',
        },
        '2.6-python-signalfd_gevent-nocover': {
            'coverage_flags': 'false',
            'dependencies': 'python-signalfd gevent',
            'environment_variables': '',
            'python_versions': '2.6',
        },
        '2.6-python-signalfd_gevent-nocover-patchthread': {
            'coverage_flags': 'false',
            'dependencies': 'python-signalfd gevent',
            'environment_variables': 'PATCH_THREAD=yes',
            'python_versions': '2.6',
        },
        '2.7-cover': {'coverage_flags': 'true', 'dependencies': '', 'environment_variables': '', 'python_versions': '2.7'},
        '2.7-eventlet-cover': {'coverage_flags': 'true', 'dependencies': 'eventlet', 'environment_variables': '', 'python_versions': '2.7'},
        '2.7-eventlet-cover-patchthread': {
            'coverage_flags': 'true',
            'dependencies': 'eventlet',
            'environment_variables': 'PATCH_THREAD=yes',
            'python_versions': '2.7',
        },
        '2.7-eventlet-nocover': {
            'coverage_flags': 'false',
            'dependencies': 'eventlet',
            'environment_variables': '',
            'python_versions': '2.7',
        },
        '2.7-eventlet-nocover-patchthread': {
            'coverage_flags': 'false',
            'dependencies': 'eventlet',
            'environment_variables': 'PATCH_THREAD=yes',
            'python_versions': '2.7',
        },
        '2.7-gevent-cover': {'coverage_flags': 'true', 'dependencies': 'gevent', 'environment_variables': '', 'python_versions': '2.7'},
        '2.7-gevent-cover-patchthread': {
            'coverage_flags': 'true',
            'dependencies': 'gevent',
            'environment_variables': 'PATCH_THREAD=yes',
            'python_versions': '2.7',
        },
        '2.7-gevent-nocover': {'coverage_flags': 'false', 'dependencies': 'gevent', 'environment_variables': '', 'python_versions': '2.7'},
        '2.7-gevent-nocover-patchthread': {
            'coverage_flags': 'false',
            'dependencies': 'gevent',
            'environment_variables': 'PATCH_THREAD=yes',
            'python_versions': '2.7',
        },
        '2.7-nocover': {'coverage_flags': 'false', 'dependencies': '', 'environment_variables': '', 'python_versions': '2.7'},
        '2.7-python-signalfd-cover': {
            'coverage_flags': 'true',
            'dependencies': 'python-signalfd',
            'environment_variables': '',
            'python_versions': '2.7',
        },
        '2.7-python-signalfd-nocover': {
            'coverage_flags': 'false',
            'dependencies': 'python-signalfd',
            'environment_variables': '',
            'python_versions': '2.7',
        },
        '2.7-python-signalfd_eventlet-cover': {
            'coverage_flags': 'true',
            'dependencies': 'python-signalfd eventlet',
            'environment_variables': '',
            'python_versions': '2.7',
        },
        '2.7-python-signalfd_eventlet-cover-patchthread': {
            'coverage_flags': 'true',
            'dependencies': 'python-signalfd eventlet',
            'environment_variables': 'PATCH_THREAD=yes',
            'python_versions': '2.7',
        },
        '2.7-python-signalfd_eventlet-nocover': {
            'coverage_flags': 'false',
            'dependencies': 'python-signalfd eventlet',
            'environment_variables': '',
            'python_versions': '2.7',
        },
        '2.7-python-signalfd_eventlet-nocover-patchthread': {
            'coverage_flags': 'false',
            'dependencies': 'python-signalfd eventlet',
            'environment_variables': 'PATCH_THREAD=yes',
            'python_versions': '2.7',
        },
        '2.7-python-signalfd_gevent-cover': {
            'coverage_flags': 'true',
            'dependencies': 'python-signalfd gevent',
            'environment_variables': '',
            'python_versions': '2.7',
        },
        '2.7-python-signalfd_gevent-cover-patchthread': {
            'coverage_flags': 'true',
            'dependencies': 'python-signalfd gevent',
            'environment_variables': 'PATCH_THREAD=yes',
            'python_versions': '2.7',
        },
        '2.7-python-signalfd_gevent-nocover': {
            'coverage_flags': 'false',
            'dependencies': 'python-signalfd gevent',
            'environment_variables': '',
            'python_versions': '2.7',
        },
        '2.7-python-signalfd_gevent-nocover-patchthread': {
            'coverage_flags': 'false',
            'dependencies': 'python-signalfd gevent',
            'environment_variables': 'PATCH_THREAD=yes',
            'python_versions': '2.7',
        },
        '3.2-cover': {'coverage_flags': 'true', 'dependencies': '', 'environment_variables': '', 'python_versions': '3.2'},
        '3.2-nocover': {'coverage_flags': 'false', 'dependencies': '', 'environment_variables': '', 'python_versions': '3.2'},
        '3.2-python-signalfd-cover': {
            'coverage_flags': 'true',
            'dependencies': 'python-signalfd',
            'environment_variables': '',
            'python_versions': '3.2',
        },
        '3.2-python-signalfd-nocover': {
            'coverage_flags': 'false',
            'dependencies': 'python-signalfd',
            'environment_variables': '',
            'python_versions': '3.2',
        },
        '3.3-cover': {'coverage_flags': 'true', 'dependencies': '', 'environment_variables': '', 'python_versions': '3.3'},
        '3.3-nocover': {'coverage_flags': 'false', 'dependencies': '', 'environment_variables': '', 'python_versions': '3.3'},
        '3.3-python-signalfd-cover': {
            'coverage_flags': 'true',
            'dependencies': 'python-signalfd',
            'environment_variables': '',
            'python_versions': '3.3',
        },
        '3.3-python-signalfd-nocover': {
            'coverage_flags': 'false',
            'dependencies': 'python-signalfd',
            'environment_variables': '',
            'python_versions': '3.3',
        },
        '3.4-cover': {'coverage_flags': 'true', 'dependencies': '', 'environment_variables': '', 'python_versions': '3.4'},
        '3.4-nocover': {'coverage_flags': 'false', 'dependencies': '', 'environment_variables': '', 'python_versions': '3.4'},
        '3.4-python-signalfd-cover': {
            'coverage_flags': 'true',
            'dependencies': 'python-signalfd',
            'environment_variables': '',
            'python_versions': '3.4',
        },
        '3.4-python-signalfd-nocover': {
            'coverage_flags': 'false',
            'dependencies': 'python-signalfd',
            'environment_variables': '',
            'python_versions': '3.4',
        },
        'pypy-cover': {'coverage_flags': 'true', 'dependencies': '', 'environment_variables': '', 'python_versions': 'pypy'},
        'pypy-eventlet-cover': {
            'coverage_flags': 'true',
            'dependencies': 'eventlet',
            'environment_variables': '',
            'python_versions': 'pypy',
        },
        'pypy-eventlet-cover-patchthread': {
            'coverage_flags': 'true',
            'dependencies': 'eventlet',
            'environment_variables': 'PATCH_THREAD=yes',
            'python_versions': 'pypy',
        },
        'pypy-eventlet-nocover': {
            'coverage_flags': 'false',
            'dependencies': 'eventlet',
            'environment_variables': '',
            'python_versions': 'pypy',
        },
        'pypy-eventlet-nocover-patchthread': {
            'coverage_flags': 'false',
            'dependencies': 'eventlet',
            'environment_variables': 'PATCH_THREAD=yes',
            'python_versions': 'pypy',
        },
        'pypy-gevent-cover': {'coverage_flags': 'true', 'dependencies': 'gevent', 'environment_variables': '', 'python_versions': 'pypy'},
        'pypy-gevent-cover-patchthread': {
            'coverage_flags': 'true',
            'dependencies': 'gevent',
            'environment_variables': 'PATCH_THREAD=yes',
            'python_versions': 'pypy',
        },
        'pypy-gevent-nocover': {
            'coverage_flags': 'false',
            'dependencies': 'gevent',
            'environment_variables': '',
            'python_versions': 'pypy',
        },
        'pypy-gevent-nocover-patchthread': {
            'coverage_flags': 'false',
            'dependencies': 'gevent',
            'environment_variables': 'PATCH_THREAD=yes',
            'python_versions': 'pypy',
        },
        'pypy-nocover': {'coverage_flags': 'false', 'dependencies': '', 'environment_variables': '', 'python_versions': 'pypy'},
        'pypy-python-signalfd-cover': {
            'coverage_flags': 'true',
            'dependencies': 'python-signalfd',
            'environment_variables': '',
            'python_versions': 'pypy',
        },
        'pypy-python-signalfd-nocover': {
            'coverage_flags': 'false',
            'dependencies': 'python-signalfd',
            'environment_variables': '',
            'python_versions': 'pypy',
        },
        'pypy-python-signalfd_eventlet-cover': {
            'coverage_flags': 'true',
            'dependencies': 'python-signalfd eventlet',
            'environment_variables': '',
            'python_versions': 'pypy',
        },
        'pypy-python-signalfd_eventlet-cover-patchthread': {
            'coverage_flags': 'true',
            'dependencies': 'python-signalfd eventlet',
            'environment_variables': 'PATCH_THREAD=yes',
            'python_versions': 'pypy',
        },
        'pypy-python-signalfd_eventlet-nocover': {
            'coverage_flags': 'false',
            'dependencies': 'python-signalfd eventlet',
            'environment_variables': '',
            'python_versions': 'pypy',
        },
        'pypy-python-signalfd_eventlet-nocover-patchthread': {
            'coverage_flags': 'false',
            'dependencies': 'python-signalfd eventlet',
            'environment_variables': 'PATCH_THREAD=yes',
            'python_versions': 'pypy',
        },
        'pypy-python-signalfd_gevent-cover': {
            'coverage_flags': 'true',
            'dependencies': 'python-signalfd gevent',
            'environment_variables': '',
            'python_versions': 'pypy',
        },
        'pypy-python-signalfd_gevent-cover-patchthread': {
            'coverage_flags': 'true',
            'dependencies': 'python-signalfd gevent',
            'environment_variables': 'PATCH_THREAD=yes',
            'python_versions': 'pypy',
        },
        'pypy-python-signalfd_gevent-nocover': {
            'coverage_flags': 'false',
            'dependencies': 'python-signalfd gevent',
            'environment_variables': '',
            'python_versions': 'pypy',
        },
        'pypy-python-signalfd_gevent-nocover-patchthread': {
            'coverage_flags': 'false',
            'dependencies': 'python-signalfd gevent',
            'environment_variables': 'PATCH_THREAD=yes',
            'python_versions': 'pypy',
        },
    }


def test_make_matrix_2():
    assert from_file(here('config_2.ini')) == {
        '2.6-1.3': {'coverage_flags': 'true', 'depencencies': 'Django==1.3.7', 'environment_variables': '', 'python_versions': '2.6'},
        '2.6-1.3-nocover': {
            'coverage_flags': 'false',
            'depencencies': 'Django==1.3.7',
            'environment_variables': '',
            'python_versions': '2.6',
        },
        '2.6-1.4': {'coverage_flags': 'true', 'depencencies': 'Django==1.4.13', 'environment_variables': '', 'python_versions': '2.6'},
        '2.6-1.4-nocover': {
            'coverage_flags': 'false',
            'depencencies': 'Django==1.4.13',
            'environment_variables': '',
            'python_versions': '2.6',
        },
        '2.6-1.5': {'coverage_flags': 'true', 'depencencies': 'Django==1.5.8', 'environment_variables': '', 'python_versions': '2.6'},
        '2.6-1.5-nocover': {
            'coverage_flags': 'false',
            'depencencies': 'Django==1.5.8',
            'environment_variables': '',
            'python_versions': '2.6',
        },
        '2.6-1.6': {'coverage_flags': 'true', 'depencencies': 'Django==1.6.5', 'environment_variables': '', 'python_versions': '2.6'},
        '2.6-1.6-nocover': {
            'coverage_flags': 'false',
            'depencencies': 'Django==1.6.5',
            'environment_variables': '',
            'python_versions': '2.6',
        },
        '2.7-1.3': {'coverage_flags': 'true', 'depencencies': 'Django==1.3.7', 'environment_variables': '', 'python_versions': '2.7'},
        '2.7-1.3-nocover': {
            'coverage_flags': 'false',
            'depencencies': 'Django==1.3.7',
            'environment_variables': '',
            'python_versions': '2.7',
        },
        '2.7-1.4': {'coverage_flags': 'true', 'depencencies': 'Django==1.4.13', 'environment_variables': '', 'python_versions': '2.7'},
        '2.7-1.4-nocover': {
            'coverage_flags': 'false',
            'depencencies': 'Django==1.4.13',
            'environment_variables': '',
            'python_versions': '2.7',
        },
        '2.7-1.5': {'coverage_flags': 'true', 'depencencies': 'Django==1.5.8', 'environment_variables': '', 'python_versions': '2.7'},
        '2.7-1.5-nocover': {
            'coverage_flags': 'false',
            'depencencies': 'Django==1.5.8',
            'environment_variables': '',
            'python_versions': '2.7',
        },
        '2.7-1.6': {'coverage_flags': 'true', 'depencencies': 'Django==1.6.5', 'environment_variables': '', 'python_versions': '2.7'},
        '2.7-1.6-nocover': {
            'coverage_flags': 'false',
            'depencencies': 'Django==1.6.5',
            'environment_variables': '',
            'python_versions': '2.7',
        },
        '2.7-1.7': {
            'coverage_flags': 'true',
            'depencencies': 'https://www.djangoproject.com/download/1.7.b4/tarball/',
            'environment_variables': '',
            'python_versions': '2.7',
        },
        '2.7-1.7-nocover': {
            'coverage_flags': 'false',
            'depencencies': 'https://www.djangoproject.com/download/1.7.b4/tarball/',
            'environment_variables': '',
            'python_versions': '2.7',
        },
        '3.3-1.5': {'coverage_flags': 'true', 'depencencies': 'Django==1.5.8', 'environment_variables': '', 'python_versions': '3.3'},
        '3.3-1.5-nocover': {
            'coverage_flags': 'false',
            'depencencies': 'Django==1.5.8',
            'environment_variables': '',
            'python_versions': '3.3',
        },
        '3.3-1.6': {'coverage_flags': 'true', 'depencencies': 'Django==1.6.5', 'environment_variables': '', 'python_versions': '3.3'},
        '3.3-1.6-nocover': {
            'coverage_flags': 'false',
            'depencencies': 'Django==1.6.5',
            'environment_variables': '',
            'python_versions': '3.3',
        },
        '3.3-1.7': {
            'coverage_flags': 'true',
            'depencencies': 'https://www.djangoproject.com/download/1.7.b4/tarball/',
            'environment_variables': '',
            'python_versions': '3.3',
        },
        '3.3-1.7-nocover': {
            'coverage_flags': 'false',
            'depencencies': 'https://www.djangoproject.com/download/1.7.b4/tarball/',
            'environment_variables': '',
            'python_versions': '3.3',
        },
        '3.4-1.5': {'coverage_flags': 'true', 'depencencies': 'Django==1.5.8', 'environment_variables': '', 'python_versions': '3.4'},
        '3.4-1.5-nocover': {
            'coverage_flags': 'false',
            'depencencies': 'Django==1.5.8',
            'environment_variables': '',
            'python_versions': '3.4',
        },
        '3.4-1.6': {'coverage_flags': 'true', 'depencencies': 'Django==1.6.5', 'environment_variables': '', 'python_versions': '3.4'},
        '3.4-1.6-nocover': {
            'coverage_flags': 'false',
            'depencencies': 'Django==1.6.5',
            'environment_variables': '',
            'python_versions': '3.4',
        },
        '3.4-1.7': {
            'coverage_flags': 'true',
            'depencencies': 'https://www.djangoproject.com/download/1.7.b4/tarball/',
            'environment_variables': '',
            'python_versions': '3.4',
        },
        '3.4-1.7-nocover': {
            'coverage_flags': 'false',
            'depencencies': 'https://www.djangoproject.com/download/1.7.b4/tarball/',
            'environment_variables': '',
            'python_versions': '3.4',
        },
        'pypy-1.3': {'coverage_flags': 'true', 'depencencies': 'Django==1.3.7', 'environment_variables': '', 'python_versions': 'pypy'},
        'pypy-1.3-nocover': {
            'coverage_flags': 'false',
            'depencencies': 'Django==1.3.7',
            'environment_variables': '',
            'python_versions': 'pypy',
        },
        'pypy-1.4': {'coverage_flags': 'true', 'depencencies': 'Django==1.4.13', 'environment_variables': '', 'python_versions': 'pypy'},
        'pypy-1.4-nocover': {
            'coverage_flags': 'false',
            'depencencies': 'Django==1.4.13',
            'environment_variables': '',
            'python_versions': 'pypy',
        },
        'pypy-1.5': {'coverage_flags': 'true', 'depencencies': 'Django==1.5.8', 'environment_variables': '', 'python_versions': 'pypy'},
        'pypy-1.5-nocover': {
            'coverage_flags': 'false',
            'depencencies': 'Django==1.5.8',
            'environment_variables': '',
            'python_versions': 'pypy',
        },
        'pypy-1.6': {'coverage_flags': 'true', 'depencencies': 'Django==1.6.5', 'environment_variables': '', 'python_versions': 'pypy'},
        'pypy-1.6-nocover': {
            'coverage_flags': 'false',
            'depencencies': 'Django==1.6.5',
            'environment_variables': '',
            'python_versions': 'pypy',
        },
        'pypy-1.7': {
            'coverage_flags': 'true',
            'depencencies': 'https://www.djangoproject.com/download/1.7.b4/tarball/',
            'environment_variables': '',
            'python_versions': 'pypy',
        },
        'pypy-1.7-nocover': {
            'coverage_flags': 'false',
            'depencencies': 'https://www.djangoproject.com/download/1.7.b4/tarball/',
            'environment_variables': '',
            'python_versions': 'pypy',
        },
    }


def test_make_matrix_3():
    assert from_file(here('config_3.ini')) == {
        '2.6-Django==1.3.7': {
            'coverage_flags': 'true',
            'depencencies': 'Django==1.3.7',
            'environment_variables': '',
            'python_versions': '2.6',
        },
        '2.6-Django==1.3.7-nocover': {
            'coverage_flags': 'false',
            'depencencies': 'Django==1.3.7',
            'environment_variables': '',
            'python_versions': '2.6',
        },
        '2.6-Django==1.4.13': {
            'coverage_flags': 'true',
            'depencencies': 'Django==1.4.13',
            'environment_variables': '',
            'python_versions': '2.6',
        },
        '2.6-Django==1.4.13-nocover': {
            'coverage_flags': 'false',
            'depencencies': 'Django==1.4.13',
            'environment_variables': '',
            'python_versions': '2.6',
        },
        '2.6-Django==1.5.8': {
            'coverage_flags': 'true',
            'depencencies': 'Django==1.5.8',
            'environment_variables': '',
            'python_versions': '2.6',
        },
        '2.6-Django==1.5.8-nocover': {
            'coverage_flags': 'false',
            'depencencies': 'Django==1.5.8',
            'environment_variables': '',
            'python_versions': '2.6',
        },
        '2.6-Django==1.6.5': {
            'coverage_flags': 'true',
            'depencencies': 'Django==1.6.5',
            'environment_variables': '',
            'python_versions': '2.6',
        },
        '2.6-Django==1.6.5-nocover': {
            'coverage_flags': 'false',
            'depencencies': 'Django==1.6.5',
            'environment_variables': '',
            'python_versions': '2.6',
        },
        '2.7-Django==1.3.7': {
            'coverage_flags': 'true',
            'depencencies': 'Django==1.3.7',
            'environment_variables': '',
            'python_versions': '2.7',
        },
        '2.7-Django==1.3.7-nocover': {
            'coverage_flags': 'false',
            'depencencies': 'Django==1.3.7',
            'environment_variables': '',
            'python_versions': '2.7',
        },
        '2.7-Django==1.4.13': {
            'coverage_flags': 'true',
            'depencencies': 'Django==1.4.13',
            'environment_variables': '',
            'python_versions': '2.7',
        },
        '2.7-Django==1.4.13-nocover': {
            'coverage_flags': 'false',
            'depencencies': 'Django==1.4.13',
            'environment_variables': '',
            'python_versions': '2.7',
        },
        '2.7-Django==1.5.8': {
            'coverage_flags': 'true',
            'depencencies': 'Django==1.5.8',
            'environment_variables': '',
            'python_versions': '2.7',
        },
        '2.7-Django==1.5.8-nocover': {
            'coverage_flags': 'false',
            'depencencies': 'Django==1.5.8',
            'environment_variables': '',
            'python_versions': '2.7',
        },
        '2.7-Django==1.6.5': {
            'coverage_flags': 'true',
            'depencencies': 'Django==1.6.5',
            'environment_variables': '',
            'python_versions': '2.7',
        },
        '2.7-Django==1.6.5-nocover': {
            'coverage_flags': 'false',
            'depencencies': 'Django==1.6.5',
            'environment_variables': '',
            'python_versions': '2.7',
        },
        '2.7-Django==1.7': {
            'coverage_flags': 'true',
            'depencencies': 'https://www.djangoproject.com/download/1.7.b4/tarball/',
            'environment_variables': '',
            'python_versions': '2.7',
        },
        '2.7-Django==1.7-nocover': {
            'coverage_flags': 'false',
            'depencencies': 'https://www.djangoproject.com/download/1.7.b4/tarball/',
            'environment_variables': '',
            'python_versions': '2.7',
        },
        '3.3-Django==1.5.8': {
            'coverage_flags': 'true',
            'depencencies': 'Django==1.5.8',
            'environment_variables': '',
            'python_versions': '3.3',
        },
        '3.3-Django==1.5.8-nocover': {
            'coverage_flags': 'false',
            'depencencies': 'Django==1.5.8',
            'environment_variables': '',
            'python_versions': '3.3',
        },
        '3.3-Django==1.6.5': {
            'coverage_flags': 'true',
            'depencencies': 'Django==1.6.5',
            'environment_variables': '',
            'python_versions': '3.3',
        },
        '3.3-Django==1.6.5-nocover': {
            'coverage_flags': 'false',
            'depencencies': 'Django==1.6.5',
            'environment_variables': '',
            'python_versions': '3.3',
        },
        '3.3-Django==1.7': {
            'coverage_flags': 'true',
            'depencencies': 'https://www.djangoproject.com/download/1.7.b4/tarball/',
            'environment_variables': '',
            'python_versions': '3.3',
        },
        '3.3-Django==1.7-nocover': {
            'coverage_flags': 'false',
            'depencencies': 'https://www.djangoproject.com/download/1.7.b4/tarball/',
            'environment_variables': '',
            'python_versions': '3.3',
        },
        '3.4-Django==1.5.8': {
            'coverage_flags': 'true',
            'depencencies': 'Django==1.5.8',
            'environment_variables': '',
            'python_versions': '3.4',
        },
        '3.4-Django==1.5.8-nocover': {
            'coverage_flags': 'false',
            'depencencies': 'Django==1.5.8',
            'environment_variables': '',
            'python_versions': '3.4',
        },
        '3.4-Django==1.6.5': {
            'coverage_flags': 'true',
            'depencencies': 'Django==1.6.5',
            'environment_variables': '',
            'python_versions': '3.4',
        },
        '3.4-Django==1.6.5-nocover': {
            'coverage_flags': 'false',
            'depencencies': 'Django==1.6.5',
            'environment_variables': '',
            'python_versions': '3.4',
        },
        '3.4-Django==1.7': {
            'coverage_flags': 'true',
            'depencencies': 'https://www.djangoproject.com/download/1.7.b4/tarball/',
            'environment_variables': '',
            'python_versions': '3.4',
        },
        '3.4-Django==1.7-nocover': {
            'coverage_flags': 'false',
            'depencencies': 'https://www.djangoproject.com/download/1.7.b4/tarball/',
            'environment_variables': '',
            'python_versions': '3.4',
        },
        'pypy-Django==1.3.7': {
            'coverage_flags': 'true',
            'depencencies': 'Django==1.3.7',
            'environment_variables': '',
            'python_versions': 'pypy',
        },
        'pypy-Django==1.3.7-nocover': {
            'coverage_flags': 'false',
            'depencencies': 'Django==1.3.7',
            'environment_variables': '',
            'python_versions': 'pypy',
        },
        'pypy-Django==1.4.13': {
            'coverage_flags': 'true',
            'depencencies': 'Django==1.4.13',
            'environment_variables': '',
            'python_versions': 'pypy',
        },
        'pypy-Django==1.4.13-nocover': {
            'coverage_flags': 'false',
            'depencencies': 'Django==1.4.13',
            'environment_variables': '',
            'python_versions': 'pypy',
        },
        'pypy-Django==1.5.8': {
            'coverage_flags': 'true',
            'depencencies': 'Django==1.5.8',
            'environment_variables': '',
            'python_versions': 'pypy',
        },
        'pypy-Django==1.5.8-nocover': {
            'coverage_flags': 'false',
            'depencencies': 'Django==1.5.8',
            'environment_variables': '',
            'python_versions': 'pypy',
        },
        'pypy-Django==1.6.5': {
            'coverage_flags': 'true',
            'depencencies': 'Django==1.6.5',
            'environment_variables': '',
            'python_versions': 'pypy',
        },
        'pypy-Django==1.6.5-nocover': {
            'coverage_flags': 'false',
            'depencencies': 'Django==1.6.5',
            'environment_variables': '',
            'python_versions': 'pypy',
        },
        'pypy-Django==1.7': {
            'coverage_flags': 'true',
            'depencencies': 'https://www.djangoproject.com/download/1.7.b4/tarball/',
            'environment_variables': '',
            'python_versions': 'pypy',
        },
        'pypy-Django==1.7-nocover': {
            'coverage_flags': 'false',
            'depencencies': 'https://www.djangoproject.com/download/1.7.b4/tarball/',
            'environment_variables': '',
            'python_versions': 'pypy',
        },
    }


def test_make_matrix_from_string_1():
    assert (
        from_string(
            """
[matrix]
python_versions =
    2.6
    2.7
    3.3
    3.4
    pypy

dependencies =
    : trollius MySQL-python !python_versions[3.*]
    win: trollius !python_versions[3.*]
    : asyncio &python_versions[3.3]
    : &python_versions[3.4]

coverage_flags =
    : true
    nocover: false

environment_variables =
    debug: ASPECTLIB_DEBUG=yes
    -
"""
        )
        == {
            '2.6': {
                'coverage_flags': 'true',
                'dependencies': 'trollius MySQL-python',
                'environment_variables': '',
                'python_versions': '2.6',
            },
            '2.6-debug': {
                'coverage_flags': 'true',
                'dependencies': 'trollius MySQL-python',
                'environment_variables': 'ASPECTLIB_DEBUG=yes',
                'python_versions': '2.6',
            },
            '2.6-nocover': {
                'coverage_flags': 'false',
                'dependencies': 'trollius MySQL-python',
                'environment_variables': '',
                'python_versions': '2.6',
            },
            '2.6-nocover-debug': {
                'coverage_flags': 'false',
                'dependencies': 'trollius MySQL-python',
                'environment_variables': 'ASPECTLIB_DEBUG=yes',
                'python_versions': '2.6',
            },
            '2.6-win': {'coverage_flags': 'true', 'dependencies': 'trollius', 'environment_variables': '', 'python_versions': '2.6'},
            '2.6-win-debug': {
                'coverage_flags': 'true',
                'dependencies': 'trollius',
                'environment_variables': 'ASPECTLIB_DEBUG=yes',
                'python_versions': '2.6',
            },
            '2.6-win-nocover': {
                'coverage_flags': 'false',
                'dependencies': 'trollius',
                'environment_variables': '',
                'python_versions': '2.6',
            },
            '2.6-win-nocover-debug': {
                'coverage_flags': 'false',
                'dependencies': 'trollius',
                'environment_variables': 'ASPECTLIB_DEBUG=yes',
                'python_versions': '2.6',
            },
            '2.7': {
                'coverage_flags': 'true',
                'dependencies': 'trollius MySQL-python',
                'environment_variables': '',
                'python_versions': '2.7',
            },
            '2.7-debug': {
                'coverage_flags': 'true',
                'dependencies': 'trollius MySQL-python',
                'environment_variables': 'ASPECTLIB_DEBUG=yes',
                'python_versions': '2.7',
            },
            '2.7-nocover': {
                'coverage_flags': 'false',
                'dependencies': 'trollius MySQL-python',
                'environment_variables': '',
                'python_versions': '2.7',
            },
            '2.7-nocover-debug': {
                'coverage_flags': 'false',
                'dependencies': 'trollius MySQL-python',
                'environment_variables': 'ASPECTLIB_DEBUG=yes',
                'python_versions': '2.7',
            },
            '2.7-win': {'coverage_flags': 'true', 'dependencies': 'trollius', 'environment_variables': '', 'python_versions': '2.7'},
            '2.7-win-debug': {
                'coverage_flags': 'true',
                'dependencies': 'trollius',
                'environment_variables': 'ASPECTLIB_DEBUG=yes',
                'python_versions': '2.7',
            },
            '2.7-win-nocover': {
                'coverage_flags': 'false',
                'dependencies': 'trollius',
                'environment_variables': '',
                'python_versions': '2.7',
            },
            '2.7-win-nocover-debug': {
                'coverage_flags': 'false',
                'dependencies': 'trollius',
                'environment_variables': 'ASPECTLIB_DEBUG=yes',
                'python_versions': '2.7',
            },
            '3.3': {'coverage_flags': 'true', 'dependencies': 'asyncio', 'environment_variables': '', 'python_versions': '3.3'},
            '3.3-debug': {
                'coverage_flags': 'true',
                'dependencies': 'asyncio',
                'environment_variables': 'ASPECTLIB_DEBUG=yes',
                'python_versions': '3.3',
            },
            '3.3-nocover': {'coverage_flags': 'false', 'dependencies': 'asyncio', 'environment_variables': '', 'python_versions': '3.3'},
            '3.3-nocover-debug': {
                'coverage_flags': 'false',
                'dependencies': 'asyncio',
                'environment_variables': 'ASPECTLIB_DEBUG=yes',
                'python_versions': '3.3',
            },
            '3.4': {'coverage_flags': 'true', 'dependencies': ' ', 'environment_variables': '', 'python_versions': '3.4'},
            '3.4-debug': {
                'coverage_flags': 'true',
                'dependencies': ' ',
                'environment_variables': 'ASPECTLIB_DEBUG=yes',
                'python_versions': '3.4',
            },
            '3.4-nocover': {'coverage_flags': 'false', 'dependencies': ' ', 'environment_variables': '', 'python_versions': '3.4'},
            '3.4-nocover-debug': {
                'coverage_flags': 'false',
                'dependencies': ' ',
                'environment_variables': 'ASPECTLIB_DEBUG=yes',
                'python_versions': '3.4',
            },
            'pypy': {
                'coverage_flags': 'true',
                'dependencies': 'trollius MySQL-python',
                'environment_variables': '',
                'python_versions': 'pypy',
            },
            'pypy-debug': {
                'coverage_flags': 'true',
                'dependencies': 'trollius MySQL-python',
                'environment_variables': 'ASPECTLIB_DEBUG=yes',
                'python_versions': 'pypy',
            },
            'pypy-nocover': {
                'coverage_flags': 'false',
                'dependencies': 'trollius MySQL-python',
                'environment_variables': '',
                'python_versions': 'pypy',
            },
            'pypy-nocover-debug': {
                'coverage_flags': 'false',
                'dependencies': 'trollius MySQL-python',
                'environment_variables': 'ASPECTLIB_DEBUG=yes',
                'python_versions': 'pypy',
            },
            'pypy-win': {'coverage_flags': 'true', 'dependencies': 'trollius', 'environment_variables': '', 'python_versions': 'pypy'},
            'pypy-win-debug': {
                'coverage_flags': 'true',
                'dependencies': 'trollius',
                'environment_variables': 'ASPECTLIB_DEBUG=yes',
                'python_versions': 'pypy',
            },
            'pypy-win-nocover': {
                'coverage_flags': 'false',
                'dependencies': 'trollius',
                'environment_variables': '',
                'python_versions': 'pypy',
            },
            'pypy-win-nocover-debug': {
                'coverage_flags': 'false',
                'dependencies': 'trollius',
                'environment_variables': 'ASPECTLIB_DEBUG=yes',
                'python_versions': 'pypy',
            },
        }
    )


def test_make_matrix_from_string_2():
    assert (
        from_string(
            """
[matrix]
python_versions =
    # some
    2.6
    # junk
    2.7
    3.3
    3.4
    pypy

dependencies =
coverage_flags =
    : true
    nocover: false

environment_variables =
"""
        )
        == {
            '2.6': {'coverage_flags': 'true', 'dependencies': '', 'environment_variables': '', 'python_versions': '2.6'},
            '2.6-nocover': {'coverage_flags': 'false', 'dependencies': '', 'environment_variables': '', 'python_versions': '2.6'},
            '2.7': {'coverage_flags': 'true', 'dependencies': '', 'environment_variables': '', 'python_versions': '2.7'},
            '2.7-nocover': {'coverage_flags': 'false', 'dependencies': '', 'environment_variables': '', 'python_versions': '2.7'},
            '3.3': {'coverage_flags': 'true', 'dependencies': '', 'environment_variables': '', 'python_versions': '3.3'},
            '3.3-nocover': {'coverage_flags': 'false', 'dependencies': '', 'environment_variables': '', 'python_versions': '3.3'},
            '3.4': {'coverage_flags': 'true', 'dependencies': '', 'environment_variables': '', 'python_versions': '3.4'},
            '3.4-nocover': {'coverage_flags': 'false', 'dependencies': '', 'environment_variables': '', 'python_versions': '3.4'},
            'pypy': {'coverage_flags': 'true', 'dependencies': '', 'environment_variables': '', 'python_versions': 'pypy'},
            'pypy-nocover': {'coverage_flags': 'false', 'dependencies': '', 'environment_variables': '', 'python_versions': 'pypy'},
        }
    )
