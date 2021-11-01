import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

"""
text.replace(" ","")
text.split(" ")
"""


# search = input("Enter search term: ")
# params = {"q": search}
def findJobs():
    url = "https://es.indeed.com/jobs?q=data+scientist&l=Sevilla%2C+Sevilla+provincia"
    # r = requests.get("https://es.indeed.com/jobs?q=data+scientist&l=Sevilla%2C+Sevilla+provincia")
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    """
    text.replace(" ","")
    text.split(" ")
    """

    jobs = soup.find_all("div", class_="job_seen_beacon")
    newDf = pd.DataFrame(columns=columnName)
    for index, job in enumerate(jobs):
        try:
            firstJob = jobs[2].find("h2", class_="jobTitle jobTitle-color-purple").text
        except:
            firstJob = "NA"
        try:   
            compay = job.find("a", class_="turnstileLink").text
        except:
            compay = "NA"
        try:   
            location = job.find("div", class_="companyLocation").text
        except:
            location = "NA"
        try:   
           jobDiscript = job.find("li").text
        except:
            jobDiscript = "NA"
        try:   
            publishedDate = job.find("span", class_="date").text
        except:
            publishedDate = "NA"
            
        newList = [firstJob, compay, location, jobDiscript, publishedDate]
        newDf.loc[len(newDf)] = newList
        records.append((firstJob, compay, location, jobDiscript, publishedDate))

    return newDf


if __name__ == '__main__':
    
    columnName = ["firstJob", "company", "location", "jobDescription", "publishedDate"]
    df = pd.DataFrame(columns=columnName)
    timeCounter = 0
    while True:
        
        records = []
        findJobs()
        df = df.append(findJobs(), ignore_index=True)
        df.drop_duplicates(keep="last", inplace=True)
        time_wait = 5
        timeCounter += 1
        print(f'Waiting {time_wait} minutes ....')
        if timeCounter <= 5:
            time.sleep(5)
        else: 
            df.to_csv("jobDataScientist.csv")
            break







