#!/usr/bin/python3
# append to a dataframe a.append(pd.DataFrame({'close':99.99},index=[datetime.datetime.now()])
import matplotlib.pyplot as plt
from matplotlib import gridspec
import pandas as pd
import sys
import os
import argparse
import datetime
import numpy
import random
from filelock import Timeout, FileLock
from pandas_datareader import data
from numpy import NaN

random.seed(datetime.datetime.now())

# Create plot figures file


def PlotSave(fig):
    global graphsCreated
    #     emf, eps, pdf, png, ps, raw, rgba, svg, svgz
    #     for ext in [ ".png", ".jpeg", ".svg", ".eps", ".raw"]:
    #         filePath = outputFilepath + str(fig.number) + ext
    #         plt.figure(fig.number)
    #         plt.savefig(filePath)
    filePath = outputFilepath + str(fig.number) + outputExtension
    plt.figure(fig.number)
    plt.savefig(filePath)
    graphsCreated.append(filePath)
    print('Created plot %s.' % (filePath))


def GetRandomPrice(old_price, minPrice, maxPrice, volatility=0.30):
    new_price = maxPrice+1
    # While new price is invalid
    while (new_price > maxPrice) or (new_price < minPrice):
        rnd = random.random()
        change_percent = 2 * volatility * rnd
        if (change_percent > volatility):
            change_percent -= (2 * volatility)
        change_amount = old_price * change_percent
        new_price = old_price + change_amount
        if (new_price < 4):
            new_price += 0.6
    return new_price


# Const objects
# #####################################################
lockTimeout = 5 * 60
variability = 0.30
plotsPath = 'scenarios/'
outputExtension = '.svg'
# Game settings
gameDays = 20
gameMaxPrice = 12
gameStocks = ['crayons', 'cars', 'stone', 'wood', 'paper']
gameStocksTickers = ['o', 's', 'D', 'v', 'P']

# Arguments and config
# #####################################################
parser = argparse.ArgumentParser()
parser.add_argument('-n', '--stockCode', type=str,
                    required=True, help='Stock name code')
parser.add_argument('-x', '--variability', type=float,
                    required=False, help='Variability')
parser.add_argument('-g', '--plotToFile', action='store_true',
                    required=False, help='Plot to file')
args = parser.parse_args()


# Use non-interactive backend when plot to file used
if (args.plotToFile):
    import matplotlib
    matplotlib.use('Agg')

# Set variaibility
if (args.variability):
    variability = args.variability
print('Variability is %2.2f.' % (variability))


# Dynamic variables
# #####################################################
outputFilename = 'Scenario'+datetime.datetime.now().strftime('%y%V.%d%H%M')
outputFilepath = plotsPath + outputFilename
graphsCreated = []
stocks = []
time = range(1, gameDays+1)

# Create stock data for all stocks
for stockName in gameStocks:
    data = []
    price = random.choice(range(1, gameMaxPrice+1))
    for index in time:
        data.append(price)
        price = GetRandomPrice(price, 1, gameMaxPrice, variability)
    stocks.append(numpy.around(data))
    print(stockName)
    print(data)


# PLOTS
# #####################################################
fig = plt.figure(figsize=(16.0, 9.0))
plot1 = plt.subplot()
# Plot all stocks
for index in range(len(stocks)):
    plt.plot(time, stocks[index])
    plt.plot(time, stocks[index],
             gameStocksTickers[index], color='black', ms=8)
    plt.plot(time, stocks[index],
             gameStocksTickers[index], label=gameStocks[index])

plt.legend(loc='upper left')
plt.grid()
plt.xticks(numpy.arange(1, gameDays+1, step=1))
plt.yticks(numpy.arange(1, gameMaxPrice+1, step=1))
# plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
# plt.gca().xaxis.set_minor_formatter(mdates.DateFormatter('%d'))
# bollinger.PlotAbsDeviation()
# plt.minorticks_on()
# plt.grid(b=True, which='major', axis='both',color='k')
# plt.grid(b=True, which='minor', axis='both')

# Plot to file or show
if (args.plotToFile):
    PlotSave(fig)

# Show all plots
if (not args.plotToFile):
    plt.show()
