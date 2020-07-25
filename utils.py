import requests
import json
import db_operations


def get_count_list(states_and_cities, state_url, district_url):
    """
    Returns a list of dicts containing data for requested states and cities.

    Parameters:
        states_and_cities(list): a list of dicts containing requested states and cities.

        state_url(str): url to fetch state data.

        district_url(str): url to fetch city/district data.

    Returns:
        count_list(list): list containing counts for states and cities.
    """

    conn = db_operations.create_connection()
    count_list = []

    # extract statewise list from json response
    state_data_list = json.loads(requests.get(state_url).content).get('statewise')

    # for each requested state, add details to a list of dicts
    for state_details in state_data_list:
        for state_and_city in states_and_cities:            
            if state_and_city.get('state') == state_details.get('state'):
                city_list = get_citywise_list_for_state(
                    state_and_city.get('state'), state_and_city.get('cities'), district_url
                    )  # get details for requested cities of the respective state
                
                old_data_tup = db_operations.read_state_data(conn, state_and_city.get('state'))
                new_data_tup = (state_and_city.get('state'), 
                                state_details.get('confirmed'),
                                state_details.get('active'),
                                state_details.get('deaths')
                            )
                
                db_operations.delete_state_data(conn, state_and_city.get('state'))
                db_operations.write_state_data(conn, new_data_tup)

                count_list.append(
                    {'state': state_and_city.get('state'),
                    'total': new_data_tup[1],
                    'old_total': old_data_tup[1],
                    'active': new_data_tup[2],
                    'old_active': old_data_tup[2],
                    'deaths': new_data_tup[3],
                    'old_deaths': old_data_tup[3],
                    'cities': city_list}
                    )  # add all data to a list of dicts
    
    db_operations.close_connection(conn)
    return count_list


def get_citywise_list_for_state(state, cities, district_url):
    """
    Returns a list of dicts containing data for cities of given state.

    Parameters:
        states(str): state which the cities belong to.

        cities(list): list of requested cities for state.

        district_url(str): url to fetch city/district data.

    Returns:
        city_list(list): list containing counts for cities of given state.
    """

    conn = db_operations.create_connection()

    city_list = []

    # extract districtwise list from json response
    district_data_list = json.loads(requests.get(district_url).content)

    # for every requested city, add details to a list of dicts
    for state_details in district_data_list:
            if state == state_details.get('state'):
                for city_data in state_details.get('districtData'):
                    if city_data.get('district') in cities:
                        old_data_tup = db_operations.read_city_data(conn, city_data.get('district'))
                        new_data_tup = (city_data.get('district'),
                                        city_data.get('confirmed'),
                                        city_data.get('active'),
                                        city_data.get('deceased')
                                    )
                        
                        db_operations.delete_city_data(conn, city_data.get('district'))
                        db_operations.write_city_data(conn, new_data_tup)

                        city_list.append(
                            {'city': city_data.get('district'),
                            'total': new_data_tup[1],
                            'old_total': old_data_tup[1],
                            'active': new_data_tup[2],
                            'old_active': old_data_tup[2],
                            'deceased': new_data_tup[3],
                            'old_deceased': old_data_tup[3]}
                        )
    
    db_operations.close_connection(conn)
    return city_list


def form_message_for_email(count_list, states, cities):
    """
    Returns the formatted message to be sent as email to the receipient.

    Parameters:
        count_list(list): list of dicts containing data for requested states and cities.

        states(list): list of requested states.

        cities(list): list of requested cities.

    Returns:
        formatted_message(str): formatted message to be sent.
    """

    message_list = []

    # nested loop to add all details to a string message
    for elem_dict in count_list:
        if elem_dict.get('state') in states:
            message = (
                "\nState: " + elem_dict.get('state') +
                "\nTotal Cases: " + get_difference_str(elem_dict.get('total'), elem_dict.get('old_total')) +
                "\nActive Cases: " + get_difference_str(elem_dict.get('active'), elem_dict.get('old_active')) +
                "\nDeceased: " + get_difference_str(elem_dict.get('deaths'), elem_dict.get('old_deaths'))
            )
            for city_dict in elem_dict.get('cities'):
                if city_dict.get('city') in cities:
                    message = message + (
                        "\n\n\tCity: " + city_dict.get('city') +
                        "\n\tTotal: " + get_difference_str(city_dict.get('total'), city_dict.get('old_total')) +
                        "\n\tActive: " + get_difference_str(city_dict.get('active'), city_dict.get('old_active')) +
                        "\n\tDeceased: " + get_difference_str(city_dict.get('deceased'), city_dict.get('old_deceased'))
                    )
            message_list.append(message)  # append each message to message list
    
    message_list.append("Data fetched from covid19india.org")
    formatted_message = "\n\n-----------------------------------\n".join(message_list)
    return formatted_message


def get_difference_str(curr, old):
    """
    Returns the formatted string containing difference in counts from yesterday.

    Parameters:
        curr(str): current count.

        old(str): old(yesterday's) count.

    Returns:
        string(str): formatted string.
    """

    curr_num = int(curr)
    old_num = int(old)
    diff = curr_num - old_num

    if(diff == curr_num):
        string = str(curr) + " (+" + str(0) + ")"
    elif(diff >= 0):
        string = str(curr) + " (+" + str(diff) + ")"
    else:
        string = str(curr) + " (" + str(diff) + ")"
    
    return string