import urllib.request
import ssl
from bs4 import BeautifulSoup


base_url = "https://usos-ects.uci.pb.edu.pl/"
try:
 _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
 pass
else:
     ssl._create_default_https_context = _create_unverified_https_context
    
pages = [0 ,1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

for page in pages:
    html = urllib.request.urlopen(f"{base_url}en/courses/list?page={page}")
    data = html.read()
    parser = BeautifulSoup(data, 'html.parser')
    all_list_a = parser.find_all("a")
    module_id_list = []
    for course in all_list_a:
     url = course.get("href")
     if('/en/courses/view?prz_kod=' in url):
        module_id_list.append(url)


    for id_url in module_id_list:
     course_data_html = urllib.request.urlopen(f"{base_url}{id_url}")
     data_courses = course_data_html.read()
     parser_courses = BeautifulSoup(data_courses, 'html.parser')
     module_name = parser_courses.find("h1").findAll(text= True, recursive=False)[1]
     module_id = parser_courses.find_all("span", class_="note")[1].getText()
     module_content = parser_courses.find("div", class_="opis iml").getText()
     credit_points = parser_courses.find("div", class_="item punkty_ects")
     department = parser_courses.find("div", class_="item jednostka").find("a").getText()
     credit_points_value = credit_points.getText()
     print(module_content)
     



html.close()

    # print(mystr)