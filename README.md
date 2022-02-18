### GEMINI CURRENCY ALERTING TOOL ###

### USAGE
./gemini.py --help, -h

HELP:
    usage: gemini.py [-h] --pair PAIR [--dev DEV]

    Gemini Currency Alerting Tool

    optional arguments:
    -h, --help   show this help message and exit
    --pair PAIR  Enter a currency pair. ie. btcusd
    --dev DEV    Enter the maximum deviation allowed

./gemini.py --pair {CURRENCY PAIR} --d {DEVIATION THRESHOLD}

CURRENCY PAIR:
    This is the trading pair symbol Gemini trades on the exchange. This value is essential and must be supplied. If no CURRENCY PAIR is defined the script will log an ERROR and display the current list of symbols to use.

DEVIATION THRESHOLD:
    This value is an integer that acts as the threshold for the alerting mechanism. It is possible for standard deviations to exceed precision defined in the script which may result in "divide by zero" error. If this occurs the script will log an error stating the divide by zero error and ask to increase precision of the rounding digits of the {std_dev} value.

    NOTE: Deviation will default to an absolute value of (1) if not supplied as argument. 

### FURTHER IMPROVEMENTS AND ENHANCEMENTS

More development can be done to allow an additional command line argument to allow the user to specify the precision of the std_dev value with a default value present.

Further enhancements to allow for log level alerting (ie. 10-debug, 20-info, 30-warning, 40-error, 50-critical) for integration into Nagios, Slack and PagerDuty to ensure visibility of exceeded thresholds.

Additional checks can be developed to add functionality to enable buy, trade, sell thresholds for all currency pairs that can be user specified.
Other interesting checks you might implement to alert on market behaviour

### MY APPROACH

For me the real challenge was to capture the API JSON in a way that could be manipulated. Luckily the Gemini documentation was perfect in allowing me to see how the data could be ingested and more specifically what data.

Since I am not developing in Python regularly it took some effort sharpening my skills ingest the API data and ETL the output. Also, it has been awhile since I performed any statistical analysis. I could calculate the mean, variance and standard deviation fine but getting the absolute magnitude took me a bit to get both of my brain cells working again :)

The total time it took to develop was about 4 hours.

### NOTICE

Copyright 2022. Developed and written by Sean Hurst.

