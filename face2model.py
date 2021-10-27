#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import shutil
import sys

def run(filename):
    os.system(f"docker run --rm -v {os.getcwd()}/data:/data:Z asjackson/vrn /runner/run.sh /data/{filename}")

def main(filepath):
    tic = time.time()
    filename = os.path.basename(filepath)
    print(filename)
    shutil.copy(filepath, "data/" + filename)
    run(filename)
    toc = time.time()
    print(f"Time taken: {toc - tic:f}s")

if __name__ == "__main__":
    main(*sys.argv[1:])
