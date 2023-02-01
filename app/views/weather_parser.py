import requests
from bs4 import BeautifulSoup
from app import ua
from app.views.params import SkyParams


def search_weather(message=None, search_url=None):
    if search_url:
        response = requests.get(search_url, headers={"user-agent":ua.random})
        return show_weather(True, None, response.content, search_url)
    else:
        search_place = message.lower().split(", ")

        if len(search_place) == 3:
            city = search_place[0]
            obl = search_place[1].replace(" ", "-")
            reg = search_place[2].replace(" ", "-")
            url = f"https://ua.sinoptik.ua/україна/{obl}/{reg}"
            response = requests.get(url, headers={"user-agent":ua.random})

            if response.status_code == 200:
                return show_weather(False, city, response.content, url)
            else:
                return False

        elif len(search_place) == 2:
            city = search_place[0]
            obl = search_place[1].replace(" ", "-")
            url = f"https://ua.sinoptik.ua/україна/{obl}"
            response = requests.get(url, headers={"user-agent":ua.random})

            if response.status_code == 200:
                return show_weather(False, city, response.content, url)
            else:
                return False

        else:
            url = f"https://ua.sinoptik.ua/погода-{search_place[0]}"
            response = requests.get(url, headers={"user-agent":ua.random})

            if response.status_code == 200:
                return show_weather(True, None, response.content, url)
            else:
                return False


def show_weather(only_city, city, content, url):
    soup = BeautifulSoup(content, "html.parser")

    if only_city:
        return parser(content, url)

    all_cities = soup.find("div", class_="mapBotCol").find("div", class_="clearfix").find_all("a")

    for el in all_cities:
        if "-" in el.text:
            a_city = el.get("href").replace("погода-", "").split("/")[3].split(" ")

            if city == a_city[0]:
                response = requests.get("https:" + el.get("href"))
                return parser(response.content, "https:" + el.get("href"))
        else:
            a_city = el.get("href").split("/")[3].replace("-", " ").split(" ")

            try:
                if city == a_city[1] or city == a_city[1] + " " + a_city[2]:
                    response = requests.get("https:" + el.get("href"))
                    return parser(response.content, "https:" + el.get("href"))
            except:
                continue


def parser(content, url):
    sky_params = SkyParams().sky_params
    soup = BeautifulSoup(content, "html.parser")
    
    header = soup.find("div", class_="cityName")

    date = soup.find("div", class_="loaded").text
    week_day = f"{date.split()[0]} {date.split()[1]} {date.split()[2]}"
    min_max_temp = f"{date.split()[3]} {date.split()[4]} {date.split()[5]} {date.split()[6]}"

    city_name = header.find("h1").find("strong").text
    city_region = header.find("div", class_="currentRegion").text
    today_time = soup.find("p", class_="today-time").text
    today_temp = soup.find("p", class_="today-temp").text
    feels_like = soup.find("tr", class_="temperatureSens").find("td", class_="cur").text
    sky_class = soup.find("tr", class_="weatherIcoS").find("td", class_="cur").find("div", class_="weatherIco").get("class")[1]
    sky_title = soup.find("tr", class_="weatherIcoS").find("td", class_="cur").find("div", class_="weatherIco").get("title")
    sky_desc = sky_params.get(sky_class)
    print(sky_class)

    table = soup.find("tbody").findAll("tr", class_="")
    table_elements = [tr.find("td", class_="cur").text for tr in table]
    hudimity = table_elements[0] + " %" if table_elements[0] != "-" else "0%"
    fall_out = table_elements[1] + " %" if table_elements[1] != "-" else "0%"

    description = soup.find("div", class_="wDescription").find("div", class_="description").text
    temp = int(today_temp.split("\u00b0")[0])

    if temp <= 5:
        feel_emoji = 'Дуже прохолодно'
    if temp > 5 and temp <= 15:
        feel_emoji = 'Прохолодно'
    if temp > 15 and temp <= 27:
        feel_emoji = 'Тепло'
    if temp > 27:
        feel_emoji = 'Гаряче'

    return {
        "title": f"{city_name} {today_time.split()[1]} {today_time.split()[2]} {today_time.split()[3]}",
        "region": city_region,
        "weekday": week_day,
        "sky": f"{sky_class} {sky_title}" if sky_desc is None else sky_desc,
        "min_max": min_max_temp,
        "temp": today_temp,
        "feel_e": feel_emoji,
        "feel_t": feels_like,
        "hudimity": hudimity,
        "fall_out": fall_out,
        "desc": description.strip(),
        "url": url,
        "sky_params": sky_params
    }
