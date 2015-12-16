from __future__ import absolute_import

import pytest
import os

import bokeh.command.subcommands.json as scjson
from bokeh.command.bootstrap import main

from . import (
    TmpDir, WorkingDir, with_directory_contents, basic_scatter_script
)

def test_create():
    import argparse
    from bokeh.command.subcommand import Subcommand

    obj = scjson.JSON(parser=argparse.ArgumentParser())
    assert isinstance(obj, Subcommand)

def test_name():
    assert scjson.JSON.name == "json"

def test_help():
    assert scjson.JSON.help == "Create JSON files for one or more applications"

def test_args():
    assert scjson.JSON.args == (

        ('files', dict(
            metavar='DIRECTORY-OR-SCRIPT',
            nargs='+',
            help="The app directories or scripts to generate JSON for",
            default=None
        )),

        ('--indent', dict(
            metavar='LEVEL',
            type=int,
            help="indentation to use when printing",
            default=None
        )),

        (('-o', '--output'), dict(
                metavar='FILENAME',
                action='append',
                type=str,
                help="Name of the output file or - for standard output."
        )),
    )

def test_no_script(capsys):
    with (TmpDir(prefix="bokeh-json-no-script")) as dirname:
        with WorkingDir(dirname):
            with pytest.raises(SystemExit):
                main(["bokeh", "json"])
        out, err = capsys.readouterr()
        assert err == """usage: bokeh json [-h] [--indent LEVEL] [-o FILENAME]
                  DIRECTORY-OR-SCRIPT [DIRECTORY-OR-SCRIPT ...]
bokeh json: error: too few arguments
"""
        assert out == ""

def test_basic_script(capsys):
    def run(dirname):
        with WorkingDir(dirname):
            main(["bokeh", "json", "scatter.py"])
        out, err = capsys.readouterr()
        assert err == ""
        assert out == ""

        assert set(["scatter.json", "scatter.py"]) == set(os.listdir(dirname))

    with_directory_contents({ 'scatter.py' : basic_scatter_script },
                            run)

def test_basic_script_with_output_after(capsys):
    def run(dirname):
        with WorkingDir(dirname):
            main(["bokeh", "json", "scatter.py", "--output", "foo.json"])
        out, err = capsys.readouterr()
        assert err == ""
        assert out == ""

        assert set(["foo.json", "scatter.py"]) == set(os.listdir(dirname))

    with_directory_contents({ 'scatter.py' : basic_scatter_script },
                            run)

def test_basic_script_with_output_before(capsys):
    def run(dirname):
        with WorkingDir(dirname):
            main(["bokeh", "json", "--output", "foo.json", "scatter.py"])
        out, err = capsys.readouterr()
        assert err == ""
        assert out == ""

        assert set(["foo.json", "scatter.py"]) == set(os.listdir(dirname))

    with_directory_contents({ 'scatter.py' : basic_scatter_script },
                            run)
