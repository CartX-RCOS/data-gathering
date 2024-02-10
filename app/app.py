from . import app
from flask import render_template, redirect, url_for, Blueprint

app = Blueprint('app', __name__)

@app.route('/dashboard')
def dashboard():
    scraping_status = "Not started"  # Set initial status
    return render_template('./dashboard.html', scraping_status=scraping_status)

@app.route('/scrape', methods=['POST'])
def scrape():
    # Logic for web scraping
    # Update scraping status accordingly
    scraping_status = "Running"
    # Redirect to dashboard with updated status
    return redirect(url_for('dashboard', scraping_status=scraping_status))