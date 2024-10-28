import requests
import csv
import statistics

def fetch_leaderboard_for_date(date, cookie):
    """
    Fetches the leaderboard data for a specific date from the NYT Mini Crossword API.

    Parameters:
    - date (str): The date for which to retrieve leaderboard data, in "YYYY-MM-DD" format.
    - cookie (str): The NYT authentication cookie for API access.

    Returns:
    - dict: A dictionary containing the leaderboard data for the specified date if the request is successful.
            Structure typically includes `printDate`, `publishType`, and `data` (a list of user stats).
            Each user entry in `data` may contain `userID`, `name`, `rank`, and `score` (with `secondsSpentSolving`).
    - None: If the request fails, it returns None and prints an error message.

    Raises:
    - requests.RequestException: An error occurred while fetching the data.
    """    
    LEADERBOARD_URL = f"https://www.nytimes.com/svc/crosswords/v6/leaderboard/mini/{date}.json"
    try:
        headers = {
            'Cookie': f'NYT-S={cookie};'
        }
        response = requests.get(LEADERBOARD_URL, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def compare_leaderboard_stats(dates, usernames, cookie, output_file="leaderboard_stats.csv"):
    """
    Compare and aggregate leaderboard stats for a list of usernames over a range of dates.

    
    Parameters:
    - dates (List[str]): List of dates in "YYYY-MM-DD" format.
    - usernames (List[str]): List of usernames to include in the comparison. 
    Users must be present in your NYT Mini Crossword leaderboard.
    If only one user is provided, find their full stats between the dates.
    - cookie (str): Cookie for API authentication.
    - output_file (str): File path to save the aggregated results.
    """
    user_stats = {username: {"times": [], "rank_1_count": 0} for username in usernames}
    
    for index, date in enumerate(dates):
        print(f"Processing date {index + 1}/{len(dates)}: {date}")
        leaderboard = fetch_leaderboard_for_date(date, cookie)
        
        if not leaderboard or 'data' not in leaderboard:
            continue  # Skip if no leaderboard data for the date

        filtered_data = [
            entry for entry in leaderboard['data']
            if entry.get('name') in usernames and 'score' in entry and 'secondsSpentSolving' in entry['score']
        ]

        ## ignore if filtered data is not as long as usernames,
        ## ie if not all users completed the puzzle that day
        if len(filtered_data) != len(usernames):
            continue

        filtered_data.sort(key=lambda x: x['score']['secondsSpentSolving'])

        if filtered_data:
            top_user = filtered_data[0]['name']
            if top_user in user_stats:
                user_stats[top_user]["rank_1_count"] += 1
                

        for entry in filtered_data:
            username = entry['name']
            if username in user_stats:
                user_stats[username]["times"].append(entry['score']['secondsSpentSolving'])
        
    
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Username", "Total Time (s)", "Total Time (min)", "Median Time (s)", 
                         "Median Time (min)", "Avg Time (s)", "Avg Time (min)", "IQR (s)", 
                         "Participation Count", "Rank 1 Count", "Rank 1 Percentage"])
        
        for username, stats in user_stats.items():
            partition_count = len(stats["times"])
            total_time = sum(stats["times"])
            total_time_minutes = total_time / 60
            median = statistics.median(stats["times"]) if stats["times"] else 0
            median_time_minutes = median / 60
            avg_time = total_time / partition_count if partition_count > 0 else 0
            avg_time_minutes = avg_time / 60
            rank_1_percentage = (stats["rank_1_count"] / partition_count * 100) if partition_count > 0 else 0
            
            # Calculate Interquartile Range (IQR) for solving times in seconds
            iqr = statistics.quantiles(stats["times"], n=4)[2] - statistics.quantiles(stats["times"], n=4)[0] if len(stats["times"]) > 1 else 0
            
            writer.writerow([
                username, 
                total_time, 
                round(total_time_minutes, 1),
                round(median, 1),
                round(median_time_minutes, 1),
                round(avg_time, 1),
                round(avg_time_minutes, 1),
                round(iqr, 1),
                partition_count,
                stats["rank_1_count"],
                round(rank_1_percentage, 2)
            ])

    print(f"Aggregated stats saved to {output_file}")
