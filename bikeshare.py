import time
import datetime as dt
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

MONTH_STR2NUM = {'january': 1, 'february': 2,
                 'march': 3, 'april': 4, 'may': 5, 'june': 6}
MONTH_NUM2STR = {1: 'january', 2: 'february',
                 3: 'march', 4: 'april', 5: 'may', 6: 'june'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Please enter city name: ").lower()
        if city in CITY_DATA:
            break
        else:
            print("Invalid name")

    # get user input for month (all, january, february, ... , june)
    valid_months = {'all', 'january', 'february',
                    'march', 'april', 'may', 'june'}
    while True:
        month = input("Please enter month: ").lower()
        if month in valid_months:
            break
        else:
            print("Invalid month")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    valid_days = {'all', 'monday', 'tuesday', 'wednesday',
                  'thursday', 'friday', 'saturday', 'sunday'}
    while True:
        day = input("Please enter day: ").lower()
        if day in valid_days:
            break
        else:
            print("Invalid day")

    print('-'*40)
    return city, month, day


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
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['weekday'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        month_num = MONTH_STR2NUM[month]
        df = df[df['month'] == month_num]

    if day != 'all':
        df = df[df['weekday'] == day.title()]

    print(df.head())

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].value_counts().index[0]
    print("The most common month is: " + MONTH_NUM2STR[most_common_month])

    # display the most common day of week
    most_common_weekday = df['weekday'].value_counts().index[0]
    print("The most common day of week is: " + most_common_weekday)

    # display the most common hour of day
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour

    most_common_start_hour = df['hour'].value_counts().index[0]
    print("The most common hour of day is: ", most_common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].value_counts().index[0]
    print("The most commonly used start station is: " + start_station)

    # display most commonly used end station
    end_station = df['End Station'].value_counts().index[0]
    print("The most commonly used end station is: " + end_station)

    # display most frequent combination of start station and end station trip
    trip_df = df['Start Station'] + ' to ' + df['End Station']
    trip = trip_df.value_counts().index[0]
    print("The most frequent combination of start station and end station trip is: " + trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    tot_travel_time = df['Trip Duration'].sum()
    print("The total travel time is: ", tot_travel_time)

    # display average travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("The average travel time is: ", mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of each user types
    user_type_counts = df['User Type'].value_counts()
    print("The counts of each user types is:")
    print(user_type_counts)

    # Display counts of gender (only avaliable for NYC and Chicago)
    if 'Gender' in df:
        gender_counts = df['Gender'].value_counts()
        print("The counts of each gender is:")
        print(gender_counts)
    else:
        print("no gender information")
        print('-'*40)

    # Display earliest, most recent, and most common year of birth (only avalaible for NYC and Chicago)
    if 'Birth Year' in df:
        earliest_birth_year = df["Birth Year"].min()
        print("The earliest year of birth is: ", earliest_birth_year)

        recent_birth_year = df["Birth Year"].max()
        print("The most recent year of birth is: ", recent_birth_year)

        common_birth_year = df["Birth Year"].value_counts().index[0]
        print("The most common year of birth is: ", common_birth_year)
        print("\nThis took %s seconds." % (time.time() - start_time))

    else:
        print("no birth year information")
        print('-'*40)


def display_raw_data(df):
    """Displays five lines of raw data if the user choose'yes'. Continue prompting and printing the next five rows at a time until the user choose 'no'"""

    display = input(
        '\nWould you like to view individual trip data? Type \'yes\' or \'no\': ')
    display = display.lower()

    start_row = 0
    end_row = start_row + 5
    if display == 'yes':
        if end_row < len(df.index):
            print(df.iloc[start_row:end_row])
        else:
            print(df.iloc[:])
    else:
        print('-'*40)
        return

    while start_row < len(df.index):
        display = input(
            '\nWould you like to view another five individual trip data? Type \'yes\' or \'no\': ')
        display = display.lower()
        if display == 'yes':
            start_row += 5
            end_row += 5
            if end_row < len(df.index):
                print(df.iloc[start_row:end_row])
            else:
                print(df.iloc[start_row:])
                print("end of file")
                break
        else:
            break

    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)

        station_stats(df)

        trip_duration_stats(df)

        user_stats(df)

        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
