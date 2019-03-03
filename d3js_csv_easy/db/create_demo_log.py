import random
from tqdm import tqdm
from operator import itemgetter
import datetime
import pandas as pd

num_samples = 30

hola =[]
with open('dummy_log.csv', 'w') as file_:
    file_.write('{},{},{},{},{},{}\n'.format('Date', 'NEW_ACCOUNT_CREATION', 'ACCOUNT_TERMINATED', 'EMAIL_SENT', 'INFORMATION_UPDATED','pdfs_added'))

    for i in range(num_samples):
        year = random.randint(2008, 2018)
        month = "{:02d}".format(random.randint(1, 12))
        day = "{:02d}".format(random.randint(1, 28))
        nac = random.randint(0, 5)
        at = random.randint(0, 3)
        es = random.randint(0, 100)
        iu = random.randint(0, 200)
        pdf = random.randint(0, 15)
        log_entry = "{}-{}-{},{},{},{},{},{}\n".format(year,month,day,nac,at,es,iu,pdf)
        hola.append(log_entry)
    for i in range(len(hola)):
        file_.write(hola[i])
    file_.close()

    df = pd.read_csv('dummy_log.csv')
    df.head()
    df['Date'] =pd.to_datetime(df.Date)
    df = df.sort_values(by = 'Date')
    df.to_csv("output.csv", index=False)


    # sorted(file_,key=lambda x:x[0])

