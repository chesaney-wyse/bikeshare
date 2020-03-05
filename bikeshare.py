import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
        

print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

def get_filters():
    """
    Gets user input for the desired city and to filter by month and day if applicable.
    """
    
    while True:
        city_filter = input('\nWould you like to see data for Chicago, New York City, or Washington?\n').lower()
        message = 'It looks like you want to explore the data for {}, if this is inaccurate, please restart the program now.'
        if city_filter in ('chicago', 'new york city', 'washington'):
            print (message.format(city_filter))
            break
        else:
            print('Please enter a valid city.')
    global city
    city = CITY_DATA[city_filter.lower()] 
    
    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month_filter = input('\nWhich month: January, February, March, April, May or June? Please enter "all" to see all months.\n').lower()
        if month_filter in ('january', 'february', 'march', 'april', 'may', 'june', 'all'):
            print('Filtering data by ', month_filter, '...')
            break
        
        else:
            print('Please enter a valid month.')
    global month    
    month = month_filter.lower()        

        # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)

    while True:
        day_filter = input('\nWhich day of the week? Please enter as an integer (e.g. 1 = Sunday) or enter "all".\n')
        if day_filter in ['1', '2', '3', '4', '5', '6', '7']:
            day_filter = int(day_filter)
            print('Filtering data by', day_filter)
            break
        elif day_filter == 'all':
            print('Filtering data by', day_filter)
            break
        else:
            print('Please enter a valid day')
    global day
    day = day_filter

    while True:
        df = pd.read_csv(city)
        df_preview = input('\nWould you like to view five lines of raw data? Please enter \'yes\' or \'no\'.\n').lower()
        if df_preview == 'yes':
            print(df.head())
            break
        elif df_preview == 'no':
            break 
        else:
            print('Please enter \'yes\' or \'no\'.')

    return city, month, day
print('-'*40)
    

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
    
    df = pd.read_csv(city)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]
    elif month == 'all':
        df = df
    # filter by day of week if applicable
    if day != 'all':
        days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        day = days[day - 1]
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]
    elif day == 'all':
        df = df
    return df

    
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df = load_data(city, month, day)
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # TO DO: display the most common month
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month

    popular_month = df['month'].mode()[0]

    print('Most Popular Month: ', popular_month)

    # TO DO: display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    popular_weekday = df['day_of_week'].mode()[0]

    print('Most Popular Day of Week: ', popular_weekday)

    # TO DO: display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # find the most popular hour
    popular_hour = df['hour'].mode()[0]

    print('Most Popular Start Hour:', popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    df = load_data(city, month, day)
    # TO DO: display most commonly used start station
    popular_start = df['Start Station'].mode()[0]

    print('Most Common Start Station: ', popular_start)

    # TO DO: display most commonly used end station
    popular_end = df['End Station'].mode()[0]

    print('Most Common End Station: ', popular_end)

    # TO DO: display most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station'] + ' ---> ' + df['End Station']

    popular_trip = df['Trip'].mode()[0]

    print('Most Common Trip: ', popular_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    df = load_data(city, month, day) 
    # TO DO: display total travel time
    total_trip_time = df['Trip Duration'].sum()
    
    print('Total Trip Time: ', total_trip_time)

    # TO DO: display mean travel time
    avg_trip_duration = df['Trip Duration'].mean()

    print('Average Trip Duration: ', avg_trip_duration)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    df = load_data(city, month, day)
    # TO DO: Display counts of user types
    df.rename(columns={'User Type':'User_Type'}, inplace=True)
              
    customer = df.query('User_Type == "Customer"')
    subscriber = df.query('User_Type == "Subscriber"')
                   
    customers = customer['User_Type'].count()
    subscribers = subscriber['User_Type'].count()
                   
    user_summary = 'User Types: There are {} customers and {} subscribers.'
    print(user_summary.format(customers, subscribers))    

    # TO DO: Display counts of gender
    if city in ['chicago.csv', 'new_york_city.csv']:
        female = df.query('Gender == "Female"')['Gender'].count()
        male = df.query('Gender == "Male"')['Gender'].count()
        null = df['Gender'].isnull().sum()

        gender = 'There are {} male users, {} female users, and {} unspecified users.'
        print(gender.format(male, female, null))
    else: 
        print('Gender Statistics: There are no gender stats to display.')

    # TO DO: Display earliest, most recent, and most common year of birth
    if city in ['chicago.csv', 'new_york_city.csv']:
        earliest_yob = df['Birth Year'].min()
        latest_yob = df['Birth Year'].max()
        common_yob = df['Birth Year'].mode()[0]

        yob_summary = 'User Year of Birth Statistics: Earliest Year - {}, Latest Year - {}, Most Common Year- {}'
        print(yob_summary.format(earliest_yob, latest_yob, common_yob))
    else:
        print('User Year of Birth Statistics: There are no year of birth stats to display.')
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
