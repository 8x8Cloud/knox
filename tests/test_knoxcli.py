import pytest
import knox

from click.testing import CliRunner
from knox.cli import cli
from knox.knox import Knox


def test_vault_initialized(vault_initialized):
    policies = vault_initialized.sys.list_policies()['data']['policies']
    assert 'admin-policy' in policies
    assert 'read-policy' in policies
    assert 'user-policy' in policies


class TestKnoxCLIHelp:

    def test_version(self):
        runner = CliRunner()
        result = runner.invoke(cli, "--version")
        assert "version 0.1.11" in result.stdout

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



