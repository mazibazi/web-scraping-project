import requests
from bs4 import BeautifulSoup
import time

"""
text.replace(" ","")
text.split(" ")
"""

# search = input("Enter search term: ")
# params = {"q": search}
def findJobs():
    r = requests.get("https://es.indeed.com/jobs?q=data+scientist&l=Sevilla%2C+Sevilla+provincia")
    soup = BeautifulSoup(r.text, "html.parser")
    
    
    """
    text.replace(" ","")
    text.split(" ")
    """
    
    jobs = soup.find_all("div", class_="job_seen_beacon")
    for index, job in enumerate(jobs):
        try:
            firstJob = job.find("h2", class_="jobTitle jobTitle-color-purple").text
            compay = job.find("a", class_= "turnstileLink").text
            
            location = job.find("div",class_ = "companyLocation").text
            jobDiscript= job.find("li").text
            
            publishedDate = job.find("span", class_="date").text
            
            with open(f'posts/{index}.txt','w') as f:
               
                f.write(f'job possition: {firstJob.strip()} \n')
                f.write(f'company name: {compay.strip()}\n')
                f.write(f'location: {location.strip()}\n')
                f.write(f'Job discription: {jobDiscript}\n')
                f.write(f'date: {publishedDate.strip()}\n')
            print(f'file saved:{index}')
        except:
            print("not Reported")

if __name__ == '__main__':
    while True:
        findJobs()
        time_wait = 10
        print(f'Waiting {time_wait} minutes ....')
        time.sleep(10)












          