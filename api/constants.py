import json
from typing import List, Dict, Set
from os import environ
from collections import defaultdict


FIREBASE_API_KEY = environ.get("FIREBASE_API_KEY")
PROJECT_ID = environ.get("PROJECT_ID")
