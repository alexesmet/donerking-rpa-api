#!/usr/bin/python
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep


driver = Chrome()

def yes_delivery():
    sleep(2)
    try:
        btn = driver.find_element_by_css_selector(".fpsmart__close")
        btn.click()
    except:
        print("Could not click fpsmart__close")
    try:
        btn = driver.find_element_by_css_selector("#delivery_ok button")
        if not btn: return
        btn.click()
        btn = driver.find_element_by_css_selector("form#delivery_form button")
        btn.click()
        sleep(2)
    except:
        print("Looks like no delivery acceptance required...")


def add_ingrid(name, order):
    for mayo in [td for td in driver.find_elements_by_css_selector("tr.souce_row") if td.find_element_by_class_name("souce_row__title").text == name]:
        mayo.find_element_by_css_selector("label.check-container input[type=checkbox]").click()
        mayo.find_element_by_css_selector("select.additionsize option:nth-child("+str(order)+")").click()


def add_to_cart(address, qty=1, ingrids=[], lavash=None, comment=None):
    driver.get(address)
    btn = driver.find_element_by_css_selector("button.add-to-cart")
    btn.click()
    yes_delivery()
    if lavash:
        [label.click() for label in driver.find_elements_by_css_selector(".radio-container.spec") if label.text.startswith(lavash)]
        sleep(0.5)
    for each in ingrids:
        add_ingrid(each[0], each[1])
        sleep(0.5)
    if comment:
        driver.find_element_by_css_selector("input.order__comment").send_keys(comment)
        sleep(0.5)
    for i in range(1,qty):
        driver.find_element_by_id("qtyplus").click()
        sleep(0.1)

    driver.find_element_by_css_selector(".cart_continue button.delivery-type__addorder_btn").click()
    sleep(2)


def make_order():
    driver.get("https://donerking.by/cart")
    sleep(2)
    driver.find_element_by_css_selector("form#orderForm input[name=street]").send_keys("Карла Либкнехта")
    driver.find_element_by_css_selector("form#orderForm input[name=building]").send_keys("94")
    driver.find_element_by_css_selector("form#orderForm input[name=apartment]").send_keys("24")
    driver.find_element_by_css_selector("form#orderForm input[name=level]").send_keys("2")
    driver.find_element_by_css_selector("form#orderForm input[name=code]").send_keys("не работает")
    driver.find_element_by_css_selector("form#orderForm input[name=street]").send_keys("\n")
    sleep(2)
    driver.find_element_by_css_selector("form#orderForm input[name=last_name]").send_keys("Метлицкий")
    driver.find_element_by_css_selector("form#orderForm input[name=first_name]").send_keys("Алексей")
    for d in list("447373590"): 
        driver.find_element_by_css_selector("form#orderForm input[name=phone]").send_keys(d)

    driver.find_element_by_css_selector("form#orderForm textarea[name=comment]").send_keys("Подъезд - 2;\nДомофон не работает - звоните на мобильный;\nОплата картой")


if __name__ == "__main__":

    add_to_cart("https://donerking.by/menu/doner_kebab_po_belarusski_xl")

    add_to_cart("https://donerking.by/menu/kurochka_bbq_s_ikroy_iz_zapechennyih_ovoschey_na_u_1", 
            comment="Без майонеза", 
            ingrids=[("Шампиньоны жареные", "2")],
            lavash="Сырный")

    add_to_cart("https://donerking.by/menu/shaurma_with_chicken_xxl", 
            qty=1, 
            ingrids=[("Майонез", 1)], 
            lavash="Сырный")

    #add_to_cart("https://donerking.by/menu/banditos_s_kuritsey_xl")

    make_order()


