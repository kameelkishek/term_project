# term_project
This repository is the ME397M final project submission
The HTML file and JPG are the results of both python scripts which are explained as follows:

term_project.py:
This is a python script used for data cleaning, manipulation, and mapping as explained in details in the project submission report.
The results of this script are two JPG's titled 'Distribution of power plants in polluted vs. non-polluted areas.jpg' and 'Demographic index distribution across regions of interest '
This script uses 3 datasets which are included in this repository: 'EJSCREEN_2021_StatePctile_Tracts.gdb' , 'US_COUNTY_SHPFILE/US_county_cont.shp' , 'PowerPlants_US_EIA'

term_app.y:
This script is an edited version of term_project.py where the user inputs one of following environmental indicators (input as shown on the right):
•	Particulate Matter 2.5 (μg/m3) – PM25
•	Ozone (ppb) - OZONE
•	Diesel Particulate Matter (μg/m3) - DSLPM
•	Air Toxics Cancer Risk (x per million population) - CANCER
•	Traffic Proximity (annual average of vehicle count divided by distance) - PTRAF
•	Lead Paint (percent of houses built before 1960) – PRE1960PCT
•	Risk Management Plan (RMP) Facility Proximity (count of RMP facilities within 5 km) - PRMP
•	Hazardous Waste Proximity (count of facilities within 5 km) - PTSDF
•	Superfund Proximity (count of sites within 5 km) – PNPL 
•	Wastewater Discharge (toxicity weighted stream concentration divided by distance) - PWDIS

The result is an HTML file titled 'environmental_indices.html'
