import plotly.plotly as py
import plotly.graph_objs as go
import plotly
import csv

#REPLACE PLOTLY USERNAME & API KEY HERE
plotly.tools.set_credentials_file(username='XXXXXXXX', api_key='XXXXXXXXXXXXXXXXXXXX')

city_list=list()
positive_list=list()
negative_list=list()
neutral_list=list()

with open('sentimentValueList.csv','r') as cityData:
	csv_reader=csv.reader(cityData, delimiter=',')
	line_count=0
	for row in csv_reader:
		city_list.append(row[0])
		positive_list.append(row[1])
		negative_list.append(row[2])
		neutral_list.append(row[3])

trace0 = go.Scatter(
	x = city_list,
	y = positive_list,
	name = 'Positive Sentiment Values',
	line = dict(
		color = ('rgb(205, 12, 24)'),
		width = 2)
)

trace1 = go.Scatter(
	x = city_list,
	y = negative_list,
	name ='Negative Sentiment Values',
	line = dict(
		color = ('rgb(22, 96, 167)'),
		width = 2)
)

trace2 = go.Scatter(
	x = city_list,
	y = neutral_list,
	name ='Neutral Sentiment Values',
	line = dict(
		color = ('rgb(205, 12, 24)'),
		width = 2,
		dash ='dash')
)
		
data = [trace0, trace1, trace2]

# Edit the layout
layout = dict(title = 'Tweet Sentiment Analysis in New York',
              xaxis = dict(title = 'City'),
              yaxis = dict(title = 'Sentiment Score(%)'),
              )

fig = dict(data=data, layout=layout)
py.iplot(fig, filename='styled-line')