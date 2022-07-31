
import requests, json
from numerize import numerize
import geopy.distance
import emissions_module

# ----------------------------------------------------------------

def script(start_location, end_location, api_key_gmaps):

    final_list = []
    flight_geocodes = []
    
    key_gmaps = api_key_gmaps
    start_location = start_location
    end_location = end_location

    URL_base = "https://maps.googleapis.com/maps/api/directions/json?"
    URL_parameters = "&origin=" + start_location + "&destination=" + end_location + "&alternatives=" + "true" + "&key=" + key_gmaps

    URL_transit = URL_base + "mode=" + "transit" + URL_parameters
    URL_driving = URL_base + "mode=" + "driving" + URL_parameters

    driving_emissions = get_emissions_list(URL_driving)
    final_list.append(driving_emissions[0])

    transit_emissions = get_emissions_list(URL_transit)
    final_list.append(transit_emissions[0])

    flight_emissions = []
    flight_emissions.append(get_flight_emissions(transit_emissions[1]))
    final_list.append(flight_emissions)

    final_json = {"final_list": final_list}
    return final_json



def get_emissions_list(URL):

    print(URL)

    response = requests.get(URL)
    response = response.json()

    print("Number of transport options: " + str(len(response['routes'])))

    all_options = []

    for x in range(len(response['routes'])):

        option_legs = []

        for y in range(len(response['routes'][x]['legs'][0]['steps'])):

            if response['routes'][x]['legs'][0]['steps'][y]['travel_mode'] == "TRANSIT":
                mode = response['routes'][x]['legs'][0]['steps'][y]['transit_details']['line']['vehicle']['type']
            else:
                mode = response['routes'][x]['legs'][0]['steps'][y]['travel_mode']

            distance = response['routes'][x]['legs'][0]['steps'][y]['distance']['value']
            duration = response['routes'][x]['legs'][0]['steps'][y]['duration']['value']

            emissions = emissions_module.calculate_co2(mode, distance, duration)

            option_legs.append(emissions)


        total_option_emissions = 0
        for z in range(len(option_legs)):
            total_option_emissions += option_legs[z]
        total_option_emissions = round(total_option_emissions, 1)
        all_options.append(total_option_emissions)


    return all_options, response
                

def get_flight_emissions(transit_json):

    start_lat = transit_json['routes'][0]['legs'][0]['start_location']['lat']
    start_lon = transit_json['routes'][0]['legs'][0]['start_location']['lng']
    end_lat = transit_json['routes'][0]['legs'][0]['end_location']['lat']
    end_lon = transit_json['routes'][0]['legs'][0]['end_location']['lng']

    distance = geopy.distance.geodesic((start_lat, start_lon), (end_lat, end_lon)).km * 1000

    flight_emissions = emissions_module.calculate_co2("AIRPLANE", distance, "null")
    flight_emissions = round(flight_emissions, 1)

    return flight_emissions
