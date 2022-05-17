import requests
import os
import json
import pandas as pd
import csv
import numpy as np
from datetime import datetime
import time

os.environ['TOKEN'] = 'AAAAAAAAAAAAAAAAAAAAAKHzbwEAAAAANrBlqwYokl3ttFARZ4ZmiSD7Bw0%3DRa8THgCyIJMa416ckXp3dLfyC4JgfsugJPgLkRT802r0hynEoy'
auth = os.getenv('TOKEN')
headers = {"Authorization": f"Bearer {auth}"}