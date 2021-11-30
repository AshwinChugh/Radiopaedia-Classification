from bs4 import BeautifulSoup
import requests


def create_dataset(website):
    webpage = str(website)
    try:
        response = requests.get(webpage)
        web_content = response.content
    except:
        print("Something went wrong downloading the webpage")

    soup = BeautifulSoup(web_content, 'html.parser')
    with open('./src/dataset.txt', 'a+') as f:
        try:
            system = soup.find("div", class_="meta-item meta-item-systems").text
            generic_list = []
            for char in list(system):
                if char != ',' and char != ":":
                    generic_list.append(char)
            system = ""
            system = system.join(generic_list)
            generic_list = system.split()
            generic_list.remove('System')
            for i in range(len(generic_list)):
                generic_list[i] = "__label__"+generic_list[i]+" "
            f.write("".join(generic_list))
            content = soup.find("div", class_="body user-generated-content").text
            f.write(content.replace("\n", " ")+"\n")
        except:
            print("Error for a webpage")

    return_soup = BeautifulSoup(open('./src/webpage.html'), 'html.parser')
    return return_soup.prettify()
