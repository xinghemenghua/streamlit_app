import re

import pandas as pd
import requests
import streamlit as st


st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_page_config(
    page_title="weather",
    page_icon="🌤️",
)


mykey = '&key=' + '61cd6b6bd7ad4819a765ef17b425ea4b'  # EDIT HERE!

url_api_weather = 'https://devapi.qweather.com/v7/weather/'
url_api_geo = 'https://geoapi.qweather.com/v2/city/'
url_api_rain = 'https://devapi.qweather.com/v7/minutely/5m'
url_api_air = 'https://devapi.qweather.com/v7/air/now'


def get(api_type):
    url = url_api_weather + api_type + '?location=' + city_id + mykey
    return requests.get(url).json()


def rain(lat, lon):
    url = url_api_rain + '?location=' + lat + ',' + lon + mykey
    return requests.get(url).json()


def air(city_id):
    url = url_api_air + '?location=' + city_id + mykey
    return requests.get(url).json()


def get_city(city_kw):
    url_v2 = url_api_geo + 'lookup?location=' + city_kw + mykey
    city = requests.get(url_v2).json()['location'][0]

    city_id = city['id']
    district_name = city['name']
    city_name = city['adm2']
    province_name = city['adm1']
    country_name = city['country']
    lat = city['lat']
    lon = city['lon']

    return city_id, district_name, city_name, province_name, country_name, lat, lon


def now():
    return get_now['now']


def daily():
    return get_daily['daily']


def hourly():
    return get_hourly['hourly']


def get_icon(weather_text):
    if re.match("晴", weather_text):
        return '☀️'
    elif re.match("多云", weather_text):
        return '⛅'
    elif re.match("阴", weather_text):
        return '☁️︎️'
    elif re.match("小雨", weather_text):
        return '🌧️'
    elif re.match("中雨", weather_text):
        return '🌧️🌧️'
    elif re.match("大雨", weather_text):
        return '🌧️🌧️🌧️'
    elif re.match("雷阵雨", weather_text):
        return '⛈️'
    elif re.match("小雪", weather_text):
        return '🌨️'
    elif re.match("中雪", weather_text):
        return '🌨️🌨️'
    elif re.match("大雪", weather_text):
        return '🌨️🌨️🌨️'
    elif re.match("雾", weather_text):
        return '🌫️'
    else:
        return weather_text


city = st.text_input(label="输入城市", value='南昌', placeholder='例如：南昌')

if city is not None:
    city_input = city
    city_idname = get_city(city_input)

    city_id = city_idname[0]

    get_now = get('now')
    get_daily = get('7d')  # 3d/7d/10d/15d
    get_hourly = get('24h')  # 24h/72h/168h
    get_rain = rain(city_idname[5], city_idname[6])  # input longitude & latitude
    air_now = air(city_id)['now']

    # st.write(json.dumps(get_now, sort_keys=True, indent=4))
    if city_idname[2] == city_idname[1]:
        st.write(city_idname[3], str(city_idname[2]) + '市')
    else:
        st.write(city_idname[3], str(city_idname[2]) + '市', str(city_idname[1]) + '区')

    now_weather, temp, sen_temp, = st.columns(3)
    now_weather.metric(label='当前天气', value=get_icon(get_now['now']['text']), delta=get_now['now']['text'], delta_color='off')
    temp.metric(label='温度', value=get_now['now']['temp'] + '°C')
    sen_temp.metric(label='体感温度', value=get_now['now']['feelsLike'] + '°C')

    today_weather, today_tempmin, today_tempmax, = st.columns(3)
    today_weather.metric(label='今日天气', value=get_icon(daily()[0]['textDay']), delta=daily()[0]['textDay'], delta_color='off')
    today_tempmin.metric(label='今日最低温度', value=daily()[0]['tempMin'] + '°C')
    today_tempmax.metric(label='今日最高温度', value=daily()[0]['tempMax'] + '°C')

    st.metric(label='空气质量指数：', value=air_now['aqi'])

    weather_1, weather_2, weather_3,weather_4,weather_5,weather_6 = st.columns(6)
    weather_1.metric(label='1日后天气', value=get_icon(daily()[1]['textDay']),delta=daily()[1]['textDay']+'  '+daily()[1]['tempMin']+'-'+daily()[1]['tempMax']+'°C', delta_color='off')
    weather_2.metric(label='2日后天气', value=get_icon(daily()[2]['textDay']),delta=daily()[2]['textDay']+'  '+daily()[2]['tempMin']+'-'+daily()[2]['tempMax']+'°C', delta_color='off')
    weather_3.metric(label='3日后天气', value=get_icon(daily()[3]['textDay']),delta=daily()[3]['textDay']+'  '+daily()[3]['tempMin']+'-'+daily()[3]['tempMax']+'°C', delta_color='off')
    weather_4.metric(label='4日后天气', value=get_icon(daily()[4]['textDay']),delta=daily()[4]['textDay']+'  '+daily()[4]['tempMin']+'-'+daily()[4]['tempMax']+'°C', delta_color='off')
    weather_5.metric(label='5日后天气', value=get_icon(daily()[5]['textDay']),delta=daily()[5]['textDay']+'  '+daily()[5]['tempMin']+'-'+daily()[5]['tempMax']+'°C', delta_color='off')
    weather_6.metric(label='6日后天气', value=get_icon(daily()[6]['textDay']),delta=daily()[6]['textDay']+'  '+daily()[6]['tempMin']+'-'+daily()[6]['tempMax']+'°C', delta_color='off')

    data = [[daily()[0]['tempMin'], daily()[0]['tempMax']], [daily()[1]['tempMin'], daily()[1]['tempMax']],
            [daily()[2]['tempMin'], daily()[2]['tempMax']], [daily()[3]['tempMin'], daily()[3]['tempMax']],
            [daily()[4]['tempMin'], daily()[4]['tempMax']], [daily()[5]['tempMin'], daily()[5]['tempMax']],
            [daily()[6]['tempMin'], daily()[6]['tempMax']]]

    chart_data = pd.DataFrame(data, columns=['最低温度', '最高温度'], dtype=float)
    st.line_chart(chart_data)
