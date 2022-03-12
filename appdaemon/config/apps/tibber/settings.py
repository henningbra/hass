from datetime import datetime
import os
import pytz
from datetime import datetime

# TIBBER
TIBBER_URL = "https://api.tibber.com/v1-beta/gql"
TIBBER_TOKEN = os.getenv('TIBBER_TOKEN', default='your_secret_tibber_token_here')
TIBBER_HEADERS = {
    'Authorization': f'Bearer {TIBBER_TOKEN}',
    'Content-Type': 'application/json'
}
TZ = pytz.timezone(os.getenv('APP_DAEMON_TZ', default='CET'))  # Tibber delivers prices in UTC
