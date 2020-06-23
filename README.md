# StoryPlaces-Research-Project

The JSON formatter can be used to read in the JSON in it's original format and and it saves a JSON that can be used in PANDAS. Follow the instructions in the script and paste the file path in the variable and run it and you'll have a workable JSON in the script directory.

The CTIN Research script performs the exploratory data analysis and saves the result as the csv files also included. This is so we can access the relevant datasets without rerunning script and cells.

The CTIN Research Deep Reader Classification performs the more advanced data analysis. It's a separate script so that it's not reliant on the other script to run before I can get results, thus saves performance and time. Since I have stored the resultant data frames in the Datasets folder, I can access the exploratory data analysis results in a single line. It classifies the readers based on a number of parameters, such as number of pages read and total time reading. These 2 variables are the driving force behind the classifier.

The Shelleys Heart script retrieves necessary information and formats it to be used in deeper reader classification such as the locations of each page. It's also where the Haversine function is, which finds the distance between 2 locations using latitude and longitude 

The Choice Analysis script tries to find patterns in the choices that people make with Shelley's Heart. It holds a dictionary that links each node to each connected node. It also holds a lot of important functions to traverse the graphically representation of Shelley's Heart and allows me to analyse people's choices with their experiences throughout Shelley's Heart
