#! /usr/bin/env python

# Author: Lan Gerdej

from bs4 import BeautifulSoup
import pandas as pd
import re
import glob
import argparse
import os
    
def run(args):

    df = pd.DataFrame()

    sequences = glob.glob(str(args.input)+"/*")

    for sequence in sequences:
    
        seq = os.path.basename(os.path.normpath(sequence))

    #METABOLITES
    
        soup = BeautifulSoup(open(f'{sequence}/index.html'), 'html.parser')
        metabolites_soup = soup.find_all(True, class_=["linked-row odd", "linked-row even"])
        metabolites1 = []
    
        for i in metabolites_soup:
            i_row = re.findall(r'_blank">(.*)<', str(i))
            metabolites1.append(i_row[0])
        metabolites1 = metabolites1[0:len(metabolites1)//2]
    
        metabolites = []
        
        for m in metabolites1:
            if "," not in m:
                metabolites.append(m)
            elif m.count(",") == 1:
                x = re.findall(r'^(.*)</a>', str(m))[0]
                y = re.findall(r'_blank">(.*)', str(m))[0]
                metabolites.append(x+"/"+y)
            elif m.count(",") == 2:
                x = re.findall(r'^(.*?)</a>', str(m))[0]
                y = re.findall(r'_blank">(.*)', re.findall(r'_blank">(.*?)$', str(m))[0])[0]
                z = re.findall(r'_blank">(.*?)<', str(m))[0]
                metabolites.append(x+"/"+y+"/"+z)
            else: print("ERROR: More than 3 metabolites in a region")
    
    
    #REGIONS
    
        locations_soup = soup.find_all(True, class_="description-text")
        locations = []
    
        for i in locations_soup:
            l = re.findall(r'Location: (.*)', str(i))[0]
            locations.append(l)
    
    
    #MOST SIMILAR KNOWN CLUSTER
    
        similar1=[]
    
        for s in metabolites_soup:
            similar = re.findall(r'_blank">(.*)<', str(s))
            similar1.append(similar)
        similar1 = similar1[0:len(similar1)//2]
    
        similar = []
    
        for i in similar1:
            if len(i) == 1:
                similar.append("")
            else:
                similar.append(i[1][:-4])
    
    
    #PERCENTAGE OF SIMILARITY
    
        percentages=[]
    
        for p in metabolites_soup:
            percentage = re.findall(r'\d*%', str(p))   
            if percentage == []:
                percentages.append("/")
            else:
                percentages.append(percentage[0])
        percentages = percentages[0:len(percentages)//2]
    
    
    #JOINED MOST SIMILAR KNOWN CLUSTER & PERCENTAGE OF SIMILARITY
    
        met_percentages = []
    
        for m,p in list(zip(similar,percentages)):
            if m != "":
                met_percentages.append(m+" = "+p)
            else:
                met_percentages.append(p)
    
    
    #DATA FRAME
    
        row_names = [f"{seq} Metabolite", f"{seq} Region", f"{seq} Similar known cluster"]
        df1 = pd.DataFrame(data = [metabolites, locations, met_percentages], index = row_names)
        df = pd.concat([df, df1])
    

    #DATAFRAME TO CSV
        file_path = str(args.output) + "/" + str(args.name) + ".csv"
        df.to_csv(file_path)

def main():
	parser=argparse.ArgumentParser(description="Scrape metabolite, location and known cluster info from multiple antismash7 results.")
	parser.add_argument("-in",help="path to folder with antismash results" ,dest="input", type=str, required=True)
	parser.add_argument("-out",help="path to directory for csv results" ,dest="output", type=str, required=True)
	parser.add_argument("-name",help="name of csv file" ,dest="name", type=str, required=True)
	parser.set_defaults(func=run)
	args=parser.parse_args()
	args.func(args)

if __name__=="__main__":
	main()
