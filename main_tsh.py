import my_driver
from common_libraries import *

def psleep(sec):
    for i in range(sec):
        sleep(i+1)

class MainScraper():
    def __init__(self):
        self.start_url = "https://applications.fairtrading.nsw.gov.au/BDCRegister/RegistrationSearch.aspx"
        self.mainDriver = my_driver.Driver()
        self.subDriver = my_driver.Driver()

        self.result_dir = os.path.join(os.getcwd(), "Result")
        if not os.path.exists(self.result_dir):
            os.makedirs(self.result_dir)

        self.result_fname = os.path.join(self.result_dir, "Result.csv")
        self.create_result_file()

    def startScraping(self):
        self.mainDriver.driver.delete_all_cookies()
        self.mainDriver.get_url(self.start_url)

        # click first search button
        f_btn_search = self.mainDriver.find_by_xpath(
            '//*[@id="ctl00_ctl00_main_MainArea_SimpleSearchSection_SimpleSearchButton"]')
        self.mainDriver.click(f_btn_search)
        print("___ clicked first search button")

        # get all data count
        count_tag = self.mainDriver.find_by_xpath('//*[@id="ctl00_ctl00_main_MainArea_CardPaging"]')
        count_tag_text = count_tag.text
        print(count_tag_text)

        numbers = re.findall('\d+', count_tag_text)
        print(numbers)
        res_count = numbers[2]
        res_display_count = numbers[1]
        res_page_count = round(int(res_count) / int(res_display_count)) + 1

        print(res_count)
        print(res_display_count)
        print("___ " + str(res_page_count))

        for i in range(res_page_count):
            self.get_links(page=i + 1)

    def get_links(self, page):
        print(f"page: {page}")
        if page > 1:
            next_btn = self.mainDriver.find_by_xpath('//a[@id="ctl00_ctl00_main_MainArea_PageNextLink"]')
            self.mainDriver.click(next_btn)

            self.mainDriver.find_by_xpath(
                '//span[@id="ctl00_ctl00_main_MainArea_ResultDataList"]/span/div[@class="row"]//a')

        tree = html.fromstring(self.mainDriver.driver.page_source)
        rows = tree.xpath('//span[@id="ctl00_ctl00_main_MainArea_ResultDataList"]/span/div[@class="row"]')
        for j, row in enumerate(rows):
            id = re.findall('Registrationid=([0-9]+)', row.xpath('.//a/@href')[0])[0]
            detail_url = f'https://applications.fairtrading.nsw.gov.au/BDCRegister/PublicRegisterDetails.aspx?Registrationid={id}'
            self.get_details(detail_url)

    def get_details(self, detail_url):
        self.subDriver.get_url(detail_url)

        self.subDriver.find_by_xpath('//div[@id="ctl00_ctl00_main_MainArea_CertifierDetails_PanelBody"]')

        tree = html.fromstring(self.subDriver.driver.page_source)
        try:
            full_name = tree.xpath('//span[text()="Certifier Name"]/following-sibling::span/text()')[0].strip()
        except:
            full_name = ""
        try:
            reg_state = tree.xpath('//img[@id="ctl00_ctl00_main_MainArea_CertifierDetails_StatusImgSrouce"]/following-sibling::figcaption/text()')[0]
        except:
            reg_state = ""
        try:
            registration_number = tree.xpath('//span[text()="Registration Number"]/following-sibling::span/text()')[0].strip()
        except:
            registration_number = ""
        try:
            organisation_name = tree.xpath('//span[text()="Organisation Name"]/following-sibling::span/text()')[0].strip()
        except:
            organisation_name = ""
        try:
            business_address = ", ".join(tree.xpath('//span[text()="Business Address"]/following-sibling::span/text()'))
        except:
            business_address = ""
        try:
            postal_address = ", ".join(tree.xpath('//span[text()="Postal Address"]/following-sibling::span/text()'))
        except:
            postal_address = ""
        try:
            telephone_number = tree.xpath('//span[text()="Telephone Number"]/following-sibling::span/text()')[0]
        except:
            telephone_number = ""
        try:
            mobile_phone = tree.xpath('//span[text()="Mobile Number"]/following-sibling::span/text()')[0]
        except:
            mobile_phone = ""
        try:
            email_address = tree.xpath('//span[text()="Email Address"]/following-sibling::span/text()')[0]
        except:
            email_address = ""

        result_row = [
            full_name, reg_state, registration_number, organisation_name, business_address, postal_address, telephone_number,
            mobile_phone, email_address
        ]

        print(result_row)
        

    def create_result_file(self):
        self.result_fp = open(self.result_fname, 'w', encoding='utf-8', newline='')
        self.result_writer = csv.writer(self.result_fp)

    def insert_row(self, result_row):
        result_row = [str(elm) for elm in result_row]
        self.result_writer.writerow(result_row)
        self.result_fp.flush()


if __name__ == '__main__':
    scraper = MainScraper()
    scraper.startScraping()