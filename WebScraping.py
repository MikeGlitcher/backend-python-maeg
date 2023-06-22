from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

webdriver = webdriver.Chrome(ChromeDriverManager().install())

def details_view(url_):
    try:
        webdriver.get(url_)
        soup = BeautifulSoup(webdriver.page_source, "lxml")

        price_class = "a-offscreen"
        price = float(soup.find("span", class_=price_class).text.replace("$", "").replace(",", ""))

        description_id = "featurebullets_feature_div"
        description = soup.find("div", id=description_id).text

        rank_class = "a-icon-alt"
        rank = float(soup.find("span", class_=rank_class).text.replace(" de 5 estrellas", ""))

        return [price, description, rank]

    except Exception as error:
        return ["NONE", "NONE"]

def list_view():
    url = "https://www.amazon.com.mx/s?k=ryzen&__mk_es_MX=ÅMÅŽÕÑ&crid=12V6T72G4W4TL&sprefix=ryzen%2Caps%2C123&ref=nb_sb_noss_1"
    webdriver.get(url)

    soup = BeautifulSoup(webdriver.page_source, "lxml")

    a_class = "a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"
    a_tags = soup.find_all("a", class_=a_class)

    for a in a_tags:
        detail_link = "https://www.amazon.com.mx" + a.get("href")
        info = details_view(detail_link)
        title = a.text.replace("\n", "")

        try:
            if "gráficos" in info[1].lower() or "00g" in title.lower() or "3d" in title.lower():
                if info[2] > 4.5:
                    print("titulo: ", )
                    print("price: ", info[0], "\n")
                    print("price: ", info[1], "\n")
                else:
                    print("CALIFICACIONES NO APROBADAS ::: ", title)

            else:
                print("ARTICULO NO COMPATIBLE ::: ", title)

        except IndexError:
            pass
        # print("titulo: ", a.text.replace("\n", ""))
        # print("link: ", a.get("href"))
        # print("link2: ", detail_link)
        # print("\n")



list_view()
webdriver.close()
