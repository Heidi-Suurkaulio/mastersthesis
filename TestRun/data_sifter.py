import pandas as pd
from csv import writer
import re

dataset = pd.read_csv("Concilors_of_the_Realm.csv" ,sep=";")

#TODO consider using numbers of columns later on?
nw_data = dataset[["Name", "Id", "Family"]].copy()
nw_data["Connections"] = None

# save the connections to the dataset
for index, ent in nw_data.iterrows():
    st = ent.Family
    if isinstance(st, str):
        cons = re.findall(r'\b\d+\b', st)
        nw_data.at[index, "Connections"] = cons

printable = []
printable.append(['Source', 'Target', 'Type', 'Id', 'Weight'])
i = 0
for index, entr in nw_data.iterrows():
    if isinstance(entr.Connections, list) and len(entr.Connections) > 0:
        for o in entr.Connections:
            printable.append([entr.Id, o, "Undirected", i ,"1.0"])
            i = i + 1

nw_data.to_csv("concilors.csv", columns=["Id", "Name"], sep=";", index=False)

with open("connections.csv", "w", newline='') as csvfile:
        wr = writer(csvfile)
        wr.writerows(printable)
#print(printable)
