import pyppeteer
import asyncio
import wget
import os

username = input("Lütfen fotoğraflarını indirmek istediğiniz kişinin kullanıcı adını giriniz: ")
url = f"https://vsco.co/{username}/gallery"

hrefs, srcs = list(), ()


async def main():
    browser = await pyppeteer.launch()
    page = await browser.newPage()

    await page.goto(url)

    button = await page.xpath('//*[@id="root"]/div/main/div/div[3]/section/div[2]/button')
    if button:
        await button[0].click()

    await page.xpath('//figure')

    length = len()

    while True:
        await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
        await asyncio.sleep(1)
        figures = await page.xpath('//figure')
        if len(figures) == length:
            break
        length = len(figures)

    for i, figure in enumerate(figures):
        a = await figure.xpath('.//a')

        href = await a[0].getProperty('href')
        href = await href.jsonValue()

        hrefs.append(href)

    for href in hrefs:
        await page.goto(href)

        image = await page.xpath('//img')

        src = await image[0].getProperty('src')
        src = await src.jsonValue()

        start = "https://image-"
        src = src[2:src.find('?')]
        splitted = src.split('/')
        src = start + splitted[1] + 'vsco.co/' + "/".join(splitted[2:])

        srcs.append(src)

        if not os.path.exists(username):
            os.mkdir(username)
        else:
            for file in os.listdir(username):
                os.remove(os.path.join(username, file))
            os.rmdir(username)
            os.mkdir(username)

        for i, sec in enumerate(srcs, 1):
            wget.download(src, username + os.sep + str(i) + ".jpg")

        await browser.close()

    if __name__ == '__main__':
        asyncio.get_event_loop().run_until_complete(main())
