# IS211_Assignment3

# Instructions
1. Run python assignment3.py --url "http://s3.amazonaws.com/cuny-is211-spring2015/weblog.csv"
2. Make selection at Input

(from terminal)<br />
What would you like to do?<br />
1 - Search for image hits<br />
2 - Find most popular browser<br />
3 - Sorted list of hits by hour of day<br />
4 - Quit<br />
Please enter 1 - 3:<br />

# About Selections
Selection 1 will iterate through rows for all images in column base on user
selection. Using a regex to search for these strings 'jpg', 'gif', and 'png'.
Not case sensitive. Will count and sum up.
Will return back the percentage of hits that were images.

Selection 2 will iterate through rows in column based on user. Will search and
count each browsers.'Firefox', 'Chrome', 'MSIE', and 'Safari'. Not case
sensitive.

Selection 3 will iterate through rows in column based on user. Will search
and count of each occurrence the type of hour string. For ex. ' 12:' or '02:'.
since this is unique characters that represent hour, I thought it would be
easier than to use datetime to covert each row into datetime obj and them
apply actions on them.
