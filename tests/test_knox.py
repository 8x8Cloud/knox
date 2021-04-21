import knox
import pytest


def test_vault_initialized(vault_initialized):
    policies = vault_initialized.sys.list_policies()['data']['policies']
    assert 'admin-policy' in policies
    assert 'read-policy' in policies
    assert 'user-policy' in policies
