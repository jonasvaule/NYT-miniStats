from datetime import datetime, timedelta

def generate_date_range(start_date, end_date):
    """
    Generate a list of dates between start_date and end_date in "YYYY-MM-DD" format.

    Parameters:
    - start_date (str): The start date in "YYYY-MM-DD" format.
    - end_date (str): The end date in "YYYY-MM-DD" format.

    Returns:
    - List[str]: A list of dates as strings in "YYYY-MM-DD" format.
    """
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    
    date_list = [(start + timedelta(days=i)).strftime("%Y-%m-%d") 
                 for i in range((end - start).days + 1)]
    
    return date_list

def today():
    return datetime.now().strftime("%Y-%m-%d")