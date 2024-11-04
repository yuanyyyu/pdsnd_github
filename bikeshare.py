import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # List of valid cities, months, and days
    cities = ['chicago', 'new york city', 'washington']
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    
    # Get user input for city (chicago, new york city, washington)
    while True:
        city = input('Please enter a city (Chicago, New York City, Washington): ').lower()
        if city in cities:
            break
        else:
            print("Invalid city. Please try again.")
    
    # Get user input for month (all, january, february, ..., june)
    while True:
        month = input('Please enter a month (January, February, ..., June) or "all" to apply no filter: ').lower()
        if month in months:
            break
        else:
            print("Invalid month. Please try again.")
    
    # Get user input for day of week (all, monday, tuesday, ..., sunday)
    while True:
        day = input('Please enter a day of the week (Monday, Tuesday, ..., Sunday) or "all" to apply no filter: ').lower()
        if day in days:
            break
        else:
            print("Invalid day. Please try again.")
    
    print('-'*40)
    return city, month, day

# Call the function to test it
city, month, day = get_filters()
print(f"City: {city}, Month: {month}, Day: {day}")


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    print(f"Loading data for city: {city}")
    
    # Load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    print(f"Data loaded. Number of rows: {len(df)}")
    
    # Convert the 'Start Time' column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from 'Start Time' to create new columns
    df['month'] = df['Start Time'].dt.month_name().str.lower()
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()

    # Debugging: Print unique months and days available
    print("Available months in data:", df['month'].unique())
    print("Available days of week in data:", df['day_of_week'].unique())

    # Filter by month if applicable
    if month != 'all':
        df = df[df['month'] == month]
        print(f"Data filtered by month ({month}). Number of rows: {len(df)}")

    # Filter by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day]
        print(f"Data filtered by day of week ({day}). Number of rows: {len(df)}")

    # Final Debugging: Show the first few rows of the filtered data
    print("First few rows of the filtered data:")
    print(df.head())

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Check if DataFrame is empty
    if df.empty:
        print("The DataFrame is empty! No data to calculate.")
        return
    
    # Convert 'Start Time' to datetime if not already converted
    if df['Start Time'].dtype != '<M8[ns]':  # Check if it's not already datetime
        df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # Extract month, day of week, and hour from 'Start Time' to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # Display the most common month
    most_common_month = df['month'].mode()[0]
    print(f"Most Common Month: {most_common_month}")

    # Display the most common day of the week
    most_common_day_of_week = df['day_of_week'].mode()[0]
    print(f"Most Common Day of the Week: {most_common_day_of_week}")

    # Display the most common start hour
    most_common_start_hour = df['hour'].mode()[0]
    print(f"Most Common Start Hour: {most_common_start_hour}")

    print(f"\nThis took {time.time() - start_time} seconds.")
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Check if DataFrame is empty
    if df.empty:
        print("The DataFrame is empty! No data to calculate.")
        return

    # Display the most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print(f"Most Common Start Station: {most_common_start_station}")

    # Display the most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print(f"Most Common End Station: {most_common_end_station}")

    # Display the most frequent combination of start station and end station trip
    df['Start-End Combination'] = df['Start Station'] + " to " + df['End Station']
    most_common_trip = df['Start-End Combination'].mode()[0]
    print(f"Most Common Trip: {most_common_trip}")

    print(f"\nThis took {time.time() - start_time} seconds.")
    print('-' * 40)
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Check if DataFrame is empty
    if df.empty:
        print("The DataFrame is empty! No data to calculate.")
        return

    # Display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f"Total Travel Time: {total_travel_time} seconds")

    # Display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print(f"Average Travel Time: {mean_travel_time} seconds")

    print(f"\nThis took {time.time() - start_time} seconds.")
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Check if DataFrame is empty
    if df.empty:
        print("The DataFrame is empty! No data to calculate.")
        return

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("User Types:")
    print(user_types)

    # Check if 'Gender' column exists, and if so, display counts of gender
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print("\nGender Counts:")
        print(gender_counts)
    else:
        print("\nNo gender data available.")

    # Check if 'Birth Year' column exists, and if so, display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_birth_year = int(df['Birth Year'].min())
        most_recent_birth_year = int(df['Birth Year'].max())
        most_common_birth_year = int(df['Birth Year'].mode()[0])

        print("\nBirth Year Stats:")
        print(f"Earliest Birth Year: {earliest_birth_year}")
        print(f"Most Recent Birth Year: {most_recent_birth_year}")
        print(f"Most Common Birth Year: {most_common_birth_year}")
    else:
        print("\nNo birth year data available.")

    print(f"\nThis took {time.time() - start_time} seconds.")
    print('-' * 40)


def display_raw_data(df):
    """
    Displays 5 rows of raw data at a time upon user request.
    
    Args:
        df - Pandas DataFrame containing city data.
    """
    row_start = 0  # Starting index
    row_end = 5    # Ending index

    # Ask the user if they want to see the first 5 rows of raw data
    show_data = input("Would you like to see 5 rows of raw data? Enter yes or no: ").lower()

    # Loop while the user says 'yes' and there is more data to display
    while show_data == 'yes':
        # Display the next 5 rows
        print(df.iloc[row_start:row_end])

        # Update the row indices to show the next set of data
        row_start += 5
        row_end += 5

        # Check if we have reached or exceeded the length of the DataFrame
        if row_start >= len(df):
            print("You've reached the end of the data.")
            break

        # Ask the user again if they want to see more data
        show_data = input("Would you like to see 5 more rows of raw data? Enter yes or no: ").lower()

    print("Exiting raw data display.")


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # Ask if the user wants to see raw data and display it if requested
        display_raw_data(df)

        # Ask if the user wants to restart
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
