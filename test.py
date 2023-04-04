
from playwright.sync_api import sync_playwright
from auth import UserInfo


width, height = 1920, 1080


def login():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            args=["--window-size=1920,1080"], headless=False)
        context = browser.new_context()
        page1 = context.new_page()

        # 登录
        page1.goto(
            "http://ehall.hnuahe.edu.cn/publicapp/sys/bulletin/index.do#/bulletin")
        page1.locator("#username").click()
        page1.locator("#username").fill(UserInfo.username)
        page1.wait_for_timeout(1000)
        page1.locator("#password").click()
        page1.locator("#password").fill(UserInfo.password)
        page1.wait_for_timeout(9000)
        # 等待页面加载完毕
        page1.wait_for_load_state("networkidle")
        # 保存cookie
        storage_state = context.storage_state(path="login_data.json")
        # 关闭

    return storage_state


def index():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            args=["--window-size=1920,1080"], headless=True)
        context = browser.new_context(storage_state="login_data.json")
        page1 = context.new_page()
        page1.goto("http://ehall.hnuahe.edu.cn/publicapp/sys/bulletin/index.do")
        page1.wait_for_timeout(3000)
        cpage = page1.query_selector('.current').text_content()
        total_page = page1.query_selector(
            '//span[@class="totalPages"]/span').text_content()
        print("-"*24)
        print(f"当前在第{cpage}页, 一共{total_page}页。")
        print("-"*24)
        page1.wait_for_load_state("networkidle")
        title_all = page1.query_selector_all("//span[@class='intro-title']")
        yx_all = page1.query_selector_all(".list_dept")
        print("这页的内容是：\n")
        print("="*40)
        dict_all = dict(zip(yx_all, title_all))
        for k, v in dict_all.items():
            title = k.text_content()
            yx = v.text_content()
            print(f"{title}-{yx}")
        print("="*40, end="\n")


def search():
    global res
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(storage_state="login_data.json")
        page1 = context.new_page()
        page1.goto("http://ehall.hnuahe.edu.cn/publicapp/sys/bulletin/index.do")
        page1.wait_for_load_state("networkidle")
        search_title = input("请输入检索关键词（非必填）：")
        page1.locator("#titlesearch").click()
        page1.locator("#titlesearch").fill(f"{search_title}")
        department = input("请输入检索部门，以空格分隔（非必填）：")
        if department:
            page1.get_by_role("paragraph").filter(
                has_text="发布部门 党委办公室组织部宣传部统战部纪律检查委员会学工部离退休职工工作处团委校团委校工会机关党委人事处教务处招生办公室科学技术处保卫处后勤处实验室管理处国际交").get_by_role("button", name="全部").click()
            department_list = department.split(" ")
            for i in department_list:
                page1.locator("a").filter(has_text=f"{i}").click()
        column = input("请输入检索栏目，以空格分隔（非必填）：")
        if column:
            page1.get_by_role("button", name="全部").click()
            column_list = column.split(" ")
            for i in column_list:
                page1.locator("a").filter(has_text=f"{i}").click()

        start_time = input("请输入开始时间（非必填）（如：2023-1-1）：")
        if start_time:
            end_time = input("请输入结束时间（如：2023-1-1）：")
            page1.locator("#startimediv").get_by_role("textbox").click()
            page1.locator("#startimediv").get_by_role(
                "textbox").fill(start_time)
            page1.locator("#endtimediv").get_by_role("textbox").click()
            page1.locator("#endtimediv").get_by_role("textbox").fill(end_time)

        page1.locator("//p/button[1]").click()
        title_all = page1.query_selector_all("//span[@class='intro-title']")
        print("搜索结果是：")

        cpage = page1.query_selector('.current').text_content()
        total_page = page1.query_selector(
            '//span[@class="totalPages"]/span').text_content()
        print("-"*24)
        print(f"当前在第{cpage}页, 一共{total_page}页。")
        print("-"*24)

        print("=" * 40)
        for i in title_all:
            title = i.text_content()
            print(title)
        print("=" * 40)
        print("\n")
        res = int(input("请问是否打印：1、打印 2、不打印"))
        if res == 1:
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
                all_wid = page1.query_selector_all("//ul[@class='infoul']/li")

                for i in all_wid:
                    _wid = i.get_attribute("id")
                    wid = _wid.replace("_", "")
                    url = f"http://ehall.hnuahe.edu.cn/publicapp/sys/bulletin/bulletinDetail.do?WID={wid}#/bulletinDetail"
                    url_list.append(url)
                title_all_new = page1.query_selector_all(
                    "//span[@class='intro-title']")
                for i in title_all_new:
                    title_new = i.text_content()
                    title_list.append(title_new)

                page1.get_by_text("下一页").click()
                page1.wait_for_load_state('networkidle')
        if res == 1:
            return url_list, title_list


def get_url() -> list:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(storage_state="login_data.json")
        page1 = context.new_page()
        page1.goto("http://ehall.hnuahe.edu.cn/publicapp/sys/bulletin/index.do")
        page1.wait_for_load_state('networkidle')
        total_page = page1.query_selector(
            '//span[@class="totalPages"]/span').text_content()
        b = 1
        url_list = []
        title_list = []
        while b <= int(total_page):
            b += 1
            all_wid = page1.query_selector_all("//ul[@class='infoul']/li")
            for i in all_wid:
                _wid = i.get_attribute("id")
                wid = _wid.replace("_", "")
                url = f"http://ehall.hnuahe.edu.cn/publicapp/sys/bulletin/bulletinDetail.do?WID={wid}#/bulletinDetail"
                url_list.append(url)
            title_all = page1.query_selector_all(
                "//span[@class='intro-title']")
            for i in title_all:
                title = i.text_content()
                title_list.append(title)
            page1.get_by_text("下一页").click()
            page1.wait_for_load_state('networkidle')

    return url_list


def to_pdf(urls, titles):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(args=[
            f"--window-size={width},{height}",
        ],
            headless=True)
        context = browser.new_context(storage_state="login_data.json")
        page1 = context.new_page()

        for id, i in enumerate(urls):

            page1.goto(i)
            page1.wait_for_load_state('networkidle')
            page1.set_viewport_size({"width": width, "height": height})

            final_title = titles[id]

            page1.pdf(
                path=f"save/{final_title}.pdf", width="1920", height="1080")

        page1.close()
        context.close()


def main():
    print("首次使用请登录，默认登陆一次")
    # login(p)
    pass
    while True:
        print("="*10 + "Menu" + "="*10)
        print("请先登录！")
        print("功能：\n1、查看（主页）\n2、搜索\n3、登录\n4、打印全部\n5、退出")
        print("特别说明：打印全部会非常慢！")
        print("by - awsl1414")
        print("="*24)
        i = int(input("请输入:"))
        if i == 1:
            index()

        if i == 2:
            result = search()
            if res == 1:
                urls = result[0]
                titles = result[1]
                to_pdf(urls=urls, titles=titles)
            # print(urls)
        if i == 3:
            login()
        if i == 4:
            result2 = get_url()
            urls = result2[0]
            titles = result2[1]

            to_pdf(urls=urls, titles=titles)
        if i == 5:
            print("您输入了5，即将退出")
            break


if __name__ == '__main__':
    main()
