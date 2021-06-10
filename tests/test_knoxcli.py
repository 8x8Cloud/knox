"""
Apache Software License 2.0

Copyright (c) 2020, 8x8, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License."""

import pytest
import knox

from click.testing import CliRunner
from knox.cli import cli


def test_vault_initialized(vault_initialized):
    policies = vault_initialized.sys.list_policies()['data']['policies']
    assert 'admin-policy' in policies
    assert 'read-policy' in policies
    assert 'user-policy' in policies


class TestKnoxCLIHelp:

    def test_version(self):
        runner = CliRunner()
        result = runner.invoke(cli, "--version")
        assert "version 0.1.14" in result.stdout

    def test_cert(self):
        runner = CliRunner()
        result = runner.invoke(cli, "cert")
        assert "Certificate utilities" in result.stdout

    def test_cert_aws(self):
        runner = CliRunner()
        result = runner.invoke(cli, "cert aws")
        assert "AWS" in result.stdout

    def test_cert_gen(self):
        runner = CliRunner()
        result = runner.invoke(cli, "cert gen")
        assert "Create and store a new certificate" in result.stdout

    def test_cert_get(self):
        runner = CliRunner()
        result = runner.invoke(cli, "cert get")
        assert "Retrieve an existing certificate" in result.stdout

    def test_cert_save(self):
        runner = CliRunner()
        result = runner.invoke(cli, "cert save")
        assert "Store an existing certificate" in result.stdout

    def test_store(self):
        runner = CliRunner()
        result = runner.invoke(cli, "store")
        assert "Store commands" in result.stdout

    def test_store_find(self):
        runner = CliRunner()
        result = runner.invoke(cli, "store find")
        assert "Given a certificate NAME pattern search the store" in result.stdout



