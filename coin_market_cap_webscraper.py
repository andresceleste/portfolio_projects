import json
import os

import pandas as pd
from dotenv import load_dotenv
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

# Set display options for pandas
pd.set_option("display.width", 400)
pd.set_option("display.max_row", None)
pd.set_option("display.max_column", None)
pd.set_option("display.float_format", "{:.2f}".format)


# Load environment variables from the .env file
load_dotenv()

# Access the API key from the environment variables
api_key = os.getenv("COIN_MARKETCAP_API_KEY")

# URL for the CoinMarketCap API to fetch cryptocurrency data
url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

# Parameters for the API request (start: starting rank, limit: maximum number of
# cryptocurrencies to retrieve, convert: currency to convert prices to)
parameters = {"start": "1", "limit": "5000", "convert": "USD"}

# Headers required for the API request, including the API key
headers = {
    "Accepts": "application/json",  # Specify the response format as JSON
    "X-CMC_PRO_API_KEY": api_key,  # Provide the API key for authentication
}

# Create a session object to maintain connection settings and headers
try:
    session = Session()
    session.headers.update(headers)
except NameError:
    print("Error: 'headers' variable is not defined.")


def get_crypto_currency_info(output_file):
    """
    Fetch cryptocurrency information from CoinMarketCap API and save to a CSV file.

    :param output_file: Output CSV file path to save the data.
    """
    # List to store parsed cryptocurrency data
    cryptocurrency_data = []

    try:
        # Make a GET request to the API endpoint with the specified parameters
        response = session.get(url, params=parameters)

        # Load the response JSON data into a Python dictionary
        data = json.loads(response.text)

        # Iterate over each cryptocurrency item in the API response data
        for item in data["data"]:
            # Create a dictionary to store cryptocurrency information
            cryptocurrency_info = {}

            # Extract relevant data fields from the API response and add them to the dictionary
            cryptocurrency_info["Rank"] = item["cmc_rank"]
            cryptocurrency_info["Name"] = item["name"]
            cryptocurrency_info["Symbol"] = item["symbol"]
            cryptocurrency_info["Price"] = item["quote"]["USD"]["price"]
            cryptocurrency_info["Market_Cap"] = item["quote"]["USD"]["market_cap"]
            cryptocurrency_info["Circulating_Supply"] = item["circulating_supply"]

            # Append the cryptocurrency information dictionary to the list
            cryptocurrency_data.append(cryptocurrency_info)

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        # Handle connection-related errors gracefully
        print(f"Error: {e}")

    # Create a DataFrame from the parsed cryptocurrency data
    df = pd.DataFrame(cryptocurrency_data)

    # Create a CSV file
    df.to_csv(output_file)
    print(f"Data saved to {output_file}")


if __name__ == "__main__":
    # Define the output file path
    output_file_path = "../../data_analytics/datasets/crypto_currency_info.csv"

    # Call the function to get cryptocurrency data from CoinMarketCap API and create a csv file.
    get_crypto_currency_info(output_file_path)
