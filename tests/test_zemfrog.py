#!/usr/bin/env python

"""Tests for `zemfrog` package."""


import unittest

from click.testing import CliRunner

from zemfrog import cli


class TestZemfrog(unittest.TestCase):
    """Tests for `zemfrog` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
