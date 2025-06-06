__author__ = "Heidi Suurkaulio"
__dependencies__ = ["sys", "pandas", "csv", "re"]
__version__ = "1.0"
__date__ = "01-05-2025"
__project__ = "https://github.com/Heidi-Suurkaulio/mastersthesis"
__maintainer__ = "Heidi Suurkaulio"
__email__ = "heidisuur@gmail.com"

import sys
import pandas as pd
from csv import writer
import re

# testing that the filename is present
if len(sys.argv) < 2:
     print("Error: file name must be given in format .csv")
     sys.exit()

# reading the data
dataset_name = sys.argv[1]
dataset = pd.read_csv(dataset_name ,sep=";", index_col="Id")
dataset["Connections"] = None

# make sure the years of appointment are numeric type
dataset.update(pd.to_numeric(dataset['Appointed']))

# if start and end year or interval is given, limits the dataset on given parameters
if len(sys.argv) == 4:
     match sys.argv[2]:
          case "prior":
               # the year of appointment is the same or smaller than given
               end_year = int(sys.argv[3])
               dataset = dataset.loc[dataset['Appointed'] <= end_year]
          case "post":
               # the year of appointment is the same or greater than given
               start_year = int(sys.argv[3])
               dataset = dataset.loc[dataset['Appointed'] >= start_year]
          case default:
               # the year of appointment is greater than the first year given
               # the year of appointment is smaller than the last year given
               start_year = int(sys.argv[2])
               dataset = dataset.loc[dataset['Appointed'] >= start_year]
               end_year = int(sys.argv[3])
               dataset = dataset.loc[dataset['Appointed'] <= end_year]       

# save the connections to the dataset
for index, ent in dataset.iterrows():
    st = ent.Family
    if isinstance(st, str):
        cons = re.findall(r'\b\d+\b', st)
        cons = list(map(int, cons)) # convert to integer
        dataset.at[index, "Connections"] = cons

# find current indexes
current_ids = dataset.index

# make a list of connections
printable = []
printable.append(['Source', 'Target', 'Type', 'Id', 'Weight'])
i = 0
for index, entr in dataset.iterrows():
    if isinstance(entr.Connections, list) and len(entr.Connections) > 0:
        for o in entr.Connections:
            if o in current_ids: # check if the id mentioned in connection is in dataset
                 printable.append([index, o, "Undirected", i ,"1.0"])
                 i = i + 1

# print all
dataset.to_csv("councillors.csv", columns=["Name"], sep=";", header=["Label"])

with open("connections.csv", "w", newline='') as csvfile:
        wr = writer(csvfile)
        wr.writerows(printable)
