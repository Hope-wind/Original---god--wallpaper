import asyncio,aiohttp,os,re
from parsel import Selector
from time import time


headers = {
    "User-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
    "Cookie":"visitor-id=2559253688967639000V10; data-t=13342522863494151200~~3; data-tl=setstatuscode~~1",
}


if not os.path.exists("img"):
    os.mkdir("img")


class Download(object):

    def mk_url(self,startnum,endnum):
        for num in range(startnum,endnum+1):
            base_url = "https://wall.alphacoders.com/by_sub_category.php?id=333944&name=%E5%8E%9F%E7%A5%9E+%E5%A3%81%E7%BA%B8&lang=Chinese={}".format(num)
            task_list = []
            task_list.append(base_url)
            yield task_list

    async def fetch_html(self,session,url):
        '''请求网页数据'''
        async with session.get(url) as response:
            return await response.text()

    async def fetch_img(self,session,url):
        '''请求图片数据'''
        async with session.get(url) as data:
            return await data.read()

    async def parse_data(self,session,html):
        '''处理数据'''
        selector = Selector(html)
        result_list = selector.css("div.thumb-container > div.boxgrid > a::attr(href)").extract()

        for image_url in result_list: 
            image_html_url = "https://wall.alphacoders.com/" + image_url

            html_data = await self.fetch_html(session,image_html_url)
            selector = Selector(html_data)

            img_url = selector.css("div.center.img-container-desktop > a::attr(href)").extract_first()
            split_name = img_url.split(".")[-1]
            ID = selector.css("head > title").extract_first().split("|")[-1]
            ID = re.findall(r"\d+\d*",ID)[0]
            file_name = ID + "." + split_name


            try:
                with open("img/" + file_name,mode="wb") as f:
                    content = await self.fetch_img(session,img_url)
                    f.write(content)
                    print("已写入:" + ID)
                       
            except Exception as e:
                print(e)


    async def start_save(self,url):
        async with aiohttp.ClientSession(headers=headers) as session:
            html = await self.fetch_html(session,url)
            await self.parse_data(session = session, html = html)

    async def download_pictures(self,startnum,endnum):
        for page in range(startnum,endnum+1):
            print("######正在下载第{}页数据######".format(page))
            url_list = self.mk_url(startnum,endnum)
            for url in url_list:
                base_url = url[0]
                await self.start_save(base_url)


'''实例化'''
if __name__ == '__main__':
    print("任务启动中...")
    download = Download()
    loop = asyncio.get_event_loop()

    tasks = [
        asyncio.ensure_future(download.download_pictures(2,20)),
        asyncio.ensure_future(download.download_pictures(21,50)),

    ]
    start_time = time()
    loop.run_until_complete(asyncio.gather(*tasks))
    end_time = time()
    run_time = end_time - start_time
    print(run_time)
