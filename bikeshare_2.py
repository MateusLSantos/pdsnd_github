import time
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ["january", "february", "march", "april", "may", "june"]

DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    # Setup
    print('Hello! Let\'s explore some US bikeshare data!')
    cities = ["chicago", "new york city", "washington"]
    city = ""
    
    # get user input for city (chicago, new york city, washington). 
    while city.lower() not in cities:
        city = input("\nWhat city data would you like to see?\n")
        if city.lower() not in cities:
            print("\nPlease enter a valid city.\n")

    # get user input for month (all, january, february, ... , june)
    month = ""
    while month.lower() not in MONTHS and month.lower() != "all":
        month = input("\nWhat month would you like to analyze?\n")
        if month.lower() not in MONTHS and month.lower() != "all":
            print("\nPlease enter a valid month.\n")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ""
    while day.lower() not in DAYS and day.lower() != "all":
        day = input("\nWhat weekday would you like to analyze?\n")
        if day.lower() not in DAYS and day.lower() != "all":
            print("\nPlease enter a valid weekday.\n")
    
    # Selecting the correct index for Pandas
    # Month indexes start in 1 on Pandas Datetime
    if month != "all":
        month = MONTHS.index(month) + 1
        
    if day != "all":
        day = DAYS.index(day)
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
    df['day'] = df['Start Time'].dt.weekday
    
    # Filtering by month or day, except when user selects "all"
    if month != "all":
        df = df[df["month"] == month]
    if day != "all":
        df = df[df["day"] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("The most common month was {}.".format(MONTHS[df["Start Time"].dt.month.mode()[0] - 1].capitalize()))

    # display the most common day of week
    print("The most common day of the week was {}.".format(DAYS[df["Start Time"].dt.weekday.mode()[0]].capitalize()))

    # display the most common start hour
    print("The most common hour was {}h.".format(df["Start Time"].dt.hour.mode()[0]))

    # Performance display
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("The most commonly used start station is {}.".format(df["Start Station"].mode()[0]))

    # display most commonly used end station
    print("The most common end station is {}.".format(df["End Station"].mode()[0]))

    # display most frequent combination of start station and end station trip
    df["Combined Trip"] = df["Start Station"] + " to " + df["End Station"]
    print("The most common trip is from {}.".format(df["Combined Trip"].mode()[0]))

    # Performance display
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("The total time spent traveling was {} seconds.".format(df["Trip Duration"].sum()))

    # display mean travel time
    print("The mean travel time was {} seconds.".format(df["Trip Duration"].mean()))

    # Performance display
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("These are counts for each user type: ")
    print(df["User Type"].value_counts(), "\n")        

    # Display counts of gender
    try:
        df["Gender"] # Checking if this column exists
        print("These are counts for each gender: ")
        print(df["Gender"].value_counts(), "\n")    
    except:
        print("No gender data found.")

    # Display earliest, most recent, and most common year of birth
    try:
        df["Birth Year"] # Checking if this column exists
        print("The earliest birth year of a rider was {}.".format(int(df["Birth Year"].min())))
        print("The most recent birth year of a rider was {}.".format(int(df["Birth Year"].max())))
        print("The most common birth year of a rider was {}.".format(int(df["Birth Year"].mode())))
        
    except:
        print("No birth year data found.")

    # Performance display
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df, i):
    """ Displays 5 lines of raw data starting from index i.
        
        Returns True if there are more lines to be read or False 
        if reached the end of the data.
    """
    
    if i + 5 < len(df):
        print(df[i:i+5])
        return True
    else:
        print(df[i:-1])
        print("You reached the end of the data.\n")
        print('-'*40)
        return False
        

def main():
    while True:
        
        # Filtering and Loading
        city, month, day = get_filters()
        df = load_data(city, month, day)

        # Stats functions
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        # Checking if user wants to see 5 rows of data.
        while True:
            i = 0
            answer = input("\nWould you like to see 5 rows of raw data? Enter yes or no.\n").lower()
            if answer == "yes": # Different text after user sees the first 5 rows
                raw_data(df, i)
                while True:
                    answer2 = input("\nWould you like to see 5 more rows of raw data? Enter yes or no.\n").lower()
                    if answer2 == "yes":
                        i += 5
                        raw_data(df, i)
                        continue
                    elif answer2 == "no":
                        print("Thank you for looking at this project. Have a nice day!")
                        break
                    else:
                        print("Invalid answer. Please enter yes or no.")
                        continue
                break
            elif answer == "no":
                print("Thank you for looking at this project. Have a nice day!")
                break
            else:
                print("Invalid answer. Please enter yes or no.")
        

        # Restart
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
