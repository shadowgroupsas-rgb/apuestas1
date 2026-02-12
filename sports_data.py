import requests
from datetime import datetime

class SportsData:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def get_matches(self, sport='soccer'):
        """
        Fetches today's matches for the given sport.
        Returns a list of dictionaries:
        [{'home_team': 'Team A', 'away_team': 'Team B', 'time': '15:00', 'league': 'League Name'}]
        """
        if sport == 'soccer':
            return self._get_soccer_matches()
        elif sport == 'basketball':
            return self._get_nba_matches()
        elif sport == 'baseball':
            return self._get_mlb_matches()
        else:
            return []

    def _get_soccer_matches(self):
        # Using ESPN's public API for Soccer (EPL default for demo)
        # You can expand this to other leagues by changing the endpoint
        url = "https://site.api.espn.com/apis/site/v2/sports/soccer/eng.1/scoreboard"
        try:
            response = requests.get(url, headers=self.headers, timeout=5)
            data = response.json()
            matches = []

            for event in data.get('events', []):
                try:
                    competition = event['competitions'][0]
                    home = competition['competitors'][0]['team']['displayName']
                    away = competition['competitors'][1]['team']['displayName']
                    date_str = event['date'] # ISO format

                    # Parse time (simplified)
                    dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%MZ")
                    time_str = dt.strftime("%H:%M UTC")

                    matches.append({
                        'home_team': home,
                        'away_team': away,
                        'time': time_str,
                        'league': 'Premier League'
                    })
                except (KeyError, IndexError):
                    continue
            return matches
        except Exception as e:
            print(f"Error fetching soccer: {e}")
            return []

    def _get_nba_matches(self):
        url = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard"
        try:
            response = requests.get(url, headers=self.headers, timeout=5)
            data = response.json()
            matches = []

            for event in data.get('events', []):
                try:
                    competition = event['competitions'][0]
                    home = competition['competitors'][0]['team']['displayName']
                    away = competition['competitors'][1]['team']['displayName']
                    date_str = event['date']
                    dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%MZ")
                    time_str = dt.strftime("%H:%M UTC")

                    matches.append({
                        'home_team': home,
                        'away_team': away,
                        'time': time_str,
                        'league': 'NBA'
                    })
                except:
                    continue
            return matches
        except Exception as e:
            print(f"Error fetching NBA: {e}")
            return []

    def _get_mlb_matches(self):
        url = "https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard"
        try:
            response = requests.get(url, headers=self.headers, timeout=5)
            data = response.json()
            matches = []

            for event in data.get('events', []):
                try:
                    competition = event['competitions'][0]
                    home = competition['competitors'][0]['team']['displayName']
                    away = competition['competitors'][1]['team']['displayName']
                    date_str = event['date']
                    dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%MZ")
                    time_str = dt.strftime("%H:%M UTC")

                    matches.append({
                        'home_team': home,
                        'away_team': away,
                        'time': time_str,
                        'league': 'MLB'
                    })
                except:
                    continue
            return matches
        except Exception as e:
            print(f"Error fetching MLB: {e}")
            return []

if __name__ == "__main__":
    sd = SportsData()
    print("Soccer:", sd.get_matches('soccer'))
    print("NBA:", sd.get_matches('basketball'))
