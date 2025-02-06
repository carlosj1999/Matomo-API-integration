# API parameters
sixty_min = datetime.now() - timedelta(minutes=70)
params = {
    "module": "API",
    "method": "Live.getLastVisitsDetails",
    "idSite": "2",
    "period": "day",
    "date": "2025-02-06",
    "minTimestamp": int(sixty_min.timestamp()),
    "countVisitorsToFetch": 10000,
    "format": "json",
    "token_auth": TOKEN_AUTH,
}

# Fetch data from Matomo API
response = requests.post(MATOMO_URL, params=params)

# Check response
if response.status_code == 200:
    # Print extracted user IDs
    visits = response.json()
    user_ids = [visit["userId"] for visit in visits if visit.get("userId")]
    print(f"Amount of visits: {len(visits)}")
    print(f"Amount of users: {len(user_ids)}")
    print(f"Users ID's who logged in the last 60 minutes: {','.join(user_ids)}")
else:
    print("Error:", response.status_code, response.text)
