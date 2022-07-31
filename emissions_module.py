def calculate_co2(mode_of_transport, trip_length_m, trip_time_s):
    mode_of_transport_options = ['RAIL', 'METRO_RAIL', 'SUBWAY', 'TRAM', 'MONORAIL', 'HEAVY_RAIL', 'COMMUTER_TRAIN',
                                 'HIGH_SPEED_TRAIN', 'BUS', 'INTERCITY_BUS', 'TROLLEYBUS', 'SHARE_TAXI']
    emissions_list = [41, 4.8, 6.4, 14.69, 23.6, 20, 10, 20.5, 26.72, 25, 37, 132, 19] #In g

    if mode_of_transport == 'DRIVING':
        mean_speed = trip_length_m/trip_time_s*3.6 # In km/h
        emissions = (1085*(mean_speed**(-0.7)))*trip_length_m/1000 #In g/km, km, km/h (explained in excel sheet)
    elif mode_of_transport == 'WALKING' or mode_of_transport == 'BICYCLE':
        emissions = 0
    elif mode_of_transport == 'AIRPLANE':
        #mean_speed = trip_length_m/trip_time_s*3.6 # In km/h
        emissions = (-0.1546*trip_length_m/1000+245.27)*trip_length_m/1000 #In km, g/seat_km
    elif mode_of_transport in mode_of_transport_options:
        emissions = trip_length_m*emissions_list[mode_of_transport_options.index(mode_of_transport)]/1000 #In g, km
    else:
        emissions = False
        
    emissions = emissions/1000 # In kg
    return emissions