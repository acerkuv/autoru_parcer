import time
from os import  path
import json
 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as ES
# import undetected_chromedriver as uc
 
sd = path.join(path.dirname(__file__), 'cards')
 
driver = webdriver.Chrome('/path/to/chromedriver')  # Optional argument, if not specified will search path.
 
## Процедура проверки капчи: если есть, кликаем.
def check_capture():
    try:
        #<input aria-invalid="false" autocomplete="off" autofocus="" class="Textinput-Control" id="xuniq-0-1" name="rep" placeholder="Строчные или прописные буквы" value="">
        capture = driver.find_element(By.XPATH, '//input[@class="CheckboxCaptcha-Button"]')
        if capture:
            capture.click()
            time.sleep(3)
    except:
        pass
 
def manual_start():   
    check_capture()
    time.sleep(10)
      
# Парсим в список урл карточек авто
def get_urls_cars():
 
    all_proposals =driver.find_element(By.XPATH, '//a[@class="Link"][@target="_blank"]')
    all_urls = all_proposals.get_attribute('href')
    driver.get(all_urls)
 
    ## Все предложения
    car_cards_url = driver.find_elements(By.XPATH, "//a[@class='Link CardGroupListingItem__titleLink']")
    card_urld = []
    
    for url in car_cards_url:
        card_urld.append(url.get_attribute('href'))
    
    return card_urld       
 
# Выбираем данные с карты автмобиля
def car_card_parce(url, model):
    driver.get(url)
 
     # проверяем блокировку капчей
    check_capture()
 
    # name = driver.find_element(By.XPATH, '//h1[@class="CardNewHead__title"]').text
    # offers
    offer_price ='0'
    offer_str = driver.find_element(By.CSS_SELECTOR, 'span[class^="OfferPriceCaption__price"]').text
    
    if offer_str[:2]=='от':
        offer_price = ''.join(offer_str[2:-2].split())
    else:
        offer_price = ''.join(offer_str[:-2].split())
 
    try:
        price_str = driver.find_element(By.CSS_SELECTOR, 'div[class^="PriceNewOffer__origina"]').text
        price = ''.join(price_str[:-13].split())
    except:
        price = offer_price
 
    # price_text = driver.find_element(By.XPATH, "//span[@class='OfferPriceCaption__price']").text   
    # price_list = []
    # for spell in price_text.split(' '):
    #     try:
    #         d = int(spell)
    #         price_list.append(str(d))
    #     except:
    #         pass
    # price = "".join(price_list)
 
    complect = driver.find_element(By.XPATH, "//span[@class='Link CardInfoGroupedRow__cellValue CardInfoGroupedRow__cellValue_complectationName']").text
    dealership_el = driver.find_element(By.XPATH, "//a[@class='Link Link_color_black CardSellerNamePlace__name CardSellerNamePlace__name_type_commercial']")
    dealership = dealership_el.get_attribute('title')
    number = driver.find_element(By.XPATH, '//div[@class="CardHead__infoItem CardHead__id"]').text[2:]
    city = driver.find_element(By.XPATH, '//span[@class="GeoSelect__titleShrinker-wjCdV"]')
    discounts_name = driver.find_elements(By.XPATH, '//div[@class="CardDiscountList__itemName"]')
    discounts_value = driver.find_elements(By.XPATH, '//div[@class="CardDiscountList__itemValue"]')
    status = driver.find_element(By.CSS_SELECTOR,'div[class^="CardImageGallery__badges"]').text 
    
 
    discount_list = {}
    
    low_price = offer_price
    if len(discounts_name) > 0:
        for i in range(len(discounts_name)-1):
            discount_list.update({discounts_name[i].text: ''.join(discounts_value[i].text.split(' ')[1:-1])})
        max_discount = ''.join(discounts_value[-1:][0].text.split(' ')[:-1])
        # low_price = int(price) - int(max_discount)
    else:
        max_discount=0
    ## НДС ?
    try:
        driver.find_element(By.XPATH, '//div[@class="HoveredTooltip__trigger"]')
        vat = 1
    except :
        vat =0
 
    car_json = json.dumps({
        'number':number,
        'model_name': model, #name.split(",")[0],
        'year':'2022', #name.split('\n')[0].split(',')[1][1:],
        'equipment':complect,
        'status':status,
        'max_price':price,
        'min_price':offer_price,
        'max_discount':max_discount,
        'VAT':vat,
        'dealership_name':dealership,
        'dealership_city':city.get_attribute('title'),
        'disqount_dict': discount_list
 
    })
    return car_json
 
# Сохраняем данные автомбиля в JSON
def json_save(json_file):
    tj = json.loads(json_file)
    with open(path.join(sd, ''.join([tj['number'], ".json" ])), 'w') as f:
        json.dump(json_file, f, ensure_ascii=False, indent=4)
        f.close()
 
# Формируем сылку для выбора данных по условиям
def choise_model(model, city, brand, conditions):
    url = ''.join(["https://auto.ru/",city, "/cars/", brand,"/",model,"/", conditions,"/"])
    driver.get(url)
 
     # проверяем блокировку капчей
    check_capture()
 
    ## проверяем пагинатор TODO
    for car in get_urls_cars():
        json_save(car_card_parce(car, model))
 
# Main 
def parse_cars():
    models = ['cs75', 'cs35plus', 'cs55plus', 'uni_k', 'uni_v', 'cs95', 'cs85']
    # models = ['cs35plus']
 
    for model in models:
        choise_model(model, 'sankt-peterburg', 'changan', 'new')
 
driver.get('http://auto.ru')
manual_start()
parse_cars()
