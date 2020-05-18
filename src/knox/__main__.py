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
limitations under the License.


Entrypoint module, in case you use `python -mknox`.


Why does this file exist, and why __main__? For more info, read:

- https://www.python.org/dev/peps/pep-0338/
- https://docs.python.org/2/using/cmdline.html#cmdoption-m
- https://docs.python.org/3/using/cmdline.html#cmdoption-m
"""
import sys

from loguru import logger

from .certificate import Cert  # noqa: F401
from .knox import Knox

logger.add(sys.stdout, format="{time} {level} {message}", level="INFO")


@logger.catch()
def main():
    knox = Knox()

    # load a certificates
    cert1 = Cert("www.example.com")
    cert1.load_x509("sample_cert1.pem")
    # save it to store
    knox.store.save(cert1)

    # load a certificates
    cert2 = Cert("web.example.com")
    cert2.load_x509("sample_cert2.pem")
    # save it to store
    knox.store.save(cert2)

    # load a certificates
    cert3 = Cert("www.cloud.example.com")
    cert3.load_x509("sample_cert3.pem")
    # save it to store
    knox.store.save(cert3)


if __name__ == "__main__":
    main()
