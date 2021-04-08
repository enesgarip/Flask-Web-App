from flask import Flask, render_template, request, redirect, url_for
import requests
from bs4 import BeautifulSoup

app1 = Flask(__name__)


def add_product(link):
    product_obj = dict()
    html_requests = requests.get(link)
    soup = BeautifulSoup(html_requests.text, 'html.parser')
    product_name = soup.find(
        attrs={'class': 'wt-text-body-03 wt-line-height-tight wt-break-word wt-mb-xs-1'}).getText().strip()
    product_obj['name'] = product_name
    product_image = soup.find(
        attrs={'class': 'wt-max-width-full wt-horizontal-center wt-vertical-center carousel-image wt-rounded'})[
        'src']
    product_obj['image'] = product_image
    product_price = soup.find(attrs={'class': 'wt-text-title-03 wt-mr-xs-2'}).getText().strip()[1:]
    product_obj['price'] = product_price
    return product_obj


@app1.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        product_link = request.form['inputForm']
        if "www.etsy.com" in product_link:
            # print(addProduct(product_link))
            product_obj = add_product(product_link)
            return render_template("product.html", data=product_obj)
        else:
            return redirect(url_for('error'))
    else:
        return render_template("home.html")


@app1.route("/error")
def error():
    return render_template("error.html")


@app1.route("/products")
def products():
    return render_template("products.html")


if __name__ == '__main__':
    app1.run(debug=True)
