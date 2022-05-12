import pandas as pd
import geopandas as gpd
import numpy as np
import fiona
import seaborn as sns
import matplotlib.pyplot as plt

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
tx_norm[['CANCER','PTRAF','DSLPM','PTSDF','PRMP','PNPL','PWDIS','PM25','OZONE']] = (tx_norm[['CANCER','PTRAF','DSLPM','PTSDF','PRMP','PNPL','PWDIS','PM25','OZONE']] -tx_norm[['CANCER','PTRAF','DSLPM','PTSDF','PRMP','PNPL','PWDIS','PM25','OZONE']].min())/(tx_norm[['CANCER','PTRAF','DSLPM','PTSDF','PRMP','PNPL','PWDIS','PM25','OZONE']].max()-tx_norm[['CANCER','PTRAF','DSLPM','PTSDF','PRMP','PNPL','PWDIS','PM25','OZONE']].min())
tx_norm['dem_index'] = (tx_norm['LOWINCPCT']+ tx_norm['MINORPCT'])/2

#Finding the mean of the indicators
means = list(tx_norm[['CANCER','PTRAF','DSLPM','PTSDF','PRMP','PNPL','PWDIS','PM25','OZONE']].mean())
indices = list(['CANCER','PTRAF','DSLPM','PTSDF','PRMP','PNPL','PWDIS','PM25','OZONE'])

#Creating a dataframe with all the tracts/areas where at least one environmental indicator is greater than the state average
tx_poll = tx_norm[(tx_norm['CANCER'] >means[0]) | (tx_norm['PTRAF'] >means[1]) | (tx_norm['DSLPM'] >means[2]) | (tx_norm['PTSDF'] >means[3]) | (tx_norm['PRMP'] >means[4]) | (tx_norm['PNPL'] >means[5]) | (tx_norm['PWDIS'] >means[6]) | (tx_norm['PM25'] >means[7]) | (tx_norm['OZONE'] >means[8])]

#Reading in counties
us_county = gpd.read_file('US_COUNTY_SHPFILE/US_county_cont.shp')
tx_county = us_county[us_county['STATE_NAME'] == 'Texas']

#Creating a demographic index column which, per EPA, is the average of the low income and minority percentages
tx_poll['dem_index'] = (tx_poll['LOWINCPCT']+ tx_poll['MINORPCT'])/2

#Aggregating polluted tracts and  counties
county_ref = gpd.sjoin(left_df=tx_poll, right_df=tx_county, how='left')
polluted_counties = county_ref.dissolve(by='NAME',as_index=False,aggfunc=({"ACSTOTPOP":"sum","OZONE":"mean","PTRAF":"mean","CANCER":"mean","DSLPM":"mean","PTSDF":"mean","PRMP":"mean","PNPL":"mean","PWDIS":"mean","PM25":"mean","dem_index":"mean"}))
polluted_counties1 = county_ref.dissolve(by='STATE_NAME',as_index=False,aggfunc=({"ACSTOTPOP":"sum","OZONE":"mean","PTRAF":"mean","CANCER":"mean","DSLPM":"mean","PTSDF":"mean","PRMP":"mean","PNPL":"mean","PWDIS":"mean","PM25":"mean","dem_index":"mean"}))


#Reading in power plants in Texas
#Source: EIA
pp = gpd.read_file('PowerPlants_US_EIA')
tx_pp = pp[pp['StateName']=='Texas']
tx_pp = tx_pp[['Plant_Code', 'PrimSource','Total_MW','geometry']]
tx_pp[tx_pp.isna().any(axis=1)].sum() #No NaN entries
tx_pp=tx_pp[tx_pp['PrimSource'].isin(['natural gas','coal'])]

#Plotting all the regions exceeding any environmental indicator mean
base = tx_county.plot(color="white",edgecolor='black', lw=0.25,legend=True)
tx_poll.plot(ax=base,color='#dc2f02',lw = 0.5,alpha=0.3,label='Areas with at least one air quality indicator above the state average')
polluted_counties1.plot(ax=base,color="none",edgecolor="k", lw=0.5)
tx_pp.plot(ax=base, marker='o', markersize=2,facecolor='purple',label='Coal/NG Power plants')
plt.rcParams["figure.figsize"] = (40,2)
figure = plt.gcf() 
figure.set_size_inches(8, 6)
plt.legend()
plt.xticks(color='w')
plt.yticks(color='w')
plt.title('Regions with at least one environmental indicator above state average')
plt.savefig('Distribution of power plants in polluted vs. non-polluted areas.jpg')

#Plotting these regions and the demographic index distribution
base = tx_county.plot(color="white",edgecolor='black', lw=0.25,legend=True)
tx_poll.plot(ax=base,column='dem_index',cmap='inferno',alpha=0.6,legend=True,label='hellp')
polluted_counties1.plot(ax=base,color='none',edgecolor="k", lw=0.5)
plt.rcParams["figure.figsize"] = (40,2)
plt.title('Demographic index distribution across regions of interest ')
figure = plt.gcf()
figure.set_size_inches(8, 6)
plt.legend()
plt.xticks(color='w')
plt.yticks(color='w')
plt.savefig('Demographic index distribution in polluted areas.jpg')





