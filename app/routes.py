from flask import Blueprint

main = Blueprint('main', __name__)

@main.route('/scrape')
def scrape():
    return "Data will be sent from here!"