"""
Pseudocode for Holiday Manager
Aaron Janaszak
"""

# import libraries

# loop for url 2020-2024
    # for i in range(0, 5):
        # html = getHTML('https://www.timeanddate.com/holidays/us/202' + str(i))

# import provided json
    # as lists?

# scrape url to get names, dates of holidays

# convert dates from 'Jan 1, 202x' format to 'yyyy-mm-dd' format
    # custom function

# combine provided json to scraped data in lists

# use lists to build dictionaries

# build class 'Holiday' w/name and date

# use loop through dict to apply Holiday class

# find weather API
    # apply to model by using this week as input dates
    # easier to hardcode dates for this week
    # don't know yet, so we'll se

# write functions for 5 menu options
    # 4 menu options, 5 = exit
    # filter dates with filter/lambda

# use main() to trigger running

# Add Holiday
    # input name
    # input date
        # check date str = 10 chars
    # add name and date to lists, update dict, update Class object

# Remove Holiday
    # ask for name
    # loop 'while exists'
        # find index of name
        # del index from name/date lists 
    # update dict, Class object

# View Holidays
    # calc date range off of input year and week#
    # lambda to filter class object within range

# Save
    # use json dump(s) 
