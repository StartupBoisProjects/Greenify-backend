def calculate_co2(mode_of_transport, trip_length_m, trip_time_s):
    mode_of_transport_options = ['RAIL', 'METRO_RAIL', 'SUBWAY', 'TRAM', 'MONORAIL', 'HEAVY_RAIL', 'COMMUTER_TRAIN',
                                 'HIGH_SPEED_TRAIN', 'TROLLEYBUS', 'SHARE_TAXI']
    emissions_list = [30, 5.8, 6.9, 15.69, 20.6, 25, 5, 10.5, 42.0, 90, 30] #In g

    if mode_of_transport == 'DRIVING':
        emissions = 200
    elif mode_of_transport == 'WALKING' or mode_of_transport == 'BICYCLE':
        emissions = 0
    elif mode_of_transport == 'BUS' or mode_of_transport == 'INTERCITY_BUS':
        emissions = 110
    elif mode_of_transport == 'AIRPLANE':
        emissions = 150
    elif mode_of_transport in mode_of_transport_options:
        emissions = trip_length_m*emissions_list[mode_of_transport_options.index(mode_of_transport)]/1000 #In g, km
    else:
        emissions = False
    emissions = emissions/1000*3.6 # In kg
    return emissions
