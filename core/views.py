from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import os
import pandas as pd
from django.conf import settings
from datetime import datetime,timedelta
@login_required
def home(request):
    return render(request, "home.html")

@login_required
def dashboard(request):
    filename = f"watchlist_{(datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d')}.csv"
    print(f"Loading watchlist from: {filename}")
    csv_path = os.path.join(settings.BASE_DIR, 'data', filename)

    try:
        df = pd.read_csv(csv_path)
        df['Change'] = pd.to_numeric(df['Change'], errors='coerce')
        watchlist = df.to_dict(orient='records')  # list of dicts
    except Exception as e:
        watchlist = []
        print(f"Error reading watchlist CSV: {e}")
    return render(request, 'dashboard.html', {
        'watchlist': watchlist
    })