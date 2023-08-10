from time import sleep
from constants import BASE_URL, HEADERS, indent
from requests import post, get, delete
from pprint import pformat


def reservations_create(data: dict) -> dict:
    """
    Creates a reservation.
    Parameters:
    - data (dict): The reservation details.
    Returns:
    - bool: True if the reservation was created, False otherwise.
    - dict: The API response.
    """
    print("Creating reservation...")
    url = f'{BASE_URL}/v2/reservations/'
    response = post(url, headers=HEADERS, json=data)
    print("Create reservation response:", response.json())
    response.raise_for_status()
    if response.status_code != 201:
        print('Error creating reservation')
        return False, response.json()
    return True, response.json()


def reservations_retrieve_poll(search_id: str) -> dict:
    """
    Retrieves a reservation.
    Parameters:
    - search_id (str): The id of the reservation.
    Returns:
    - dict: The API response.
    """
    url = f'{BASE_URL}/v2/reservations/{search_id}/poll'
    response = get(url, headers=HEADERS)
    response.raise_for_status()
    if response.status_code == 202:
        print('Waiting reservation to be completed...')
    return response.json()


def retrieve_reservations_loop(search_id: str):
    """
    Retrieves a reservation based on search_id.
    Parameters:
    - search_id (str): The id of the reservation.
    Returns:
    - reservation: The API response.
    """
    while True:
        response = reservations_retrieve_poll(search_id)
        status = response.get("status")

        if status == "completed":
            print("Reservation completed")
            reservations = response.get("reservations", [])
            if reservations:
                return reservations[0]
        sleep(1)
        if not status:
            break
    print('No reservation found')
    exit()


def reservations_cancel(hashed_id: str) -> bool:
    """
    Cancels a reservation.
    Parameters:
    - confirmation_number (str): The confirmation nubmer (hashed_id) of the reservation.
    Returns:
    - bool: True if the reservation was cancelled, False otherwise.
    """
    url = f'{BASE_URL}/v2/reservations/{hashed_id}/'
    response = delete(url, headers=HEADERS)
    response.raise_for_status()
    if response.status_code != 202:
        return False, response.json()
    else:
        return True, response.json()


def reservation_test(search_id: str, result_id: str):
    """
    Creates a reservation, polls for it, and cancels it.

    Parameters:
    - search_id (str): The search id.
    - result_id (str): The result id.
    """
    reservation_data = {
        'search_id': search_id,
        'result_id': result_id,
        'email': 'happytraveller@mozio.com',
        'country_code_name': 'US',
        'phone_number': '8776665544',
        'first_name': 'John',
        'last_name': 'Doe',
        'airline': 'AA',
        'flight_number': '132',
        'customer_special_instructions': 'My doorbell is broken, please yell'
    }
    created, created_response = reservations_create(reservation_data)
    if (created):
        print(f'Reservations created')
    else:
        print(
            f'Error creating reservation: {pformat(created_response, indent)}')
        exit()
    print("Polling for reservation...")
    reservation = retrieve_reservations_loop(search_id)
    confirmation_number = reservation.get('confirmation_number')
    id = reservation.get('id')
    cancelled, cancelled_response = reservations_cancel(id)
    if (cancelled):
        print(
            f'Booking was made and cancelled. Confirmation number: {confirmation_number}')
        print(f'Hashed id: {id}')
    else:
        print('Something went wrong cancelling reservation')
        print(
            f'Error cancelling reservation: {pformat(cancelled_response, indent)}')
