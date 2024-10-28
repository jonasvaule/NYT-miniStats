# NYT Mini Crossword Leaderboard Stats

See stats for the **NYT Mini Crossword**, and compare with others on your leaderboard.

## Features

- Fetch and compare solving times for specified usernames over multiple dates.
- Track and calculate statistics like:
  - Total solving time (in seconds and minutes)
  - Average solving time per puzzle
  - Rank 1 count and rank 1 percentage
  - Mean and Interquartile Range (IQR) of solving times

## Prerequisites

- **Python 3.x**

### Required Python Packages

```bash
pip install -r requirements.txt
```

## Setup

### Obtain Your NYT-S Cookie

To access the NYT Mini Crossword leaderboard, you’ll need your **NYT-S cookie**:

1. **Log in** to the [NY Times Crossword](https://www.nytimes.com/crosswords) site.
2. Open **Developer Tools** in your browser (usually available by right-clicking on the page and selecting “Inspect”).
3. Go to the **Network** or **Application** tab, find **Cookies**, and locate the **NYT-S** cookie.  
4. Copy the **NYT-S** cookie value, starting AFTER 'NYT-S=' and ending at the first ';'.

### Configure the Script

1. In `main.py`, update the following placeholders with your information:
   - Replace `<YOUR_COOKIE_HERE>` with your actual NYT-S cookie value.
   - Replace `<YOUR_USERNAMES_HERE>` with a list of usernames you want to track (e.g., `["user1", "user2"]`).

### Usage

Run the script to fetch leaderboard data and calculate statistics for the desired date range:

```bash
python src/main.py
```

If several usernames are provided, only results where **all** usernames completed the puzzle will be considered.

If a single username is provided, all results will be considered (within the date range).

### Example Output

The script will generate a CSV file (`leaderboard_stats.csv`) with the following columns for each tracked user:

| Username | Total Time (s) | Total Time (min) | Mean Time (s) | Mean Time (min) | Avg Time (s) | Avg Time (min) | IQR (s) | Participation Count | Rank 1 Count | Rank 1 Percentage |
|----------|----------------|------------------|---------------|-----------------|--------------|----------------|---------|---------------------|---------------|--------------------|
| username1     | 170            | 2.8              | 85.0          | 1.4             | 85.0         | 1.4            | 10.0    | 2                   | 1             | 50.0              |
