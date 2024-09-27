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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    while True:
        city = input("Pick a city to report bikeshare statistics on: Chicago, New York City, or Washington: ").lower()
        if city not in ['chicago', 'new york city', 'washington']:
            print("Invalid input.  Valid inputs are:  Chicago, New York City, Washington.")
            continue
        else:
            break

    # get user input for month (all, january, february, ... , june)

    while True:
        month = input("Pick one from the following for the month: January, February, March, April, May, June, or All: ").lower()
        if month not in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
            print('Invalid input.  Valid inputs are:  January, February, March, April, May, June', 'All')
            continue
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)

    while True:
        day = input("Pick one from the following for the day: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or All: ").lower()
        if day not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
            print("Invalid input.  Valid inputs are:  All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday")
            continue
        else:
            break

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

# load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    
# convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
# extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    
# extract month from the Start Time column to create a month column
    df['month'] = df['Start Time'].dt.month
    
# extract weekday from the Start Time column to create a weekday column
    df['weekday'] = df['Start Time'].dt.day_name()

    
# filter by month
    if month.lower() != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
    
# filter by day of week
    if day != 'all':
        df = df[df['weekday'] == day.title()]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print("The most common month for a ride: ", common_month)

    # display the most common day
    print("The most common day for a ride:", df['weekday'].mode()[0])
    
    # display the most common start hour
    print("The most common start hour for a ride:", df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("The most commonly used start station is:", df['Start Station'].mode()[0])

    # display most commonly used end station
    print("The most commonly used end station is:", df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    df['round_trip'] = df['Start Station'] + " to " + df['End Station']
    print("The most common trip is:", df['round_trip'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("The total travel time was:", float(sum((df['Trip Duration']))))

    # display mean travel time

    print("The mean travel time was:", float(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Count by user type:\n", df.groupby(['User Type'])['User Type'].count())

    # Display counts of gender
    try:
        print("Usage by gender:\n", df.groupby(['Gender'])['Gender'].count())

    # Display earliest, most recent, and most common year of birth

#        print("Subscriber birth year statistics:\n")
        
        print("The oldest subscriber was born in:\n", int(df['Birth Year'].min()))
        
        print("The youngest subscriber was born in:\n", int(df['Birth Year'].max()))
        
        print("The most common birth year was:\n", int(df['Birth Year'].mode()[0]))
    except KeyError:
        
        print("Gender and birth year statistics are not available for Washington")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data_display(df):
    """Asks if the user wants to see raw data in increments of 5 rows"""

    confirm = input('\nWould you like to see a few rows of the source data? Enter Yes or No.\n')
    row_offset = 1
    row_increment = 5

    while True:
        if confirm.lower() not in ['yes']:
            break
        else:
            print(df[row_offset:row_offset + row_increment])
            row_offset += row_increment
            confirm = input('\nWould you like to see more data? Enter Yes or No.\n')

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data_display(df)

        restart = input('\nWould you like to restart? Enter yes or No.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
