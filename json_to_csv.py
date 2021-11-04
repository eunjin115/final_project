# -*- coding: utf-8 -*-
#https://github.com/epicarts/AI_challenge2018 코드 참고 
import os
import json
import glob
import csv
import os.path

os.chdir('./')  #작업하고 있는 디렉토리 변경
os.getcwd()
os.listdir('./') #현재 폴더의 파일들 목록

class FeatureExtraction:
    def __init__(self,json_file_path):
        json_data=open(json_file_path).read()
        data = json.loads(json_data) #json 형태로 변환
        self.data = data
        self.get_behavior_api_order = self.get_behavior_api_order(data)

    def get_behavior_api_order(self,data):
        result_list = []
        result_list.append(data['target']['file']['name'])
        try:
            for process in data['behavior']['processes']:
                for call in process['calls']:
                    result_list.append(call['api'])
            return result_list
        except Exception as e:
            pass
        return result_list
