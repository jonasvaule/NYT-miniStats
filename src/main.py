from leaderboard_compare import compare_leaderboard_stats
from utils import generate_date_range

# Replace with your NYT-S cookie, which can be found in the browser dev tools
# after logging in to the NY Times crossword site.
# Insert the value after "NYT-S=" and before the next ";"
# Should end with "=;"
COOKIE = "<YOUR_COOKIE_HERE>"

if __name__ == "__main__":
    dates = generate_date_range("2024-06-01","2024-10-28")

    # Replace with usernames present in your NYT Mini Crossword leaderboard
    usernames = ["<YOUR_USERNAMES_HERE>", "<AND_MAYBE_HERE>"]

    compare_leaderboard_stats(dates, usernames, COOKIE)