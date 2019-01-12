import pandas
from bokeh.plotting import figure, show, output_file
from bokeh.layouts import widgetbox
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, TableColumn, NumberFormatter
from datetime import date
from random import randint




flights = pandas.read_pickle('flights_all')
airline_list = pandas.read_pickle('airlines')

airline_dict = airline_list.set_index('Code').T.to_dict('list')

# #Overview of data
# Most flights departing
origin_count = flights['ORIGIN'].value_counts()
origin_count_sorted = origin_count.sort_values(ascending=False)
origins = origin_count_sorted.keys()[0:25]

#
# ost flights arriving
dest_count = flights['DEST'].value_counts()
dest_count_sorted = dest_count.sort_values(ascending=False)
print(dest_count_sorted.keys()[0:25])

x = flights['DEP_DELAY']
y = flights['ARR_DELAY']

print(x)
output_file("scatter.html")
p = figure(plot_width=400, plot_height=400)
p.circle(flights['DEP_DELAY'], flights['ARR_DELAY'])
show(p)


#Does late departure mean late arrival?
for origin in origins:
    origin_data = flights[flights['ORIGIN'] == origin]
    # x = origin_data['DEP_DELAY']
    # print(x)
    print(origin_data)
    departure_delay = origin_data['DEP_DELAY'].mean()
    print(origin + ': ' + str(round(departure_delay,1)))


#
# # Most popular route
# routes = flights.groupby(['ORIGIN', 'DEST']).size().reset_index(name='count').sort_values(['count'], ascending=False)
# print(routes)

#On time flights total
# zero_minutes_late = len(flights[flights['ARR_DELAY'] <= 0])
# late_flights = len(flights[flights['ARR_DELAY'] > 0])
# total_flights = len(flights)

# percent_on_time = zero_minutes_late/total_flights

# print(zero_minutes_late)
# print(late_flights)
# print(percent_on_time)

# On time arrivals by origin airport

# origins = flights['ORIGIN'].unique()
# top_100_origins = origins[0:10]

# for origin in top_100_origins:
#     zero_minutes_late = len(flights[(flights['ORIGIN'] == origin) & (flights['ARR_DELAY'] <= 0)])
#     total_flights = len(flights[flights['ORIGIN'] == origin])
#     percent_on_time = zero_minutes_late/total_flights
#     print(str(origin) + ": " + str(percent_on_time))

# On time arrivals by destination airport

# destinations = flights['DEST'].unique()
# top_100_destinations = destinations[0:10]
#
# for destination in top_100_destinations:
#     zero_minutes_late = len(flights[(flights['DEST'] == destination) & (flights['ARR_DELAY'] <= 0)])
#     total_flights = len(flights[flights['ORIGIN'] == destination])
#     percent_on_time = zero_minutes_late / total_flights
#     print(str(destination) + ": " + str(percent_on_time))

# On time arrival by airline
airlines = flights['OP_UNIQUE_CARRIER'].unique()
# print(airline_dict.items())

airline_axis = []
on_time_percentage_axis = []
departure_delay = []
taxi_out = []
arr_delay = []
taxi_in = []
cancelled = []
per_cancelled = []
delayed = []
tot_flights = []

# Airline summary statistics
for airline in airlines:
    airline_data = flights[flights['OP_UNIQUE_CARRIER'] == airline]

    #Airline Name
    airline_name = airline_dict[airline][0]

    # Total flights
    total_flights = len(airline_data)
    total_flights_label = str(total_flights)

    # Average departure delay
    average_dep_delay = str(round(airline_data['DEP_DELAY'].mean(),1))

    # Average taxi out time
    average_taxi_out_time = str(round(airline_data['TAXI_OUT'].mean(),1))

    # Average arrival delay
    average_arr_delay = str(round(airline_data['ARR_DELAY'].mean(),1))

    # Average taxi in time
    average_taxi_in_time = str(round(airline_data['TAXI_IN'].mean(),1))

    # Total flights cancelled
    flights_cancelled = airline_data['CANCELLED'].sum()
    flights_cancelled_label = str(int(flights_cancelled))

    # Percent Cancelled
    percent_cancelled = round(100 * flights_cancelled / total_flights,1)
    percent_cancelled_label = str(percent_cancelled)

    # Number of Flights delayed (Arrive 15 minutes late or greater)
    total_delayed_flights = len(airline_data[airline_data['ARR_DELAY'] >= 15.0])
    total_delayed_flights_label = str(total_delayed_flights)

    # Percent On-Time
    percent_on_time = str(round(100*(total_flights - total_delayed_flights)/total_flights,1))


    print(airline_name)
    print('Number of Flights: ' + total_flights_label)
    print('Average Departure Delay: ' + average_dep_delay)
    print('Average Taxi Out Time: ' + average_taxi_out_time)
    print('Average Arrival Delay: ' + average_arr_delay)
    print('Average Taxi In Time: ' + average_taxi_in_time)
    print('Percent Flights On-Time: ' + percent_on_time + '%')
    print('Flights Cancelled: ' + flights_cancelled_label)
    print('Percent Cancelled: ' + percent_cancelled_label + '%')
    print('Delayed Flights: ' + total_delayed_flights_label)

    airline_axis.append(airline_name)
    on_time_percentage_axis.append(percent_on_time)
    departure_delay.append(float(average_dep_delay))
    taxi_out.append(float(average_taxi_out_time))
    arr_delay.append(float(average_arr_delay))
    taxi_in.append(float(average_taxi_in_time))
    cancelled.append(int(flights_cancelled_label))
    per_cancelled.append(percent_cancelled_label)
    delayed.append(total_delayed_flights)
    tot_flights.append(int(total_flights))

print(airline_axis)
print(on_time_percentage_axis)

output_file('airline_summary.html')

data = dict(
        airlines=[i for i in airline_axis],
        on_time=[x for x in on_time_percentage_axis],
        dep_delay=[a for a in departure_delay],
        taxi_out2=[b for b in taxi_out],
        arr_delay2=[c for c in arr_delay],
        taxi_in2=[d for d in taxi_in],
        cancelled2=[e for e in cancelled],
        per_cancelled2=[f for f in per_cancelled],
        delayed2=[g for g in delayed],
        total_flights2=[h for h in tot_flights]

    )
source = ColumnDataSource(data)

columns = [
        TableColumn(field="airlines", title="Airlines"),
        TableColumn(field="on_time", title="On Time Performance", formatter=NumberFormatter(format="0.0")),
        TableColumn(field="dep_delay", title="Average Departure Delay", formatter=NumberFormatter(format="0.0")),
        TableColumn(field="taxi_out2", title="Taxi Out Time", formatter=NumberFormatter(format="0.0")),
        TableColumn(field="arr_delay2", title="Arrival Delay", formatter=NumberFormatter(format="0.0")),
        TableColumn(field="taxi_in2", title="Taxi In Time", formatter=NumberFormatter(format="0.0")),
        TableColumn(field="cancelled2", title="Flights Cancelled", formatter=NumberFormatter(format="0,0")),
        TableColumn(field="per_cancelled2", title="Percent Cancelled"),
        TableColumn(field="total_flights2", title="Total Flights", formatter=NumberFormatter(format="0,0"))

]
data_table = DataTable(source=source,
                       columns=columns,
                       width=850,
                       height=280,
                       index_position=None,
                       sortable=True
                       )

show(widgetbox(data_table))


# Most common day of the week to travel
# days = ['1','2','3','4','5','6','7']
# 1 = Monday, 7 = Sunday
days = {'Monday': 1, 'Tuesday': 2, 'Wednesday': 3, 'Thursday': 4, 'Friday': 5, 'Saturday': 6, 'Sunday': 7}
months = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}




for key, value in days.items():
    day_of_week = key
    day_num = value
    day_data = flights[flights['DAY_OF_WEEK']==day_num]
    delay_by_day = day_data['ARR_DELAY'].mean()
    print(day_of_week + ': ' + str(round(delay_by_day,1)))

print(tot_flights)



# Most likely to be late when
# Predict delay
# Longest taxi time



# get row by row number
# print(flights.iloc[5500000])



# ['YEAR' 'QUARTER' 'MONTH' 'DAY_OF_MONTH' 'DAY_OF_WEEK' 'FL_DATE'
#  'OP_UNIQUE_CARRIER' 'ORIGIN' 'DEST' 'CRS_DEP_TIME' 'DEP_TIME' 'DEP_DELAY'
#  'TAXI_OUT' 'WHEELS_OFF' 'WHEELS_ON' 'TAXI_IN' 'CRS_ARR_TIME' 'ARR_TIME'
#  'ARR_DELAY' 'CANCELLED' 'CANCELLATION_CODE' 'DIVERTED' 'CRS_ELAPSED_TIME'
#  'ACTUAL_ELAPSED_TIME' 'AIR_TIME' 'FLIGHTS' 'DISTANCE' 'CARRIER_DELAY'
#  'WEATHER_DELAY' 'NAS_DELAY' 'SECURITY_DELAY' 'LATE_AIRCRAFT_DELAY'
#  'Unnamed: 32']