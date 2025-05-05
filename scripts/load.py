import psycopg2
import logging

# create an instance of the logger
logger = logging.getLogger()

# logging set up
log_format = logging.Formatter('%(asctime)-15s %(levelname)-2s %(message)s')
sh = logging.StreamHandler()
sh.setFormatter(log_format)

# add the handler
logger.addHandler(sh)
logger.setLevel(logging.INFO)

conn = psycopg2.connect(database="",
                        user="",
                        password="",
                        host="",
                        port="")
print("Database Connected....")

cur = conn.cursor()
#open the csv file using python standard file I/O
#copy file into the table just created
with open('currency-v2.csv', 'r') as f:
    next(f)  # Başlık satırını atla
    try:
        cur.copy_from(f, 'exchange_rates', sep=',',
                     columns=('base_currency', 'target_currency', 'rate', 'last_updated'))
    except Exception as e:
        logger.error(e)
    #Commit Changes
    conn.commit()
    #Close connection
    conn.close()

f.close()