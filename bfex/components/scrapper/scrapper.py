from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings()
http = urllib3.PoolManager()


# this is where we would do json parsing to get the names?!?!?!

# concatenate names into url? here ?!?!!?

url = "https://www.ualberta.ca/science/about-us/contact-us/faculty-directory/william-allison"
response = http.request("GET", url)
soup = BeautifulSoup(response.data, "html.parser")
links = soup.find_all("a")
for link in links:
    try:
        if 'orcid' in link.attrs['href']:
            print("ORCID ID")
            print(link.attrs['href'])
        if "researcherid" in link.attrs['href']:
            print("ResearcherID")
            print(link.attrs['href'])
    except KeyError:
        # not all 'a' tags have the links we want
        pass
