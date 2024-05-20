import requests
import json

"""
This file is used to save data for the league code: 411316
"""

# Define constants
LEAGUE_CODE = '411316'  # Replace with your actual league code
OUTPUT_FILE = f'fpl_raw_data_league_data_{LEAGUE_CODE}.json'

# Function to get general FPL data
def get_general_data():
    url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    response = requests.get(url)
    return response.json()

# Function to get league data
def get_league_data(league_code):
    url = f'https://fantasy.premierleague.com/api/leagues-classic/{league_code}/standings/'
    response = requests.get(url)
    return response.json()

# Function to get team data
def get_team_data(team_id):
    url = f'https://fantasy.premierleague.com/api/entry/{team_id}/history/'
    response = requests.get(url)
    return response.json()

# Function to collect data for each team in the league
def collect_fpl_data(league_code):
    league_data = get_league_data(league_code)
    teams = league_data['standings']['results']
    
    all_teams_data = []
    
    for team in teams:
        team_id = team['entry']
        team_name = team['entry_name']
        manager_name = team['player_name']
        
        team_data = get_team_data(team_id)
        
        gw_points = [gw['points'] for gw in team_data['current']]
        total_points = sum(gw_points)
        
        team_info = {
            'team_id': team_id,
            'team_name': team_name,
            'manager_name': manager_name,
            'gw_points': gw_points,
            'total_points': total_points
        }
        
        all_teams_data.append(team_info)
    
    return all_teams_data

# Save data to a file
def save_data_to_file(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# Main function to run the script
def main():
    fpl_data = collect_fpl_data(LEAGUE_CODE)
    save_data_to_file(fpl_data, OUTPUT_FILE)
    print(f"Data saved to {OUTPUT_FILE}")

if __name__ == '__main__':
    main()
