# -*- coding: utf-8 -*-
# Purpose   : Script to get PI Data in a CSV
# Input     : PI Server Name:(PIServerName variable inside the script) , List of PI Tags to retrive (List the tags in the same folder as the script)
# Output    : PI Data of the Tags in CSV format
# Authors:
# Jordi Dekker (jordi.dekker@shell.com) - Orginal Author
# Karthick Shashi (karthick.shashi@shell.com) - Modified for Oman-PDO
# Mithun  (Mithun.cdharman@shell.com) - Modified for SMEP
# Version 1.3
# Last updated: 05-Feb-2019 13:00:00

import logging
import pandas as pd

from win32com.client.dynamic import Dispatch
from datetime import datetime

logger = logging.getLogger()

################### Define the PI Server here . To get the right name-> open the tool "AboutSDK" -> go to connections -> get the name of the PI Server from the list of available PI Servers
PIServerName = 'DSAPPICOLL'  # Name of the PIServer
StartTime = '12-07-2018 00:00:00'  # StartTime in LocalTime in "DD-MM-YYYY HH:MM:SS" format
EndTime = '12-17-2018 11:47:00'  # Endtime in LocalTime in "DD-MM-YYYY HH:MM:SS" format
RetrivalInterval = '10m'  # Frequency of retrival f Data points from PI
Input_TagListCSV = 'taglist.csv'  # List of PI Tags
Output_PIDataCSV = 'pi_data_op.csv'  # Retrived data of PITags in LocalTimeStamp (not in UTC)


################### Change the PI Server name to the correct PI Server ################


class PiPython(object):
    def __init__(self, pi_server=PIServerName):
        self.pi_srv = Dispatch('PISDK.PISDK').Servers(pi_server)
        self.pi_time = Dispatch('PITimeServer.PITime')
        self.pi_timeintervals = Dispatch('PITimeServer.TimeIntervals')
        self.pi_timeformat = Dispatch('PITimeServer.PITimeFormat')

    def get_snapshot(self, tag_name, col_name='value'):
        """Retrieve the last known value of the PI-tag

        Args:
            tag_name (str): PI tag name
            col_name (str): Desired column name of the returned pandas dataframe

        Returns
            pandas dataframe: index=datetime, col_1=interpolated values
        """
        tag = self.pi_srv.PIPoints(tag_name)
        startTime= (self.pivalues_to_df([tag.Data.Snapshot], tag_name))
        return startTime

    def get_data(self, tag_name, t_start, t_end, t_interval):
        """Retrieve interpolated data from the PI-server

        Args:
            tag_name (str): PI tag name
            t_start (str): PI time format (ex. '*-72h')
            t_end (str): PI time format (ex. '*')
            t_interval (str): PI time format (ex. '1h')

        Returns:
            pandas dataframe: index=datetime, col_1=interpolated values
        """

        logger.info('get_data for tag `%s`' % tag_name)
        tag = self.pi_srv.PIPoints(tag_name)
        pi_values = tag.Data.InterpolatedValues2(t_start, t_end, t_interval, asynchStatus=None)
        return (self.pivalues_to_df(pi_values, tag_name))

    def get_data_multiple(self, tags, t_start, t_end, t_interval):
        """Retrieve interpolated data from the PI-server for multiple tags

        Args:
            tags (list): List of PI tag names
            t_start (str): PI time format (ex. '*-72h')
            t_end (str): PI time format (ex. '*')
            t_interval (str): PI time format (ex. '1h')

        Returns:
            pandas dataframe: index=datetime, cols=interpolated values

        """
        print("Start Date ,End date(DD:MM:YYY) & interval:")
        print(t_start,t_end,t_interval)
        logger.info('getting data for %s tags' % len(tags))
        list_of_values = []
        for tag in tags:
            df = self.get_data(tag, t_start, t_end, t_interval)
            # drop duplicated indices -> result of summer-to-winter time
            # transition. Not doing this results in the subsequent join() to
            # spiral out of control
            df = df[~df.index.duplicated()]
            list_of_values.append(df)

        df_values = pd.DataFrame().join(list_of_values, how='outer')

        return df_values

    def is_valid_tag(self, tag_name):
        """Checks whether the tag_name exists on the PI-server

        Returns boolean True in case the tag exists

        Args:
            tag_name (str): PI tag name

        Returns:
            boolean
        """
        try:
            self.pi_srv.PIPoints(tag_name)
        except:
            return False
        return True

    def pivalues_to_df(self, pivalues, col_name='value'):
        """Converts a list of PI-value objects to a pandas dataframe

        Args:
            pivalues (list): List of PI-value objects
            col_name (str): desired name of the pandas df column

        Returns:
            pandas dataframe: index=datetime, column=list_of_values
        """
        list_of_values = []
        list_of_datetimes = []
        print("PI Values:")

        for v in pivalues:
            try:

                list_of_values.append(float(v.Value))
                list_of_datetimes.append(self.epoch_to_dt(v.TimeStamp))
            except:
                pass
        print(list_of_datetimes)
        print(list_of_values)
        df = pd.DataFrame({'date': list_of_datetimes, col_name: list_of_values})
        df = df.set_index('date')
        print(df)
        return df


    def timeformat(self, arg):
        """Converts a relative time str to a PI datetime formatted string

        Args:
            arg (str): relative time string i.e. '*' or '*-24h'

        Returns:
            str: formatted datetime i.e. '17-10-2017 9:48:15'

        """
        try:
            self.pi_timeformat.InputString = arg
            return self.pi_timeformat.OutputString
        except:
            logger.error('`%s` is an invalid PI time format' % arg)
            return arg

    def epoch_to_dt(self, timestamp):
        """Convert epoch to human readable date and vice versa

        Args:
            timestamp (float): Unix epoch timestamp i.e. '1508227058.0'

        Returns:
            (datetime object)
        """
        return datetime.fromtimestamp(timestamp)

    # def WriteBackToPI(self, TagName: str, Value, TimeStamp):
    #     """Write Back Values to PI
    #
    #     Args:
    #         PIPython Obj, PITagName , Value to write, TimeStamp in LocalTime in "DD-MM-YYYY HH:MM:SS" format
    #
    #     Returns:
    #         (datetime object)
    #     """
    #     try:
    #         PIServer = self.pi_srv
    #         try:
    #             PITag = self.pi_srv.PIPoints(TagName)
    #         except Exception as e:
    #             raise ValueError("PI TagName not found in PI Server")
    #
    #         try:
    #             # you need write access on the PI Tag mentioned
    #             PITag.Data.UpdateValue(Value, TimeStamp, 0, None)
    #         except Exception as e:
    #             raise ConnectionError("Write Back to PI Failed -" + str(e))
    #
    #
    #     except Exception as e:
    #         raise ValueError("Write back failed due to ->" + str(e))


import csv

# with open('taglist.csv', 'r') as f:
#    reader = csv.reader(f)
#    your_list = list(reader)

#

tags = pd.read_csv(Input_TagListCSV)
tag_list = tags['Tags'].tolist()

if __name__ == "__main__":
    ''' Usage example '''
    pi = PiPython(PIServerName)
    df = pi.get_data_multiple(tag_list, StartTime, EndTime, RetrivalInterval)
    df.to_csv(Output_PIDataCSV)

