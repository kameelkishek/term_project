import pandas as pd
import geopandas as gpd
import numpy as np
import fiona
import seaborn as sns
import matplotlib.pyplot as plt
import folium
import sys

user_input = sys.argv[1]
#Reading in EPA's Environmental Justice data
#Source: EPA
df = gpd.read_file('EJSCREEN_2021_StatePctile_Tracts.gdb')
tx = df[df['STATE_NAME']=='Texas']
tx.to_crs(4326,inplace=True)
##10 indicators as per the technical documentation [1]
poll_indices = ['PM25','OZONE','CANCER','PTRAF','DSLPM','PRE1960PCT','PTSDF','PRMP','PNPL','PWDIS']
demo_indices = ['ACSTOTPOP','MINORPCT','LOWINCPCT','LESSHSPCT','LINGISOPCT','UNDER5PCT','OVER64PCT']
tx = tx[(['Shape_Length','Shape_Area','geometry']+poll_indices+demo_indices)]

#Normalizing the data 
tx_norm = tx.copy()
tx_norm[['CANCER','PTRAF','DSLPM','PTSDF','PRMP','PNPL','PWDIS']] = round((tx_norm[['CANCER','PTRAF','DSLPM','PTSDF','PRMP','PNPL','PWDIS']] -tx_norm[['CANCER','PTRAF','DSLPM','PTSDF','PRMP','PNPL','PWDIS']].min())/(tx_norm[['CANCER','PTRAF','DSLPM','PTSDF','PRMP','PNPL','PWDIS']].max()-tx_norm[['CANCER','PTRAF','DSLPM','PTSDF','PRMP','PNPL','PWDIS']].min()),3)*100
tx_norm['dem_index'] = (tx_norm['LOWINCPCT']+ tx_norm['MINORPCT'])/2

#Finding the mean of the indicators and creating a dictionary
means = list(tx_norm[['CANCER','PTRAF','DSLPM','PTSDF','PRMP','PNPL','PWDIS','PRE1960PCT','PM25','OZONE']].mean())
indices = list(['CANCER','PTRAF','DSLPM','PTSDF','PRMP','PNPL','PWDIS','PRE1960PCT','PM25','OZONE'])
means_indices = dict(zip(indices,means))


if user_input in poll_indices:
    tx_poll = tx_norm[(tx_norm[user_input] >means_indices[user_input])]
    tx_poll = tx_poll[[user_input,'ACSTOTPOP','LOWINCPCT','MINORPCT','geometry']]
    tx_poll = tx_poll.round(3)
    
    #Reading in counties
    us_county = gpd.read_file('US_COUNTY_SHPFILE/US_county_cont.shp')
    tx_county = us_county[us_county['STATE_NAME'] == 'Texas']

    #Aggregating polluted tracts and  counties
    county_ref = gpd.sjoin(left_df=tx_poll, right_df=tx_county, how='left')
    #polluted_counties = county_ref.dissolve(by='NAME',as_index=False,aggfunc=({"ACSTOTPOP":"sum",user_input:"mean"}))


    m = county_ref.explore(
        column=user_input,  # make choropleth based on "BoroName" column
        tooltip=('ACSTOTPOP','LOWINCPCT','MINORPCT','NAME'),
        scheme="naturalbreaks",  # use mapclassify's natural breaks scheme
        legend=True, # show legend
        k=10, # use 10 bins
        legend_kwds=dict(colorbar=True), # do not use colorbar
        name="poll_tracts" # name of the layer in the map
    )

    m 

    m.save('environmental_indices.html')
else:
    print('Index not found! Please input one of the environmental indices listed in the README file')






