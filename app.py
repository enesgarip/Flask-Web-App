from flask import Flask, render_template, request, redirect, url_for
import requests
import mysql.connector as mysql
from bs4 import BeautifulSoup

app = Flask(__name__)

db = mysql.connect(
    host="localhost",
    user="newuser",
    passwd="password"
)
cursor = db.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS productdb")
db.database = "productdb"
cursor.execute(
    "CREATE TABLE IF NOT EXISTS product (id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), "
    "image VARCHAR(255), price DECIMAL(12,2))")


def add_product_database(d):
    query = "INSERT INTO product (name, image, price) VALUES (%s, %s, %s)"
    values = (d['name'], d['image'], d['price'])
    cursor.execute(query, values)
    db.commit()


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
    add_product_database(product_obj)
    return product_obj


def product_details(p_id):
    try:
        query = "SELECT * FROM product WHERE id=%s"
        p_id = (p_id,)
        cursor.execute(query, p_id)
        data = cursor.fetchall()
        return data
    except:
        return "error!!"


def all_products():
    query = "SELECT * FROM product ORDER BY id"
    cursor.execute(query)
    records = cursor.fetchall()
    return records


@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        product_link = request.form['inputForm']
        if "www.etsy.com" in product_link:
            product_obj = add_product(product_link)
            return render_template("added-product.html", data=product_obj)
        else:
            return redirect(url_for('error'))
    else:
        return render_template("home.html")


@app.route("/error")
def error():
    return render_template("error.html")


@app.route("/products")
def products():
    records = all_products()
    return render_template("products.html", data=records)


@app.route("/product<product_id>")
def product(product_id):
    try:
        data=product_details(product_id)
        return render_template("product.html", data=data[0])
    except:
        return redirect(url_for('error'))


if __name__ == '__main__':
    app.run()
