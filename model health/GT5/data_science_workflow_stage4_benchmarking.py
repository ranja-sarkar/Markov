
# -*- coding: utf-8 -*-

"""
Contributors:
Ali, Zeshaan GSUK-PTX/D/S Zeshaan.Ali@shell.com
Channa, Venkata Viswanath SSSCCH-FO/XF Venkata.Channa@shell.com
Davarynejad, Mohsen SIEP-ITZ/AD Mohsen.Davarynejad@shell.com
Deo, Himat GSUK-PTX/D/S Himat.Deo@shell.com
Doherty, Andrew GSUK-PTX/D/S Andrew.Doherty@shell.com
Goodwin, Nigel GSUK-PTX/D/S Nigel.Goodwin@shell.com
Ogunseye, Tolu O GSUK-PTX/D/S Tolu.Ogunseye@shell.com
Srivastava, Anshul SSSCCH-FO/XF Anshul.Srivastava@shell.com
Subramanian, Sundar Raman SSSCCH-FO/XF S-R.Subramanian@shell.com
Vukovic, Ivana GSNL-ITPT/DA Ivana.Vukovic@shell.com
Chandrasekaran, Sridharan SSSCCH-FO/XF S.Chandrasekaran5@shell.com
Sarkar, Ranja SSSCCH-FO/XF Ranja.Sarkar@shell.com
Kumar, Jitendra SSSCCH-FO/XF Jitendra.J.Kumar3@shell.com

Created: Aug, 2019
© Copyright 2019 AND Confidential Information of Shell Global Solutions UK. All rights reserved.

Only authorised Shell employees and authorised contractors may utilise the software or codes (in source and binary forms
with or without modification) subject to the following conditions:
* Only in performance of work for Shell;
* NO licence is granted to any party not so authorised;
* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
software.

THE SOFTWARE AND/OR THE CODES ARE PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE USE OR OTHER DEALINGS OF THE SOFTWARE AND/OR THE CODES

This is the script is intended for calculating the benchmarking KPI and also to publish them for
a) Training and Testing results
b) Testing result on number of models

1. First run main/data_science_workflow_stage2_train_model.py to produce trn_pred and tst_pred results
2. Use the same configuration used in step 1 to point this code to the location where the results have been dumped
3. Run the code in a python console to allow you to generate results and plots
4. Results include
    - ***Model_Testing.csv
    - **Key**.csv
    - **trn_KPI**
    - **tst_KPI**
4. There are three types of plots.
    a) A box/line plot that shows the variation of anomaly ratio over various models
    b) A box/line plot that shows the variation of flip ratio over various models
    c) A box/line plot that shows the variation of model uptime ration over various models
    d) A weekly distribution of anomaly ratio in the form of line plot over the testing period
    e) A weekly distribution of flips ratio in the form of line plot over the testing period
    f) A weekly distribution of model uptime ratio in the form of line plot over the testing period

"""

import logging
from autologging import TRACE
from utils.FileUtils import FileUtils
from tagdata.TagData import TagData
from autologging import TRACE
import glob
import sys
import pandas as pd
import matplotlib.pyplot as plt
# import seaborn as sns

# Function Definitions

def load_file(filename):
    """
            Gets results file from the workflow stage 2 output.
            :return: pandas dataframe: index=datetime
            """
    dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
    df = pd.read_csv(filename, parse_dates=['timestamp'], date_parser=dateparse)
    df.set_index('timestamp', inplace=True)
    return df


def compute_kpi(df):
    """
            Compute the anomaly ratio, flips (alert) ratio and uptime ratio.
            :return: pandas dataframe: index=Weekly datetime
            """
    # Converting -1 to 1 and 1 to 0. This enables easy summation weekly
    df.prediction = df.prediction.replace(1, 0)
    df.prediction = df.prediction.replace(-1, 1)
    # Create new column
    df['anomaly'] = 0
    df.loc[(df['system_status'] == 'online') & (df['prediction'] == 1), 'anomaly'] = 1
    # Create new column
    df['sys_status'] = 0
    df.loc[(df['system_status'] == 'online'), 'sys_status'] = 1
    # Create new column
    df['up_time'] = 0
    df.loc[(df['system_status'] == 'online') & (df['prediction'] == 0), 'up_time'] = 1
    # Create new column
    df['updated_alert'] = 0
    df.loc[(df['system_status'] == 'online') & (df['alert'] == 1), 'updated_alert'] = 1

    resultsdf = df[['anomaly', 'updated_alert', 'up_time', 'sys_status']].resample('W').sum()
    # Compute to the two digits in decimals
    resultsdf['anomaly_ratio'] = (resultsdf['anomaly'] / resultsdf['sys_status']).round(2)
    resultsdf['alert_ratio'] = (resultsdf['updated_alert'] / resultsdf['sys_status']).round(2)
    resultsdf['uptime_ratio'] = (resultsdf['up_time'] / resultsdf['sys_status']).round(2)
    resultsdf.rename({'updated_alert': 'alert'}, axis=1, inplace=True)

    return resultsdf


def generate_visualization_model_comparison(final_df, location):
    """
            Generate visualization for comparing different models
            :return: nil
            """
    # Writing the entire model name in the box plot is difficult and hence aliasing as Model_1, Model_2
    list_columns = [col for col in final_df.columns if 'anomaly_ratio' in col]
    xtickmark = []
    for count in range(len(list_columns)):
        temp = 'Model_' + str(count + 1)
        xtickmark.append(temp)

    # This creates a directory of the Key name and the model name for reference
    key_df = pd.DataFrame()
    key_df['Key'] = xtickmark
    key_df['Model Name'] = list_columns

    # Plotting box plot for anomaly ratio
    plt.figure(1)
    final_df[list_columns].boxplot()
    plt.title('Anomaly Ratio')
    plt.ylabel('Anomaly Ratio')
    locs, labels = plt.xticks()
    plt.xticks(ticks=locs, labels=xtickmark)
    plt.savefig(location + "_anomaly_ratio_boxplot.png", dpi=200, bbox_inches='tight', pad_inches=0)

    # Plotting Line plots for anomaly ratio
    plt.figure(2)
    final_df[list_columns].plot.line()
    plt.legend(xtickmark, loc='best')
    plt.grid()
    plt.xlabel('Weekly Metrics')
    plt.ylabel('Anomaly Ratio [No Unit]')
    plt.savefig(location + "_anomaly_ratio_lineplot.png", dpi=200, bbox_inches='tight', pad_inches=0)

    # Plotting box plot for alert ratio
    list_columns = [col for col in final_df.columns if 'alert_ratio' in col]
    plt.figure(3)
    final_df[list_columns].boxplot()
    plt.title('Alert Ratio')
    plt.ylabel('Alert Ratio')
    locs, labels = plt.xticks()
    plt.xticks(ticks=locs, labels=xtickmark)
    plt.savefig(location + "_flips_ratio_boxplot.png", dpi=200, bbox_inches='tight',
                pad_inches=0)
    
    # Plotting line plot for alert ratio
    plt.figure(4)
    final_df[list_columns].plot.line()
    plt.legend(xtickmark, loc='best')
    plt.grid()
    plt.xlabel('Weekly Metrics')
    plt.ylabel('Alert Ratio [No Unit]')
    plt.savefig(location + "_flips_ratio_lineplot.png", dpi=200, bbox_inches='tight', pad_inches=0)

    # Plotting for uptime ratio
    list_columns = [col for col in final_df.columns if 'uptime_ratio' in col]
    plt.figure(5)
    final_df[list_columns].boxplot()
    plt.title('Uptime Ratio')
    plt.ylabel('Uptime Ratio')
    locs, labels = plt.xticks()
    plt.xticks(ticks=locs, labels=xtickmark)
    plt.savefig(location + "_uptime_ratio_boxplot.png", dpi=200, bbox_inches='tight',
                pad_inches=0)
    
    # Plotting line plot for model uptime ratio
    plt.figure(6)
    final_df[list_columns].plot.line()
    plt.legend(xtickmark, loc='best')
    plt.grid()
    plt.xlabel('Weekly Metrics')
    plt.ylabel('Uptime Ratio [No Unit]')
    plt.savefig(location + "_uptime_ratio_lineplot.png", dpi=200, bbox_inches='tight', pad_inches=0)
    plt.show()
    return key_df


def generate_visualization_model_benchmarking(df, location):
    """
            Generate visualization for model benchmarking
            :return: nil
            """
    # Plotting bar graph for anomaly ratio
    list_columns = [col for col in df.columns if 'anomaly_ratio' in col]
    list_columns = list_columns[0]
    plt.figure(1)
    # plt.bar(df.index, df[list_columns], width=5.0)
    plt.plot(df.index, df[list_columns], '-o', color='orange')
    plt.ylabel('Anomaly Ratio')
    plt.xlabel('Weeks')
    plt.grid()
    plt.savefig(location + "_anomaly_ratio_benchmarking_lineplot.png", dpi=200, bbox_inches='tight', pad_inches=0)
    # ax2 = sns.distplot(df[list_columns], color="b")
    # ax2.set(xlabel='Anomaly Ratio')
    # ax2.savefig(location + "_anomaly_ratio_distn.png", dpi=200, bbox_inches='tight', pad_inches=0)
    
    # Plotting bar graph for flips ratio
    list_columns = [col for col in df.columns if 'alert_ratio' in col]
    plt.figure(2)
    # plt.bar(df.index, df[list_columns], width=5.0)
    plt.plot(df.index, df[list_columns], '-o', color='orange')
    plt.ylabel('Alert Ratio')
    plt.xlabel('Weeks')
    plt.grid()
    plt.savefig(location + "_alert_ratio_benchmarking_lineplot.png", dpi=200, bbox_inches='tight', pad_inches=0)
    # ax2 = sns.distplot(df[list_columns], color="b")
    # ax2.set(xlabel='Alert Ratio')
    # ax2.savefig(location + "_alert_ratio_distn.png", dpi=200, bbox_inches='tight', pad_inches=0)
    
    # Plotting bar graph for uptime ratio
    list_columns = [col for col in df.columns if 'uptime_ratio' in col]
    plt.figure(3)
    # plt.bar(df.index, df[list_columns], width=5.0)
    plt.plot(df.index, df[list_columns], '-o', color='orange')
    plt.ylabel('Uptime Ratio')
    plt.xlabel('Weeks')
    plt.grid()
    plt.savefig(location + "_uptime_ratio_benchmarking_lineplot.png", dpi=200, bbox_inches='tight', pad_inches=0)
    # ax2 = sns.distplot(df[list_columns], color="b")
    # ax2.set(xlabel='Uptime Ratio')
    # ax2.savefig(location + "_uptime_ratio_distn.png", dpi=200, bbox_inches='tight', pad_inches=0)
    plt.show()


################### MAIN Program Starts Here ######################################


# This is the folder that contains the json file for configuration
folder = FileUtils().return_src_folder_from_run_path() + '/files/config_templates'
# This is the name of the json configuration file used for model training
configuration_filename = "c3"
# Visualization True for storing the plots , False for not generating the plots
visualization = True

# Specifies the level of logging information printed to screen
logging_mode_is_simple = True
if logging_mode_is_simple:
    init_format = '%(asctime)s - %(message)s'
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format=init_format)
    logging.info("Workflow started")
else:
    init_format = "%(asctime)s | line %(lineno)4d | %(module)30s.%(funcName)s"
    logging.basicConfig(level=TRACE, stream=sys.stdout, format=init_format)

# Construct the TagData class. It contains all the methods needs to execute the workflow
tag_data = TagData(folder=folder, configuration_filename=configuration_filename)
# Acquires relevant information to determine which types of models will be used
tag_data.load_configurations_from_file()
#
# Load the testing output and training output files from the folder. If the many models were trained, load the training
# testing files recursively
files = []
folder_to_search = tag_data.get_model_configuration().get_results_output_folder_location()
folders = [f for f in glob.glob(folder_to_search + "**/", recursive=True)]
for folderscounter in folders:
    files_pred = [f for f in glob.glob(folderscounter + "/*tst_pred*", recursive=True)]
    files_trn = [f for f in glob.glob(folderscounter + "/*trn_pred*", recursive=True)]

# Check the number of .pred files. If the number of .pred files is > 1, it means we are doing model a vs modelv b .
# Else we are performing single model evaluation of metrics.
if len(files_pred) == 1:
    logging.info("Training & Testing KPI - Generation")
    df = load_file(files_pred[0])
    logging.info("Loaded testing results ")
    resultsdf_pred = compute_kpi(df)
    logging.info("Computed KPI  ")
    df = load_file(files_trn[0])
    logging.info("Loaded training results ")
    resultsdf_trn = compute_kpi(df)
    logging.info("Computed KPI  ")
    output_filepath = files_pred[0].replace('tst_pred', 'test_KPI')
    resultsdf_pred.to_csv(output_filepath)
    logging.info("Writing testing KPI to disc  ")
    output_filepath = files_trn[0].replace('trn_pred', 'trn_KPI')
    resultsdf_trn.to_csv(output_filepath)
    logging.info("Writing training KPI to disc  ")
    if visualization == True:
        logging.info("Generating plots ")
        generate_visualization_model_benchmarking(resultsdf_pred, tag_data.get_file_name_pattern_from_results())
    logging.info("Training & Testing KPI- Completed ")

# Compute the KPI on testing files recursively and output the results in the same output folder (Model A vs Model B)
if len(files_pred) > 1:
    logging.info("Model A vs Model B  KPI- Generation ")
    final_df = pd.DataFrame()
    for cnt in files_pred:
        model_name = cnt.split('tst_pred')[1][:-4]
        df = load_file(cnt)
        resultsdf_pred = compute_kpi(df)
        resultsdf_pred.columns = [s + model_name for s in resultsdf_pred.columns]
        final_df = df5 = pd.concat([final_df, resultsdf_pred], axis=1)
        logging.info("Computed KPI for Model:" + model_name)
    output_filepath = tag_data.get_file_name_pattern_from_results() + 'Model_Testing.csv'
    final_df.to_csv(output_filepath)
    logging.info("Writing KPI to disc  ")
    if visualization == True:
        logging.info("Generating plots ")
        key_df = generate_visualization_model_comparison(final_df, tag_data.get_file_name_pattern_from_results())
        key_df.to_csv(tag_data.get_file_name_pattern_from_results() + 'ModelNameMapping.csv')
        logging.info("Storing Mapping of Model Names ")
    logging.info("Model A vs Model B  KPI- Completed ")
