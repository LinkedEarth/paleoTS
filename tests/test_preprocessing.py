#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 18:41:25 2023

@author: deborahkhider

Tests for paleoTS PreProcessing functions

Naming rules:
1. class: Test{filename}{Class}{method} with appropriate camel case
2. function: test_{method}_t{test_id}
Notes on how to test:
0. Make sure [pytest](https://docs.pytest.org) has been installed: `pip install pytest`
1. execute `pytest {directory_path}` in terminal to perform all tests in all testing files inside the specified directory
2. execute `pytest {file_path}` in terminal to perform all tests in the specified file
3. execute `pytest {file_path}::{TestClass}::{test_method}` in terminal to perform a specific test class/method inside the specified file
4. after `pip install pytest-xdist`, one may execute "pytest -n 4" to test in parallel with number of workers specified by `-n`
5. for more details, see https://docs.pytest.org/en/stable/usage.html
"""


import pytest
import os
import pyleoclim as pyleo
import lipd as lpd

def loadSeries(filename, TSID):
    
    def filter_TSid(D,TSID):
        try:
            ts_list=lpd.extractTs(D,mode='paleo')
            found=0
            for item in ts_list:
                if item['paleoData_TSid']==TSID:
                    ts_lipd=pyleo.LipdSeries(item)
                    # get rid of the extra stuff and make it a regular Series
                    ts_dict = pyleo.utils.jsonutils.PyleoObj_to_dict(ts_lipd.copy())
                    del ts_dict['plot_default']
                    del ts_dict['lipd_ts']
                    ts=pyleo.Series(**ts_dict)
                    found=1
                elif found==1:
                    break 
            if found == 0:
                raise ValueError('No PaleoData variable corresponds to this TSid')
        except:
            ts_list=lpd.extractTs(D,mode='chron')
            found=0
            for item in ts_list:
                if item['chronData_TSid']==TSID:
                    ts_lipd=pyleo.LipdSeries(item)
                    # get rid of the extra stuff and make it a regular Series
                    ts_dict = pyleo.utils.jsonutils.PyleoObj_to_dict(ts_lipd.copy())
                    del ts_dict['plot_default']
                    del ts_dict['lipd_ts']
                    ts=pyleo.Series(**ts_dict)
                    found=1
                elif found==1:
                    break 
            if found == 0:
                raise ValueError('No ChronData variable corresponds to this TSid')
            
        return ts, ts_lipd
    
    
    if filename.split(".")[-1]=='json':
        ts = pyleo.utils.jsonutils.json_to_PyleoObj(filename,'Series')
    else:
        cwd = os.getcwd()
        filename = os.path.abspath(filename)
        D=lpd.readLipd(filename)
        ts,ts_lipd = filter_TSid(D,TSID)
        os.chdir(cwd)
        
    return ts

class TestStandardize():
    
    @pytest.mark.parametrize('filename',['./data/test_perfect_signal.json', './data/MD98_2181.Stott.2007.lpd'])
    def test_std_t0(self,filename):
        TSID = 'T2L_MD98_2181_d18o_ruber_SST_from_d18o_ruber'
        ts = loadSeries(filename, TSID)
        ts_std = ts.standardize()
        pyleo.utils.jsonutils.PyleoObj_to_json(ts_std.copy(),'./outputs/std.json') #write to JSON
        

class TestRemoveOutliers():
    
    @pytest.mark.parametrize('filename',['./data/test_perfect_signal.json', './data/MD98_2181.Stott.2007.lpd'])
    def test_outliers_t0(self, filename):
        ''' Test the DBSCAN method with defaults
        

        Returns
        -------
        None.

        '''
        TSID = 'T2L_MD98_2181_d18o_ruber_SST_from_d18o_ruber'
        ts = loadSeries(filename, TSID)
        ts_outliers = ts.outliers(method = 'DBSCAN', remove=True, 
                          settings = {'nbr_clusters':None,'eps':None,'min_samples':None,'n_neighbors':None,'metric':'euclidean'},
                          savefigclusters_settings={'path':'./outputs/outputclusters.png', 'format':'png'},
                          savefigoutliers_settings={'path':'./outputs/outputoutliers.png', 'format':'png'}, keep_log=True)
        
        for item in ts_outliers.log:
            if 'outliers' in item.values():
                res = item['results']
                res.to_csv('./outputs/clustersummary.csv')
        
        pyleo.utils.jsonutils.PyleoObj_to_json(ts_outliers.copy(), 'ts_outliers.json') #write to JSON
        
    @pytest.mark.parametrize('filename',['./data/test_perfect_signal.json', './data/MD98_2181.Stott.2007.lpd'])
    def test_outliers_t1(self, filename):
        ''' Test the kmeans method with defaults
        

        Returns
        -------
        None.

        '''
        TSID = 'T2L_MD98_2181_d18o_ruber_SST_from_d18o_ruber'
        ts = loadSeries(filename, TSID)
        ts_outliers = ts.outliers(method = 'kmeans', remove=True, 
                          settings = {'nbr_clusters':None,'max_cluster':10,'threshold':3},
                          savefigclusters_settings={'path':'./outputs/outputclusters.png', 'format':'png'},
                          savefigoutliers_settings={'path':'./outputs/outputoutliers.png', 'format':'png'}, keep_log=True)
        
        for item in ts_outliers.log:
            if 'outliers' in item.values():
                res = item['results']
                res.to_csv('./outputs/clustersummary.csv')
        
        #remove the log for saving purposes
        ts_outliers.log=None        
        pyleo.utils.jsonutils.PyleoObj_to_json(ts_outliers.copy(), './outputs/ts_outliers.json') #write to JSON
         
        
        

   
        

    
    
