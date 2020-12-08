import datetime
import platform

import pandas as pd

# Datasets scraped can be found in the following URL's:
# ¹ Johns Hopkins: https://github.com/CSSEGISandData/COVID-19
# ² Our World In Data: https://github.com/owid/covid-19-data/tree/master/public/data
# ³ New York Times: https://github.com/nytimes/covid-19-data

# Different styles in zero-padding in date depend on operating systems
if platform.system() == 'Linux':
    STRFTIME_DATA_FRAME_FORMAT = '%-m/%-d/%y'
elif platform.system() == 'Windows':
    STRFTIME_DATA_FRAME_FORMAT = '%#m/%#d/%y'
else:
    STRFTIME_DATA_FRAME_FORMAT = '%-m/%-d/%y'
def confirmed_report():
    # Returns time series version of total cases confirmed globally
    df = pd.read_csv(
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
    return df


def deaths_report():
    # Returns time series version of total deaths globally
    df = pd.read_csv(
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
    return df


def recovered_report():
    # Return time series version of total recoveries globally
    df = pd.read_csv(
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
    return df


def realtime_growth(date_string=None, weekly=False, monthly=False):
    """[summary]: consolidates all reports, to create time series of statistics.
    Columns excluded with list comp. are: ['Province/State','Country/Region','Lat','Long'].

    Args:
        date_string: must use following date formatting '4/12/20'.
        weekly: bool, returns df for last 8 weks
        monthly: bool, returns df for last 3 months
    Returns:
        [growth_df] -- [growth in series]
    """
    df1 = confirmed_report()[confirmed_report().columns[4:]].sum()
    df2 = deaths_report()[deaths_report().columns[4:]].sum()
    df3 = recovered_report()[recovered_report().columns[4:]].sum()

    growth_df = pd.DataFrame([])
    growth_df['Confirmed'], growth_df['Deaths'], growth_df['Recovered'] = df1, df2, df3
    growth_df.index = growth_df.index.rename('Date')

    yesterday = pd.Timestamp('now').date() - pd.Timedelta(days=1)

    if date_string is not None:
        return growth_df.loc[growth_df.index == date_string]

    if weekly is True:
        weekly_df = pd.DataFrame([])
        intervals = pd.date_range(end=yesterday, periods=8, freq='7D').strftime(STRFTIME_DATA_FRAME_FORMAT).tolist()
        for day in intervals:
            weekly_df = weekly_df.append(growth_df.loc[growth_df.index == day])
        return weekly_df

    elif monthly is True:
        monthly_df = pd.DataFrame([])
        intervals = pd.date_range(end=yesterday, periods=3, freq='1M').strftime(STRFTIME_DATA_FRAME_FORMAT).tolist()
        for day in intervals:
            monthly_df = monthly_df.append(growth_df.loc[growth_df.index == day])
        return monthly_df

    return growth_df
