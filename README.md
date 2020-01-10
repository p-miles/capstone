# Climate Change or Just Weather?

<p align="center">
  <img src="img/banner.png" width = 900 height = 60>
</p>

# Web-App

<p align="center">
    <br>
    <a href="http://3.134.110.25:8080/"> Climate or Weather? Web-App </a>
    <br>
</p>

*Capstone I Project for Galvanize Data Science Immersive, Week 4*

*by Paul Miles*


## Table of Contents
- [Overview](#overview)
  - [How to Run](#how-to-run)
  - [Background](#background)
  - [The Data](#the-data)
- [Exploratory Data Analysis](#exploratory-data-analysis)
- [Results](#results)
- [Analysis](#analysis)


# Overview

## How to Run

### Click the link at the top of the page to use the web-app.

Fork this repo and download the raw data

```unix
> cd repo/data
> ftp ftp.ncdc.noaa.gov/pub/data/ghcn/daily/
> get ghcnd_hcn.tar.gz
> (ctrl-d)
> tar -xvf ghcnd_hcn.tar.gz
```

From conda python-3 environment 
Additional dependencies: 
```
> pip install geopandas, pygeo
> python app.py
```

Owner Info:
Access AWS Instance command
ssh -i "~/.ssh/instancekey.pem" ec2-user@ec2-3-134-110-25.us-east-2.compute.amazonaws.com


## Background

Weather is highly variable and people are prone to recency bias.  
Do you trust your sense when you feel like it's hotter than it used to be?

<p align="center">
  <img src="img/Weather 5 year KDEN.png" width = 800>
</p>

Use the web-app to see the historical temperature distributions and rigorously test 
if the current weather you are experiencing "normal" or a consequence of climate change?

## The Data

Data are sourced from the NOAA - Historical Climatology Network
(https://www.climate.gov/maps-data/dataset/daily-temperature-and-precipitation-reports-data-tables)


## Question and Hypothesis

Are the weather conditions at a given day and location a result of climate change or normal variability?

## Methodology

Null Hypothesis: even extreme weather is part of normal variability.
Alternative Hypothesis: or seemingly unusually high temperatures are a sign of warming
Significance level: alpha = 2%
Statistical Test: against a fitted skew-normal distribution from pre-1980 observations


[Back to Top](#Table-of-Contents)

# Exploratory Data Analysis

### Stations

Use the 1,225 weather stations that are part of the NOAA - US Historical Climate Network

<p align="center">
  <img src="img/us_hcn_map.png" width = 800>
</p>


### Date Range

Typically mid-1800's to present

### Observation Categories

* Core Elements

       PRCP = Precipitation (tenths of mm)
       SNOW = Snowfall (mm)
       SNWD = Snow depth (mm)
       TMAX = Maximum temperature (tenths of degrees C)
       TMIN = Minimum temperature (tenths of degrees C)
* Additional Elements

       average cloudiness, wind direction and speed, percent possible sun
       weather type, weather in vicinity (fog, thunder, rain, snow)


[Back to Top](#Table-of-Contents)

# Results

An example to illustrate the web-app output.
For New York City on an unseasonably warm day 2016-04-01

Solid blue: histogram from reference data pre-1980.  See Methodology(#methodology)
Blue line - ref distribution fitted with skew-normal
Red: histogram of 1980-present

In this rightward shift is indicative of a warming trend since 1980.

p-val of 1% suggests that the null-hypothesis is unlikely

<p align="center">
  <img src="img/NYC_20160401.png" width = 800>
</p>

A second example during the heat wave in Denver last summer.

<p align="center">
  <img src="img/Denver_20190820.png" width = 800>
</p>

[Back to Top](#Table-of-Contents)

# Analysis

Number of days in a year with p-val exceeding set signficance level

<p align="center">
  <img src="img/daily_ht_denver.png" width = 800>
</p>

[Back to Top](#Table-of-Contents)

# Extra

<p align="center">
  <img src="img/keywest_thisweek.png" width = 800>
</p>

[Back to Top](#Table-of-Contents)