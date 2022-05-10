# Browser Automation and Experiment Tool

## Contents
* **wire.py**: Experimental tool that uses Selenium Wire to crawl a list of websites and extract advertisements from a measurement site
* **data1**: Dataset folder from Experiment 1, captured and extracted entirely by wire.py
* **data2**: Dataset folder from Experiment 2, captured using wire.py and extracted manually (invalid due to bot detection and headless Chromium)
* **data3**: Dataset folder from Experiment 3, captured using wire.py and extracted manually
* **geolocation_webs.json**: JSON dictionary of Tranco list sites that utilize Geolocation API functions
* **ExperimentHelper.py**: Helper functions used to generate environment variables for experiment
* **analyzer.py**: Google Vision API label generation file
* **travelurls.txt**: List of travel-related websites used in Experiment 1-3
* **electronics.txt**: Unused list of electronics-related websites
* **agents.txt**: List of approximately 10,000 User-Agent strings randomly sampled by User-Agent browser configuration
* **d2_adtypes/categories.txt**: Files showing how ads were categorized during Experiment 2
* **d3_adtypes/categories.txt**: Files showing how ads were categorized during Experiment 3
