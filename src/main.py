import dataset_generator as source;
import classification as algorithm;
from bs4 import BeautifulSoup;
import requests;


def pull_homepage_data(homepage, data_sources):
    """
    Scrapes the data of the homepage and adds the link to the dataSources list.
    """
    open("dataset.txt", 'w').close()
    try:
        response = requests.get(homepage)
        web_content = response.content
    except:
        print("Something went wrong downloading the webpage")
        
    soup = BeautifulSoup(web_content, 'html.parser')
    for link in soup.find_all("a", class_="search-result search-result-article", href=True):
        data_sources.append("https://radiopaedia.org" + str(link['href']))


def pull_all_data(dataSources):
    for x in range(2, 153):
        webpage = "https://radiopaedia.org/encyclopaedia/all/all?lang=us&page="+str(x)
        try:
            response_new = requests.get(webpage)
            web_content_new = response_new.content
        except Exception as e:
            print("Something went wrong downloading the webpage in for loop")
            print(e)
        soup_new = BeautifulSoup(web_content_new, 'html.parser')
        for link in soup_new.find_all("a", class_="search-result search-result-article", href=True):
            dataSources.append("https://radiopaedia.org"+str(link['href']))
            print("Source added!")


if __name__ == '__main__':
    dataSources = []
    radiopedia_all_articles_home = "https://radiopaedia.org/encyclopaedia/all/all?lang=us"
    print("Re-create dataset? Y for yes")
    if str(input()).lower() == "y":
        pull_homepage_data(radiopedia_all_articles_home, dataSources)
        pull_all_data(dataSources)
        
        for link in dataSources:
            source.create_dataset(link)
    else:
        result, test = algorithm.predict("11-13 week antenatal (nuchal translucency) scan is considered a routine investigation advised for the fetal well being as well as for early screening in pregnancy (see antenatal screening). It includes multiple components and is highly dependent on the operator. Traditionally three factors are used to calculate the risk of trisomies:", -1)#run a sample model
        print(result)
        print(test)
