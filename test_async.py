
import asyncio
from playwright.async_api import async_playwright
from auth import UserInfo


width, height = 1920, 1080


async def login():
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(
            args=["--window-size=1920,1080"], headless=False)
        context = await browser.new_context()
        page1 = await context.new_page()

        # 登录
        await page1.goto(
            "http://ehall.hnuahe.edu.cn/publicapp/sys/bulletin/index.do#/bulletin")
        await page1.locator("#username").click()
        await page1.locator("#username").fill(UserInfo.username)
        await page1.wait_for_timeout(1000)
        await page1.locator("#password").click()
        await page1.locator("#password").fill(UserInfo.password)
        await page1.wait_for_timeout(9000)
        # 等待页面加载完毕
        await page1.wait_for_load_state("networkidle")
        # 保存cookie
        storage_state = await context.storage_state(path="login_data.json")
        # 关闭

    return storage_state


async def index():
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(
            args=["--window-size=1920,1080"], headless=True)
        context = await browser.new_context(storage_state="login_data.json")
        page1 = await context.new_page()
        await page1.goto("http://ehall.hnuahe.edu.cn/publicapp/sys/bulletin/index.do")
        await page1.wait_for_timeout(3000)
        cpage2 = await page1.query_selector('.current')
        cpage = await cpage2.text_content()
        total_page2 = await page1.query_selector(
            '//span[@class="totalPages"]/span')
        total_page = await total_page2.text_content()
        # await page1.text_content()
        print("-"*24)
        print(f"当前在第{cpage}页, 一共{total_page}页。")
        print("-"*24)
        await page1.wait_for_load_state("networkidle")
        title_all = await page1.query_selector_all("//span[@class='intro-title']")
        yx_all = await page1.query_selector_all(".list_dept")
        print("这页的内容是：\n")
        print("="*40)
        dict_all = dict(zip(yx_all, title_all))
        for k, v in dict_all.items():
            title = await k.text_content()
            yx = await v.text_content()
            print(f"{title}-{yx}")
        print("="*40, end="\n")


async def search():
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        context = await browser.new_context(storage_state="login_data.json")
        page1 = await context.new_page()
        await page1.goto("http://ehall.hnuahe.edu.cn/publicapp/sys/bulletin/index.do")
        await page1.wait_for_load_state("networkidle")
        search_title = input("请输入检索关键词（非必填）：")
        await page1.locator("#titlesearch").click()
        await page1.locator("#titlesearch").fill(f"{search_title}")
        department = input("请输入检索部门，以空格分隔（非必填）：")
        if department:
            await page1.get_by_role("paragraph").filter(
                has_text="发布部门 党委办公室组织部宣传部统战部纪律检查委员会学工部离退休职工工作处团委校团委校工会机关党委人事处教务处招生办公室科学技术处保卫处后勤处实验室管理处国际交").get_by_role("button", name="全部").click()
            department_list = await department.split(" ")
            for i in department_list:
                await page1.locator("a").filter(has_text=f"{i}").click()
        column = input("请输入检索栏目，以空格分隔（非必填）：")
        if column:
            await page1.get_by_role("button", name="全部").click()
            column_list = await column.split(" ")
            for i in column_list:
                await page1.locator("a").filter(has_text=f"{i}").click()

        start_time = input("请输入开始时间（非必填）（如：2023-1-1）：")
        if start_time:
            end_time = input("请输入结束时间（如：2023-1-1）：")
            await page1.locator("#startimediv").get_by_role("textbox").click()
            await page1.locator("#startimediv").get_by_role("textbox").fill(start_time)
            await page1.locator("#endtimediv").get_by_role("textbox").click()
            await page1.locator("#endtimediv").get_by_role("textbox").fill(end_time)

        await page1.locator("//p/button[1]").click()
        title_all = await page1.query_selector_all("//span[@class='intro-title']")
        print("搜索结果是：")

        cpage2 = await page1.query_selector('.current')
        cpage = await cpage2.text_content()
        total_page2 = await page1.query_selector(
            '//span[@class="totalPages"]/span')
        total_page = await total_page2.text_content()
        print("-"*24)
        print(f"当前在第{cpage}页, 一共{total_page}页。")
        print("-"*24)

        print("=" * 40)
        for i in title_all:
            title = await i.text_content()
            print(title)
        print("=" * 40)
        print("\n")

        select1 = int(input("请选择：1、打印全部，2、打印你想打印的页数"))
        if select1 == 1:
            a = int(total_page)
        if select1 == 2:
            a = int(input("请输入你想打印的页数："))
        b = 1
        url_list = []
        title_list = []
        while b <= a:
            b += 1
            all_wid = await page1.query_selector_all("//ul[@class='infoul']/li")

            for i in all_wid:
                _wid = await i.get_attribute("id")
                wid = _wid.replace("_", "")
                url = f"http://ehall.hnuahe.edu.cn/publicapp/sys/bulletin/bulletinDetail.do?WID={wid}#/bulletinDetail"
                url_list.append(url)
            title_all_new = await page1.query_selector_all(
                "//span[@class='intro-title']")
            for i in title_all_new:
                title_new = await i.text_content()
                title_list.append(title_new)

            await page1.get_by_text("下一页").click()
            await page1.wait_for_load_state('networkidle')

    return url_list, title_list


async def get_url() -> list:
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context(storage_state="login_data.json")
        page1 = await context.new_page()
        await page1.goto("http://ehall.hnuahe.edu.cn/publicapp/sys/bulletin/index.do")
        await page1.wait_for_load_state('networkidle')
        total_page2 = await page1.query_selector(
            '//span[@class="totalPages"]/span')
        total_page = await total_page2.text_content()
        # print(total_page)
        b = 1
        url_list = []
        title_list = []
        # while b <= int(total_page):
        while b <= int(total_page):
            b += 1
            all_wid = await page1.query_selector_all("//ul[@class='infoul']/li")
            for i in all_wid:
                _wid = await i.get_attribute("id")
                wid = _wid.replace("_", "")
                url = f"http://ehall.hnuahe.edu.cn/publicapp/sys/bulletin/bulletinDetail.do?WID={wid}#/bulletinDetail"
                url_list.append(url)
            title_all = await page1.query_selector_all(
                "//span[@class='intro-title']")
            for i in title_all:
                title = await i.text_content()
                title_list.append(title)
            await page1.get_by_text("下一页").click()
            await page1.wait_for_load_state('networkidle')
        print(url_list)

    return url_list, title_list


async def to_pdf(urls, titles):
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(args=[
            f"--window-size={width},{height}",
        ],
            headless=False)
        context = await browser.new_context(storage_state="login_data.json")
        page1 = await context.new_page()

        for id, i in enumerate(urls):

            await page1.goto(f"{i}")
            await page1.wait_for_load_state('networkidle')
            await page1.set_viewport_size({"width": width, "height": height})

            final_title = titles[id]

            await page1.pdf(
                path=f"spider/save/{final_title}.pdf", width="1920", height="1080")


print("首次使用请登录，默认登陆一次")
# login(p)

while True:
    print("="*10 + "Menu" + "="*10)

    print("功能：\n1、查看（主页）\n2、搜索\n3、登录\n4、打印全部\n5、退出")
    print("特别说明：打印全部会非常慢！")
    print("by - awsl1414")
    print("="*24)
    i = int(input("请输入:"))
    if i == 1:
        asyncio.run(index())

    if i == 2:
        result = asyncio.run(search())
        urls = result[0]
        titles = result[1]

        asyncio.run(to_pdf(urls=urls, titles=titles))
        # print(urls)
    if i == 3:
        asyncio.run(login())
    if i == 4:
        result = asyncio.run(get_url())
        urls = result[0]
        titles = result[1]

        asyncio.run(to_pdf(urls=urls, titles=titles))
    if i == 5:
        print("您输入了5，即将退出")
        break
