#!/usr/bin/env python3
"""Build the dependency-free static KunaalNaik.com site."""
from pathlib import Path
from datetime import datetime, timezone
import html
import json
import subprocess

from pages_structural import STRUCTURAL
import scorecard_page

ROOT = Path(__file__).parent
SITE = "https://kunaalnaik.com"
EMAIL = "me@kunaalnaik.com"
