import time
import pandas as pd
import numpy as np
from datetime import datetime

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
    print('Hello! Let\'s explore some US bikeshare data provided by Motivate!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ''
    while(city not in CITY_DATA.keys()):
        print('First select the city to filter on or press enter to default to Chicago')
        city = input('Enter either Chicago, New York City or Washington [Chicago]: ').lower()
        if city == '':
            city = 'chicago'


    # get user input for month (all, january, february, ... , june)
    month = ''
    MONTH_LIST = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    print('Next, select a starting month to filter on or press enter for all available months')
    while(month not in MONTH_LIST):
        month = input('Enter either January, February, March, April, May or June [all]: ').lower()
        if month == '':
            month = 'all'

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''
    DAY_LIST = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    print('Next, select a day to filter on or press enter for all available days')
    while(day not in DAY_LIST):
        day = input('Enter either Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday [all]: ').lower()
        if day == '':
            day = 'all'

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
    # Load the correct city data
    df = pd.read_csv(CITY_DATA[city])

    # Convert the Start Time and End Time to true dates
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # Create Month, Day and Hour columns for both start time and end time in case it spans either
    df['Start Month'] = df['Start Time'].dt.month
    df['End Month'] = df['End Time'].dt.month
    df['Start Day'] = df['Start Time'].dt.weekday_name
    df['End Day'] = df['End Time'].dt.weekday_name
    df['Start Hour'] = df['Start Time'].dt.hour
    df['End Hour'] = df['End Time'].dt.hour

    # Filter the dataframe either by month or weekday if necessary yeilding all records that started on the selection criteria
    if(month != 'all'):
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['Start Month'] == month]

    if(day != 'all'):
        df = df[df['Start Day'] == day.title()]

   # provide a browsable list of the raw data after filters
    index = 1
    browse = input('Would you like to preview the filtered data? (y/n) [y]: ').lower()
    if(browse == ''):
        browse = 'y'
        
    while(browse == 'y'):
        print(df[index:index+5])
        index = index + 5
        browse = input('Would you like to continue? (y/n) [y]: ').lower()
        if(browse == ''):
            browse = 'y'

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month if there is more than one (ie. not filtered)
    if(len(df['Start Month'].unique()) > 1):
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        start_month = df['Start Month'].mode()[0] - 1
        end_month = df['End Month'].mode()[0] - 1
        if(start_month != end_month):
            print('There are two common months due to some starting times and ending times spanning a day')
            print('They were {0} and {1}'.format(months[start_month].title(), months[end_month].title()))
        else:
            print('The most common month is', months[start_month].title())

    # display the most common day of week if there is more than one (ie. not filtered)
    if(len(df['Start Day'].unique()) > 1):
        start_day = df['Start Day'].mode()[0]
        end_day = df['End Day'].mode()[0]
        if(start_day != end_day):
            print('There are two common days due to some starting times and ending times spanning a day')
            print('They were {0} and {1}'.format(start_day, end_day))
        else:
            print('The most common day is', start_day)

    # display the most common start hour
    start_hour = datetime(1972, 1, 1, df['Start Hour'].mode()[0], 0, 0, 0)
    end_hour = datetime(1972, 1, 1, df['End Hour'].mode()[0], 0, 0, 0)
    df_common_hour = df[(df['Start Hour'] == df['Start Hour'].mode()[0]) | (df['End Hour'] == df['End Hour'].mode()[0])]
    mean_duration = df_common_hour['Trip Duration'].mean()
    if(start_hour != end_hour):
        print('There are two common hours due to some starting times and ending times spanning an hour')
        print('They were {0} and {1}'.format(start_hour.strftime("%-I%p"), end_hour.strftime("%-I%p")))
    else:
        print('The most common hour is', start_hour.strftime("%-I%p"))
        
    print('With a mean duration of {:.{prec}f} minutes and {:.{prec}f} seconds'.format(mean_duration / 60, mean_duration % 60, prec=0))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most common starting station is', df['Start Station'].mode()[0])

    # display most commonly used end station
    print('The most common ending station is', df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    df['Combination'] = df['Start Station'] + ' to ' + df['End Station']
    print('The most common combination is', df['Combination'].mode()[0])

    # calculate the mean duration of trips for the most common combination
    df_combination = df[df['Combination'] == df['Combination'].mode()[0]]
    combo_mean = df_combination['Trip Duration'].mean()
    print('With a mean duration of {:.{prec}f} minutes and {:.{prec}f} seconds'.format(combo_mean / 60, combo_mean % 60, prec=0))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total rental time was {:.{prec}f} hours and {:.{prec}f} minutes'.format(df['Trip Duration'].sum() / 3600, (df['Trip Duration'].sum() % 3600) / 60, prec=0))

    # display mean travel time
    print('The mean trip duration was {:.{prec}f} minutes and {:.{prec}f} seconds'.format(df['Trip Duration'].mean() / 60, df['Trip Duration'].mean() % 60, prec=0))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('The total users by type are')
    print(df['User Type'].value_counts())


    # Display counts of gender
    print('The total users by gender are')
    print(df['Gender'].value_counts())

    # Display earliest, most recent, and most common year of birth
    print('The earliest, most recent and most common birth years were {:.{prec}f}, {:.{prec}f} and {:.{prec}f}.'.format(df['Birth Year'].min(), df['Birth Year'].max(), df['Birth Year'].mode()[0], prec=0))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
