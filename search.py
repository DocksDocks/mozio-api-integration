from time import sleep
from constants import BASE_URL, HEADERS, indent
from reservations import reservation_test
from requests import post, get


def create_search(params: dict):
    """
    Creates a search.

    Parameters:
    - params (dict): The search parameters.

    Returns:
    - response (dict): The response of the search.
    """
    url = f'{BASE_URL}/v2/search/'
    response = post(url, json=params, headers=HEADERS)
    response.raise_for_status()
    if response.status_code != 201:
        print('Error creating search')
    return response.json()


def retrieve_search_poll(search_id: str):
    """
    Retrieves a search poll based on search_id.

    Parameters:
    - search_id (str): The search id.

    Returns:
    - dict: The API response.
    """
    url = f'{BASE_URL}/v2/search/{search_id}/poll/'
    response = get(url, headers=HEADERS)
    response.raise_for_status()
    if response.status_code != 200:
        raise ValueError('Error polling search results')
    return response.json()


def retrieve_search_loop(search_id: str):
    """
    Retrieves a search poll based on search_id.
    Finds the cheapest result with the provider name "Dummy External Provider" and runs the function reservation_test.

    Parameters:
    - search_id (str): The search id.
    """
    while True:
        response = retrieve_search_poll(search_id)
        if not response.get('more_coming'):
            break

        results = response.get('results', [])
        if results:
            min_price = float('inf')
            cheapest_result_id = None

            for result in results:
                if not result["steps"]:
                    continue

                for step in result["steps"]:
                    if step["details"]["provider_name"] == "Dummy External Provider":
                        price = float(
                            step["details"]["price"]["price"]["value"])
                        print(f'Found result for Provider "Dummy External Provider":\n' +
                              f'price: {price}\n' +
                              f'result_id: {result["result_id"]}\n')

                        if price < min_price:
                            min_price = price
                            cheapest_result_id = result["result_id"]

            if cheapest_result_id:
                print(f'Result selected: \n' +
                      f'price: {min_price}\n' +
                      f'result_id: {cheapest_result_id}\n')
                reservation_test(search_id, cheapest_result_id)
                return

        sleep(1)

    print('No results found')
    exit()


def search_test():
    """
    Creates a search and retrieves the results.
    """
    search_params = {
        'start_address': '44 Tehama Street, San Francisco, CA, USA',
        'end_address': 'SFO',
        'mode': 'one_way',
        'pickup_datetime': '2023-12-01 15:30',
        'num_passengers': 2,
        'currency': 'USD',
        'campaign': 'Eduardo Marquez Costa Barbosa',
        "no_poll": False
    }
    create_search_response = create_search(search_params)
    search_id = create_search_response.get('search_id')
    print(f'Create Search ID: {search_id}')
    retrieve_search_loop(search_id)
