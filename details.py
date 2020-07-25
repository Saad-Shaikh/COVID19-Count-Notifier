# API that returns JSON with state details
state_url = 'https://api.covid19india.org/data.json'


# API that returns JSON with district details
district_url = 'https://api.covid19india.org/v2/state_district_wise.json'


# list of dicts having state names and their respective cities for which you want data
# for the correct state and city names, refer state_url and district_url above
states_and_cities = [
        {'state': 'state1', 'cities': ['city1', 'city2']},
        {'state': 'state2', 'cities': ['city3']},
    ]

# IDs to whom you want to send emails and the states and cities they are interested in
# a state can have zero or more cities under it, but state name should be present if
# a city from that state is included in the list
email_list = [
    {'email': 'recipientemail1', 'states': ['requestedstate1'], 'cities': ['requestedcity1', 'requestedcity2']},
    {'email': 'recipientemail2', 'states': ['requestedstate1', 'requestedstate2'], 'cities': ['requestedcity1', 'requestedcity3']},
]
