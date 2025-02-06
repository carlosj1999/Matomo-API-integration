import requests, json
from datetime import datetime, timedelta
# Matomo server details
MATOMO_URL = "...."
TOKEN_AUTH = "...."


class APIClient:
    def __init__(self, base_url, auth_token):
        self.base_url = base_url
        self.auth_token = auth_token

    def get_users(self, site_id="2", period="day", date=None, minutes_ago=6000, count_visitors=10000):
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        sixty_min_ago = datetime.now() - timedelta(minutes=minutes_ago)
        params = {
            "module": "API",
            "method": "Live.getLastVisitsDetails",
            "idSite": site_id,
            "period": period,
            "date": date,
            "minTimestamp": int(sixty_min_ago.timestamp()),
            "countVisitorsToFetch": count_visitors,
            "format": "json",
            "token_auth": self.auth_token,
        }

        response = requests.post(self.base_url, params=params)
        if response.status_code == 200:
            return response
        else:
            print("Error:", response.status_code, response.text)
            return False

# Example usage
if __name__ == "__main__":
    # Initialize URL and AuthToken
    api_url = MATOMO_URL
    token = TOKEN_AUTH

    # Create API client
    client = APIClient(api_url, token)

    # Get users data
    response = client.get_users()
    if response:
        visits = response.json()
        print(f"Amount of visits: {len(visits)}")

        users = [visit for visit in visits if visit.get("userId")]
        users_seen = set()
        users_unique = [d for d in users if not (d["userId"] in users_seen or users_seen.add(d["userId"]))]
        print(f"Amount of visits from users who Logged In: {len(users_unique)}")

        users_payed = []
        for u in users:
            if u.get("actionDetails"):
                for action in u["actionDetails"]:
                    if action.get("goalName"):
                        if "Payment Submitted" in action["goalName"]:
                            users_payed.append(u["userId"])
        users_payed_seen = set()
        users_payed_unique = [d for d in users_payed if not (d in users_payed_seen or users_payed_seen.add(d))]

        users_ret = [u["userId"] for u in users if u["userId"] not in users_payed]
        users_ret_seen = set()
        users_ret_unique = [d for d in users_ret if not (d in users_ret_seen or users_ret_seen.add(d))]
        
        print(f"Amount of users who made a payment: {len(users_payed_unique)}")
        print(f"Amount of users who didn't make a payment: {len(users_ret_unique)}")
        print(f"Users ID's who logged in the last 60 minutes and made a payment: {','.join(users_payed_unique)}")
        print(f"Users ID's who logged in the last 60 minutes and didn't make a payment: {','.join(users_ret_unique)}")
    else:
        pass
