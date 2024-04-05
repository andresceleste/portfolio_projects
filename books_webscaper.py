from bs4 import BeautifulSoup as bs
import requests
import pandas as pd

BASE_URL = "http://books.toscrape.com/catalogue/"


def scrape_books(output_file):
    """
    Scrape book data from a website and save it to an Excel file.

    Args:
    output_file (str): File path to save the scraped data.

    Returns:
    None
    """
    data = []
    current_page = 1
    proceed = True

    while proceed:
        print(f"Currently scraping page: {current_page}")
        url = f"{BASE_URL}/page-{current_page}.html"
        page = requests.get(url)
        soup = bs(page.content, "html.parser")

        if soup.title.text == "404 Not Found":
            proceed = False
        else:
            all_books = soup.find_all("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")

            for book in all_books:
                item = {}
                item["Title"] = book.find("img").attrs["alt"]
                item["Link"] = BASE_URL + book.find("a").attrs["href"]
                item["Price"] = book.find("p", class_="price_color").text[1:]
                item["Stock"] = book.find("p", class_="instock availability").text.strip()
                data.append(item)

        current_page += 1

    df = pd.DataFrame(data)
    df.to_excel(output_file)
    print(f"Scraping complete. Data saved to '{output_file}'")


if __name__ == "__main__":
    # Define the output file path
    output_file = "output_dir_path/file_name.xlsx"

    # Call the function to scrape books and save the data
    scrape_books(output_file)
