#!/usr/bin/env python
import argparse
import csv
from datetime import datetime, timedelta
from dateutil.parser import parse
import numpy as np
import matplotlib.pyplot as plt

def days_in_month(month):
    if (month == 1 or month == 3 or month == 5 or month == 7 or 
            month == 8 or month == 10 or month == 12):
        return 31.
    elif month == 4 or month == 6 or month == 9 or month == 11:
        return 30.
    elif month == 2:
        return 28.25
    else:
        return -1.

def get_postdate_tuple(date, post_tree):
    # return a tuple with the date, and the wordcount on that date
    if date.year in post_tree:
        year_tree = post_tree[date.year]
        if date.month in year_tree:
            month_dict = year_tree[date.month]
            if date.day in month_dict:
                return (date, month_dict[date.day])
    return (date, 0)

def read_entries_wordcounts(entries_file):
    ef = open(entries_file)
    reader = csv.DictReader(ef)

    posts = []
    post_tree = {}

    earliest_datetime = None
    latest_datetime = None

    for row in reader:
        wc = int(row['wordcount'])
        dt = parse(row['datetime'])

        # capture the earliest and latest post datetimes
        if earliest_datetime == None or dt < earliest_datetime:
            earliest_datetime = dt
        if latest_datetime == None or dt > latest_datetime:
            latest_datetime = dt
        
        # capture the wordcount of each post, which is by default in order from latest to earliest
        posts.append(wc)

        # capture a 'tree' of year to month to day of wordcounts
        if dt.year in post_tree:
            year_tree = post_tree[dt.year]
            if dt.month in year_tree:
                month_dict = year_tree[dt.month]
                if dt.day in month_dict:
                    month_dict[dt.day] += wc
                else:
                    month_dict[dt.day] = wc
            else:
                year_tree[dt.month] = { dt.day : wc }
        else:
            post_tree[dt.year] = { dt.month : { dt.day : wc } }

    posts.reverse()

    print 'earliest post date : ', earliest_datetime.date()
    print 'latest post date   : ', latest_datetime.date()

    # capture the wordcount of every date from earliest to latest (including dates with no posts)
    numdays = (latest_datetime.date() - earliest_datetime.date()).days
    dates = [get_postdate_tuple(latest_datetime.date() - timedelta(days=x), post_tree) for x in range(0, numdays+1)]
    dates.reverse()

    return posts, dates, post_tree

def calculate_entries_stats(entries_file):
    running_avgs = [10, 30, 90, 180, 360]
    posts, dates, post_tree = read_entries_wordcounts(entries_file)

    for n in running_avgs:
        plt.plot(np.convolve(posts, np.ones(n)/n, 'same'))
        plt.show()

    # dates_avg.append(np.convolve(zip(*dates)[1], np.ones(n)/n, 'same'))



def main():
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument("-i", "--input", required=True, action="store", dest="file", help="Input file to parse")
    
    args = args_parser.parse_args()
    calculate_entries_stats(args.file)

if __name__ == "__main__":
    main()
