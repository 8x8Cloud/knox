#!/usr/bin/env python3
import sys
from knox import awscert
from knox import cli

def test_main():
    aws = awscert.AwsCert()
    print(aws)

if __name__ == "__main__":
    sys.exit(test_main())
