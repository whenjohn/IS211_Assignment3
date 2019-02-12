#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""IS 211 - Assignment 3"""


import urllib2
import argparse
import logging
import logging.handlers
import csv
import re
import operator
import sys

def main():
    """Main function that runs at start of program.

    Args:
        --url (string): command line parameter of url

    Attributes:
        user_input (int): The num user selects
        user_select_column (int): The column based on user selection
        pattern_selection (dict): The array that is used to count user selection

    Returns:
        User promted to enters info. Program will perform action and return
            results
        Outputs to error.log file

    Examples:
        >>> $ python assignment3.py --url  "http://website.com/birthdays100.csv"
        >>> What would you like to do?
        1 - Search for image hits
        2 - Find most popular browser
        3 - Sorted list of hits by hour of day
        4 - Quit
        Please enter 1 - 3: 1
        Image requests account for 65.74% of all requests
    """
    # Set up logger named assignment2 with output level
    my_logger = logging.getLogger('assignment3')
    my_logger.setLevel(logging.WARNING)
    # Add the log message handler to the logger. output to file
    handler = logging.FileHandler('errors.log')
    my_logger.addHandler(handler)


    # Enable command-line arguments
    parser = argparse.ArgumentParser()
    # Add command-line argmuemnt --url that recives url string
    parser.add_argument('--url')
    args = parser.parse_args()


    # Ensure that argument has returned URL
    if not args.url:
        print "Error URL argument missing"
        my_logger.error('Error URL argument missing')
        sys.exit()
    else:
        req = urllib2.Request(args.url)


    # Retreive file from url
    try:
        response = urllib2.urlopen(req)
    except urllib2.HTTPError as exception:
        print "Error {}".format(exception.code)
        my_logger.error('Error Download: {}'.format(exception.code))
        sys.exit()
    except urllib2.URLError as exception:
        print "Error {}".format(exception.reason)
        my_logger.error('Error Download: {}'.format(exception.reason))
        sys.exit()


    # process data from url into csv format
    csv_file = csv.reader(response)


    # Begin asking user program selection
    while True:
        try:
            print "What would you like to do?"
            print "1 - Search for image hits"
            print "2 - Find most popular browser"
            print "3 - Sorted list of hits by hour of day"
            print "4 - Quit"
            user_input = int(input("Please enter 1 - 3: "))
        except (SyntaxError, NameError) as exception:
            # what about floats?
            my_logger.error('Error: Input is incorrect. {}'.format(
                                                            exception.message))
            print('\nYou have not entered a number.\n')
            continue
        else:
            # int num entered. break loop and continue
            break


    # Assign varables based on user selections
    # 0 = image, 2 = browsers, 1 = time
    if user_input == 1:
        user_select_column = 0;
        pattern_selection = {
            'PNG':0,
            'JPG':0,
            'GIF':0
        };
    elif user_input == 2:
        user_select_column = 2;
        pattern_selection = {
            'Firefox':0,
            'Chrome':0,
            'MSIE':0,
            'Safari':0
        };
    elif user_input == 3:
        user_select_column = 1;
        pattern_selection = {
            ' 00':0,
            ' 01':0,
            ' 02':0,
            ' 03':0,
            ' 04':0,
            ' 05':0,
            ' 06':0,
            ' 07':0,
            ' 08':0,
            ' 09':0,
            ' 10':0,
            ' 11':0,
            ' 12':0,
            ' 13':0,
            ' 14':0,
            ' 15':0,
            ' 16':0,
            ' 17':0,
            ' 18':0,
            ' 19':0,
            ' 20':0,
            ' 21':0,
            ' 22':0,
            ' 23':0
        }
    elif user_input == 4:
        print('Ok bye.')
    else:
        print('Make a valid selection\n')
        main()

    # Execute logic on user selection
    if user_input < 4:
        # Count based on user selection
        count_result = countRowByAction(user_select_column,
                                          pattern_selection, csv_file)

        # Process count results and display message to user
        processResultsByAction(user_select_column, count_result[0],
                              count_result[1], count_result[2])

        print '\n\n'

        # After action complete, prompt user to make selection again
        main()


def countRowByAction(action_column, result_dictionary, file):
    """Count rows from file of given column against on dictionary keys

    Args:
        action_column (int): Based on user selection. Only apply logic to the
            column specifed.
        result_dictionary (dictionary): based on user selection. Dictionaty key
            is used to search for value from the file row. And the Dict value is
            used to count the occurance of it in the file row.
        file (list): This list csv processed data from the url

    Attributes:
        total_row_count: (int): The running count of all rows
        action_row_count (int): The running count of rows affected by action
        result_dictionary (dict): The incrimented results of the action

    Returns:
        Returns result_dictionary, total_row_count, action_row_count
        Raise exceptions

    Examples:
    """
    total_row_count = 0
    action_row_count = 0

    for row in file:
        for key in result_dictionary.keys():
            if re.search(key, row[action_column], re.IGNORECASE):
                result_dictionary[key] += 1
                action_row_count += 1
                #print row[action_column]
                break

        total_row_count += 1

    return result_dictionary, total_row_count, action_row_count


def processResultsByAction(action_col, count_array, total_count, action_count):
    """Process count by user selection (action, col) and return results

    Args:
        action_col (int): Based on user selection. Only apply logic to the
            column specifed.
        count_array (dictionary): based on user selection. Dictionaty key
            is used to search for value from the file row. And the Dict value is
            used to count the occurance of it in the file row.
        total_count (int):
        action_count (int):

    Attributes:
        sorted_tuples: (tuple): For action: hits by hour, process the array into
            a tuple and use the sorted module to sort by value

    Returns:
        Returns result_dictionary, total_row_count, action_row_count
        Raise exceptions

    Examples:
    """
    if (action_col == 0):
        print "Image requests account for {0:.2%} of all requests ".format(
                                            action_count/float(total_count))
    elif (action_col == 2):
        print'{} is the most popular browser of all requests.'.format(max(
                                            count_array, key=count_array.get))
    elif (action_col == 1):
        sorted_tuples = sorted(count_array.items(), key=operator.itemgetter(1),
                                                                 reverse=True)
        for hour_of_day in sorted_tuples:
            print "Hour{}".format(hour_of_day[0])+" has {}".format(
                                                        hour_of_day[1])+" hits"
    else:
        print "Error"


# Run main if file direcrly executed
if __name__ == '__main__':
    main()
