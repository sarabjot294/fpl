import json
import csv

# Constants
LEAGUE_CODE = '411316'
INPUT_FILE = f'fpl_raw_data_league_data_{LEAGUE_CODE}.json'
OUTPUT_FILE = f'fpl_cleaning_data_league_data_{LEAGUE_CODE}.csv'
IMAGE_URL = 'add_team_logo_url_here'  # Replace with the actual URL of the black image

# Load the JSON data
def load_json(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

# Extract the first name from the full name
def get_first_name(full_name):
    return full_name.split()[0]

# Structure the data for CSV
def structure_data(data):
    structured_data = []
    
    for team in data:
        first_name = get_first_name(team['manager_name'])
        team_row = {
            'Player Name': first_name,
            'Team Name': team['team_name'],
            'Image URL': IMAGE_URL
        }
        
        # Initialize cumulative points
        cumulative_points = 0
        
        # Add cumulative GW points
        for i in range(1, 39):
            gw_key = f'Gameweek {i}'
            if i <= len(team['gw_points']):
                cumulative_points += team['gw_points'][i-1]
            team_row[gw_key] = cumulative_points
        
        structured_data.append(team_row)
    
    return structured_data

# Save the data to a CSV file
def save_to_csv(data, filename):
    if data:
        fieldnames = list(data[0].keys())
        
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

# Main function to execute the script
def main():
    json_data = load_json(INPUT_FILE)
    structured_data = structure_data(json_data)
    save_to_csv(structured_data, OUTPUT_FILE)
    print(f"Data saved to {OUTPUT_FILE}")

if __name__ == '__main__':
    main()
