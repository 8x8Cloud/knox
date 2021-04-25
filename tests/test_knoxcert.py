import pytest


def test_knoxcert(vault_initialized, ktfdata):
    ktfdata.gen_cert()
    print(f"pub: \n{ktfdata.cert_pub()}")
    print(f"priv: \n{ktfdata.cert_key()}")

    pass
