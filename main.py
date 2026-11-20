#!/usr/bin/env python3
"""Copy the already-rendered entry image to make.fun output."""
import os
import shutil
from pathlib import Path

source = Path(__file__).resolve().parent / 'entry.png'
output = Path(os.environ.get('MAKEFUN_OUTPUT_DIR', '/output'))
output.mkdir(parents=True, exist_ok=True)
shutil.copyfile(source, output / 'entry.png')
