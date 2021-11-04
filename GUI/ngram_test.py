# -*- coding: utf-8 -*-

import os
import time
import array
import dis
import operator
import csv
import sys

from itertools import chain

PWD = '/home/cuckoo/GUI/'

class NGRAM_features:
    def __init__(self, output):
        self.output = output
        self.gram = dict()
        self.imports = ""

    def gen_list_n_gram(self, num, asm_list):
        for i in range(0, len(asm_list), num):
            yield asm_list[i:i+num]

    def n_grams(self, num, asm_list, ex_mode):
        if ex_mode == 1:
            gram = self.gram
        elif ex_mode == 0:
            gram = dict()

        gen_list = self.gen_list_n_gram(num, asm_list)
        
        for lis in gen_list:
            lis = " ".join(map(str,lis))
            try:
                gram[lis] += 1
            except:
                gram[lis] = 1
         
        return gram


    def get_ngram_count(self, headers, grams):
        patterns = list()
        for pat in headers:
            try:
                patterns.append(grams[pat])
            except:
                patterns.append(0)
        return patterns


    def write_csv_header(self, headers):
        file_name=[]
        filepath = self.output
        headers = headers
        csv_file= open(filepath,"a")
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(headers)
        csv_file.close()
        
    
    def write_csv_data(self,data):
        filepath = self.output
        csv_file= open(filepath,"a")
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(data) #한 줄로 싹 쓰도록 
        csv_file.close()

    
def do_ngram(file_path):
    output_file = PWD + "ngram_test.csv"
    ef = NGRAM_features(output_file)
    headers = []
    api_seq = []
    i = 0
    with open(file_path, "r") as f:
        reader = csv.reader(f)
        for l in reader: #한 줄만 읽어올거라서
            headers.append(l)
            break
    del headers[0][-1] #마지막 class 지우기 
    ef.write_csv_header(headers[0]) #헤더만 가져오기 

    api_seq=[]

    with open("./api_order_test.csv", "r") as f:
        reader = csv.reader(f)
        for l in reader:
            api_seq.append(l)
        del api_seq[0][0] # 파일이름 삭제 
        grams = ef.n_grams(3, api_seq[0], 0)
        gram_count = ef.get_ngram_count(headers[0], grams) 
        # 얘는 테스트이기 때문에 0,1 을 판단하지 않음 (class) 적지 않음 
        all_data = []
        all_data.extend(gram_count)
        ef.write_csv_data(all_data)  
