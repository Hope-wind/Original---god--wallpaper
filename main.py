import os,requests,re,threading
from parsel import Selector


headers = {
    "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"

}

if not os.path.exists("img"):
    os.mkdir("img")


def save():

    for page in range(1,50):
        base_url = "https://wall.alphacoders.com/by_sub_category.php?id=333944&name=%E5%8E%9F%E7%A5%9E+%E5%A3%81%E7%BA%B8&lang=Chinese={}".format(page)


        html_data = requests.get(url=base_url,headers=headers).text
        selector = Selector(html_data)

        result_list = selector.css("div.thumb-container > div.boxgrid > a::attr(href)").extract()

        for image_url in result_list:
            image_html_url = "https://wall.alphacoders.com/" + image_url
            
            html_data = requests.get(url=image_html_url,headers=headers).text
            selector = Selector(html_data)
            img_url = selector.css("div.center.img-container-desktop > a::attr(href)").extract_first()
            split_name = img_url.split(".")[-1]
            ID = selector. css("head > title").extract_first().split("|")[-1]
            ID = re.findall(r"\d+\.?\d*",ID)[0]
            file_name = ID + "." + split_name

            content = requests.get(url=img_url,headers=headers).content
            
            try:
                if not os.path.exists(file_name):
                    with open("img/" + file_name,mode="wb") as f:
                        f.write(content)
                        print("已下载:"+ID+split_name)

            except:
                 pass

def main():
    save()


if __name__ == "__main__":
    lock = threading.RLock()
    main()





