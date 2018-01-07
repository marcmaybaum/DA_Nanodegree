# Formatting Phone Numbers
cus = cus.fillna("")
cus["Phone"] = cus["Phone"].astype(str).str.strip()
cus["HomePhone"] = cus["HomePhone"].astype(str).str.strip()
cus["WorkPhone"] = cus["WorkPhone"].str.strip()
cus["CellPhone"] = cus["CellPhone"].str.strip()
cus["Phone"] = cus["Phone"].str.replace("-","")
cus["HomePhone"] = cus["HomePhone"].astype(str).str.replace("-","")
cus["WorkPhone"] = cus["WorkPhone"].str.replace("-","")
cus["CellPhone"] = cus["CellPhone"].str.replace("-","")
cus['Phone']=cus['Phone'].astype(str).apply(lambda x: '('+x[:3]+')'+x[3:6]+'-'+x[6:10])
cus['HomePhone']=cus['HomePhone'].astype(str).apply(lambda x: '('+x[:3]+')'+x[3:6]+'-'+x[6:10])
cus['WorkPhone']=cus['WorkPhone'].astype(str).apply(lambda x: '('+x[:3]+')'+x[3:6]+'-'+x[6:10])
cus['CellPhone']=cus['CellPhone'].astype(str).apply(lambda x: '('+x[:3]+')'+x[3:6]+'-'+x[6:10])



# Second formatting phone
callers['Caller Number']=callers['Caller Number'].astype(str)
callers['Caller Number']=callers['Caller Number'].str.replace(" ","")
callers['Caller Number']=callers['Caller Number'].str.replace(")","")
callers['Caller Number']=callers['Caller Number'].str.replace("(","")
callers['Caller Number']=callers['Caller Number'].str.replace("-","")
callers['Caller Number']=callers['Caller Number'].astype(str).apply(lambda x: '('+x[:3]+')'+x[3:6]+'-'+x[6:10])



