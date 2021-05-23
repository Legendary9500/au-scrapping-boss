# ################     import module     #################

# selenium lib
from selenium import webdriver
# from seleniumwire import webdriver                                                              # for receive response
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

# re lib
import re
# time lib
from time import sleep
# requests lib
import requests
import os
import csv
from lxml import html