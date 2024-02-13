import requests
import re
import json
from flask import Blueprint, jsonify, request

scraper = Blueprint('scraper',__name__)

