# -*- encoding: utf-8 -*-
"""
@File : wsgi.py
@Time : 2022/5/14 21:11
@Author : Linleil
"""
import os
from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

import app