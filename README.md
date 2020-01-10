# Climate or Weather?

<p align="center">
  <img src="images/header.jpg" width = 900 height = 60>
</p>

## Test Hypothesis that High Temperature Observation is just a result of weather variability

*Capstone I Project for Galvanize Data Science Immersive, Week 4*

*by Paul Miles*


## Table of Contents
- [Introduction](#introduction)
  - [Background](#background)
  - [The Data](#the-data)
  - [Question and Hypothesis](#question-and-hypothesis)
  - [Methodology](#methodology)
- [Exploratory Data Analysis](#exploratory-data-analysis)
- [Web App](#web-app)


# Introduction

## Background

As a manager, it is important to consider how your expectations of employees could impact their ability to maintain a healthy work-life balance, since worker productivity is dependent on the degree to which basic needs have been met.

To borrow from Aristotle,
> "Man is by nature a social animal."

So, it seems that social connection might qualify as a basic human need that impacts productivity.

Aristotle also claims that
> "Society precedes the individual... Anyone who either cannot lead the common life or is so self-sufficient as not to need to, and therefore does not partake of society, is either a beast or a god."

But how do we help each other find the right level of social connection, so that we can thrive in that sweet spot between distraction and isolation?

This two-tailed postulate suggests that people who are not actively social will tend to be on the extremes when it comes to performance. In general, is this true? When people develop close relationships with others, is their overall productivity inherently different from those who aren't as connected to others?

## The Data

Data are sourced from the NOAA - Historical Climatology Network
(https://www.climate.gov/maps-data/dataset/daily-temperature-and-precipitation-reports-data-tables)


## Question and Hypothesis

Are the weather conditions at a given day and location a result of climate change or normal variability?

## Methodology

<p align="center">
  <img src="images/methodology.png" width = 800>
</p>

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

# Web App

<p align="center">
    <br>
    <a href="http://3.134.110.25:8080/"> Climate or Weather? Web-App </a>
</p>

[Back to Top](#Table-of-Contents)