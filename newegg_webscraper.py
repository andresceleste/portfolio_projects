from bs4 import BeautifulSoup as bs
import requests


def get_product_info(url):
    """
    Get product information (title and total price) from a Newegg product page.

    :param url: The URL of the product page.
    :return: The total price of the product (including dollars and cents).
    """
    # Fetch HTML content from the URL
    response = requests.get(url)

    # Create a Beautiful Soup object to parse the HTML content
    soup = bs(response.text, 'html.parser')
    # print(soup)

    # Extract product title
    product_title = soup.find('h1').text.strip()

    # Find all occurrences of "$" in the HTML
    prices = soup.find_all(string='$')

    # Get the parent element of the first "$" occurrence
    parent = prices[0].parent

    # Find the elements containing dollars and cents
    dollars = parent.find("strong")
    cents = parent.find("sup")

    # Construct the total price string
    product_price = f'${dollars.string}{cents.string}'

    # Create a dictionary to store the product information
    product_info = {
        'product_title': product_title,
        'product_price': product_price
    }

    return product_info


if __name__ == '__main__':
    # Example usage
    url = 'https://www.newegg.com/gigabyte-geforce-rtx-3080-ti-gv-n308tgaming-oc-12gd/p/N82E16814932436'
    product_info = get_product_info(url)
    print(f'Product: {product_info["product_title"]}')
    print(f'Price: {product_info["product_price"]}')
