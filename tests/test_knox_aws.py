#!/usr/bin/env python3
import sys
from . knox import AwsCert

def test_main():
    aws = knox.AwsCert()
    print(aws)


if __name__ == "__main__":
    sys.exit(test_main())
