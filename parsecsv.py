import pandas as pd
import smtplib, ssl
import hashlib
import re
import os


def send_email(receiver_email, message):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "facebookscraper123@gmail.com"
    password = "<password>"
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
  
def exists_in_list(target, li):
    for element in li:
        if element == target:
            return True
    return False
  
def compare_csv(oldcsv, newcsv):
    newentries = ""
    for newrow in range(len(newcsv['Hash'])):
        if not exists_in_list(newcsv['Hash'][newrow], oldcsv['Hash']):
            newentries+=str(newcsv.loc[newrow, :])
            newentries+="\n"*2
    return(newentries)
    
def second_latest_output_filename(directory):
    files = os.listdir(directory)
    files.sort()
    return(directory+files[-2])
    
def latest_output_filename(directory):
    files = os.listdir(directory)
    files.sort()
    return(directory+files[-1])


if __name__ == "__main__":
    
    results_directory = "/home/owen/Workspace/python/marketplace-webscrape/results/"
    
    df = pd.read_csv(latest_output_filename(results_directory))
    
    di = df.to_dict()
    
    pd.set_option('display.max_colwidth', None)
    
    output = ""
    
    output+="\n\n\n\n-------------------------------------------------------------------NEW ENTRIES--------------------------------------------------------------------\n\n\n\n"
    output+=(compare_csv(pd.read_csv(second_latest_output_filename(results_directory)), pd.read_csv(latest_output_filename(results_directory))))
    
    output+="\n\n\n\n-------------------------------------------------------------------ALL ENTRIES--------------------------------------------------------------------\n\n\n\n"
    for row in range(len(di['Price'])):
        if int(di['Price'][row].strip("$").replace(",", "")) < 4000:
            if type(di['Mileage'][row]) != float and float(re.sub("[^0-9]", "", di['Mileage'][row])) < 190.0:
                output+=str(df.loc[row, :])
                output+="\n"*2
    
    
    send_email("okrussow@gmail.com", output.encode('utf-8'))
    

    print(output)


