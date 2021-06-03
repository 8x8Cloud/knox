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
from click.testing import CliRunner
from knox.cli import cli


class TestKnoxIntegration:
    """Integration tests"""

    def test_cert_save(self, vault_initialized, ktfdata):
        ktfdata.gen_cert()
#        print(f"pub: \n{ktfdata.cert_pub()}")
#        print(f"priv: \n{ktfdata.cert_key()}")

        pub = "tests/data/client-pub.pem"
        key = "tests/data/client-key.pem"
        name = "test"

        runner = CliRunner()
        result = runner.invoke(cli, f"cert --pub {pub} --key {key} save {name}")
        assert result.exit_code == 0
