from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd


def parse_timesjobs() -> None:
    for page in range(0, 11):
        if page == 0:
            website_link = f'https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from' \
                           f'=submit&txtKeywords=Data+Scientist&txtLocation= '
        else:
            website_link = f'https://www.timesjobs.com/candidate/job-search.html?from=submit&actualTxtKeywords=Data' \
                           f'%20Scientist&searchBy=0&rdoOperator=OR&searchType=personalizedSearch&luceneResultSize=25' \
                           f'&postWeek=60&txtKeywords=data%20scientist&pDate=I&sequence=2&startPage={page} '

        html_file = requests.get(website_link).text
        soup = BeautifulSoup(html_file, 'lxml')
        job_list = soup.find_all('li', class_="clearfix job-bx wht-shd-bx")
        print(f"Scrapped from Times Jobs - \n\n")
        for job in job_list:
            post_date = job.find('span', class_="sim-posted").span.text
            print(f"Job Post Date: {post_date}")
            company_name = job.find('h3', class_="joblist-comp-name").text
            print(f"Company Name - {company_name.strip()}")
            job_description = job.find('ul', class_="list-job-dtl clearfix").li.text.replace('Job Description:',
                                                                                             '').replace('  ', ' ')
            print(f"Job Description: {job_description.strip()}")
            experience_level = job.find('ul', class_="top-jd-dtl").li.text.replace('card_travel', '')
            print(f"Experience: {experience_level.strip()}")
            location = job.find('span').text.replace('  ', ' ')
            print(f"Location: {location.strip()}")
            key_skills = job.find('span', class_="srp-skills").text.replace('  ', ' ').replace(' ,', ',')
            print(f"Key Skills: {key_skills.strip()} \n")


def populate_csv_with_timesjobs() -> None:
    list_post_date = []
    list_company_name = []
    list_job_description = []
    list_experience_level = []
    list_location = []
    list_key_skills = []

    for page in range(0, 11):
        if page == 0:
            website_link = f'https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from' \
                           f'=submit&txtKeywords=Data+Scientist&txtLocation= '
        else:
            website_link = f'https://www.timesjobs.com/candidate/job-search.html?from=submit&actualTxtKeywords=Data' \
                           f'%20Scientist&searchBy=0&rdoOperator=OR&searchType=personalizedSearch&luceneResultSize=25' \
                           f'&postWeek=60&txtKeywords=data%20scientist&pDate=I&sequence=2&startPage={page} '

        html_file = requests.get(website_link).text
        soup = BeautifulSoup(html_file, 'lxml')
        job_list = soup.find_all('li', class_="clearfix job-bx wht-shd-bx")
        print(f"Scrapped from Times Jobs - {page}")
        for job in job_list:
            post_date = job.find('span', class_="sim-posted").span.text
            list_post_date.append(post_date)
            company_name = job.find('h3', class_="joblist-comp-name").text
            list_company_name.append(company_name.strip())
            job_description = job.find('ul', class_="list-job-dtl clearfix").li.text.replace('Job Description:',
                                                                                             '').replace('  ', ' ')
            list_job_description.append(job_description.strip())
            experience_level = job.find('ul', class_="top-jd-dtl").li.text.replace('card_travel', '')
            list_experience_level.append(experience_level)
            location = job.find('span').text.replace('  ', ' ')
            list_location.append(location)
            key_skills = job.find('span', class_="srp-skills").text.replace('  ', ' ').replace(' ,', ',')
            list_key_skills.append(key_skills.strip())

    dict_for_df = {'CompanyName': list_company_name, 'Location': list_location, 'Experience': list_experience_level, 'Skills': list_key_skills, 'Job Description': list_job_description, 'Posted Date': list_post_date}
    df = pd.DataFrame(dict_for_df)
    df.to_csv('TimesJobsForDataScientist.csv')
    print(list_job_description)
    print(list_company_name)
    print(list_key_skills)


if __name__ == '__main__':
    # parse_timesjobs()
    populate_csv_with_timesjobs()