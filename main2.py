import time
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService


def scrap_jobs():
    list_job_title = []
    list_company_name = []
    list_job_description = []
    list_experience_level = []
    list_location = []
    list_salary = []

    for page in range(1, 25):
        if page == 1:
            website_url = f'https://www.naukri.com/data-science-jobs?src=discovery_trendingWdgt_homepage_srch'
        else:
            website_url = f'https://www.naukri.com/data-science-jobs-{page}'

        # html_file = requests.get(website_url).text
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        driver.get(website_url)
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, 'html5lib')  # lxml is not working aptly for this website
        # print(soup.prettify())
        job_list = soup.find_all('article', class_="jobTuple")
        print(f"Scrapped from Naukari.com - {page}\n\n")
        for jobs in job_list:
            job_title = jobs.find('a', class_="title ellipsis").text
            list_job_title.append(job_title.strip())
            job_description = jobs.find('div', class_="ellipsis job-description").text
            list_job_description.append(job_description.strip())
            company_name = jobs.find('a', class_="subTitle ellipsis fleft").text
            list_company_name.append(company_name.strip())
            experience = jobs.find('span', class_="ellipsis fleft expwdth").text
            list_experience_level.append(experience.strip())
            salary = jobs.find('span', class_="ellipsis fleft").text
            list_salary.append(salary)
            location = jobs.find('span', class_="ellipsis fleft locWdth").text
            list_location.append(location.strip())

        dict_for_df = {'CompanyName': list_company_name, 'Location': list_location, 'Experience': list_experience_level,
                       'Job Title': list_job_title, 'Job Description': list_job_description,
                       'Salary': list_salary}
        df = pd.DataFrame(dict_for_df)
        df.to_csv('NaukariForDataScientist.csv')


def scrap_job_from_href_url():
    all_skill = ''
    edu_criteria = ''
    loc = ''
    list_job_title = []
    list_posted_date = []
    list_company_name = []
    list_education = []
    list_experience_level = []
    list_location = []
    list_salary = []
    list_application_url = []
    list_key_skills = []
    list_all_skills = []
    list_skills = []

    for page in range(1, 3):
        if page == 1:
            website_url = f'https://www.naukri.com/data-science-jobs?src=discovery_trendingWdgt_homepage_srch'
        else:
            website_url = f'https://www.naukri.com/data-science-jobs-{page}'

        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        driver.get(website_url)
        time.sleep(3)

        soup = BeautifulSoup(driver.page_source, 'html5lib')  # lxml is not working aptly for this website
        job_list = soup.find_all('article', class_="jobTuple")
        print(f"Scrapped from Naukari.com - {page}\n")

        for jobs in job_list:
            url_for_detail = jobs.find('a', class_="title ellipsis").get('href')
            application_url = url_for_detail
            list_application_url.append(application_url)

            driver.get(url_for_detail)
            time.sleep(3)
            try:
                soup2 = BeautifulSoup(driver.page_source, 'html5lib')
                job_title = soup2.find('h1', class_="jd-header-title").text

                company_name = soup2.find('div', class_="jd-header-comp-name").a.text

                experience = soup2.find('div', class_="exp").span.text

                salary = soup2.find('div', class_="salary").span.text

                posted_date = soup2.find('span', class_="stat").span.text

                qualification_level = soup2.find('div', class_="education")
                edu_level = qualification_level.find_all('div', class_="details")

                locations = soup2.find_all('span', class_="location")

                key_skills = soup2.find('a', class_="chip clickable").text

                # print(skills.text.replace('Key Skills', '').replace("Skills highlighted with ‘‘ are preferred
                # keyskills", '').strip())

            except:
                print(f'Could not collect data from url {application_url}')
                list_job_title.append('')
                list_posted_date.append('')
                list_company_name.append('')
                list_education.append('')
                list_experience_level.append('')
                list_location.append('')
                list_salary.append('')
                list_application_url.append('')
                list_key_skills.append('')
                list_all_skills.append('')

            else:
                for skills2 in jobs.find_all('li', class_="fleft dot"):
                    list_skills.append(skills2.text.strip())

                # Populating list to create dataframe
                list_job_title.append(job_title)
                list_company_name.append(company_name.strip())
                list_experience_level.append(experience.strip())
                list_salary.append(salary)
                list_posted_date.append(posted_date)

                edu_criteria = ''
                for education in edu_level:
                    edu_criteria = edu_criteria + ',' + education.text
                list_education.append(edu_criteria)

                loc = ''
                for location in locations:
                    loc = loc + location.text
                list_location.append(loc)

                list_key_skills.append(key_skills)

                # all_skill = []
                # for sk in list_skills:
                #     all_skill.append(sk)
                list_all_skills.append(list(set(list_skills)))

    dict_for_df = {'CompanyName': list_company_name, 'Location': list_location, 'Experience': list_experience_level,
                   'Job Title': list_job_title, 'Education': list_education, 'Salary': list_salary,
                   'Job Posted': list_posted_date, 'Key Skill': list_key_skills,
                   'Preferred Skills': list_all_skills, 'Application URL': list_application_url
                   }

    df = pd.DataFrame(dict_for_df)
    df.to_csv('DataScientistJobFromNaukari.csv')


if __name__ == '__main__':
    # scrap_jobs()
    scrap_job_from_href_url()
