import yfinance as yf
import streamlit as st
import pandas as pd
import numpy as np 
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.write("""
# Котировки акций компании Apple     
""")

tickerSymbol = 'AAPL'
tickerData = yf.Ticker(tickerSymbol)
tickerDf = tickerData.history(period='1d', start='2020-5-31', end='2022-5-31')

st.subheader('График закрытия цен')
st.line_chart(tickerDf.Close)

st.subheader('График объема торгов')
st.line_chart(tickerDf.Volume)

st.subheader("График изменения цен акций Apple")
price_changes = tickerDf.Close - tickerDf.Open
st.line_chart(price_changes)

st.write("""
# Визуализация датасета tips     
""")

data_url = ('https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv')
def load_data(path):
    data = pd.read_csv(path)
    return data

st.subheader('Сырые данные')
tips = load_data(data_url)
st.write(tips)

tips['time_order'] = pd.to_datetime(np.random.uniform(pd.to_datetime('2023-01-01').timestamp(),
                                                pd.to_datetime('2023-01-31').timestamp(),
                                                size=len(tips)), unit='s')
tips['time_order'] = pd.to_datetime(tips['time_order'])
tips['time_order'] = tips['time_order'].dt.date

# Динамика чаевых во времени
tips_dynamics = tips.groupby('time_order')['tip'].mean().reset_index()

fig = px.line(tips_dynamics, x='time_order', y='tip', markers=True, title='Динамика чаевых во времени')
fig.update_layout(
    xaxis_title='Дата заказа',
    yaxis_title='Чаевые',
    xaxis=dict(tickangle=45),
)
st.plotly_chart(fig)

# Распределение значений размеров счетов
fig = px.histogram(tips, x='total_bill', title='Распределение значений размера счетов',
                   labels={'total_bill': 'Размер счета', 'count': 'Частота'})

st.plotly_chart(fig)

# Зависимость размера чаевых от размера счета
fig = px.scatter(tips, x='total_bill', y='tip', title='Зависимость размера чаевых от размера счета', )
fig.update_layout(
    xaxis_title='Размер счета',
    yaxis_title='Размер чаевых',
)
st.plotly_chart(fig)

# Взаимосвязь размера счета, чаевых и размера
fig = px.scatter(tips, x='total_bill', y='tip', title='Взаимосвязь размера счета, чаевых и размера', size='size')
fig.update_layout(
    xaxis_title='Размер счета',
    yaxis_title='Размер чаевых',
)
st.plotly_chart(fig)

# Cвязь между днем недели и размером счета
df = tips.groupby('day', as_index=False).agg({'total_bill': 'sum'})

days_order = ['Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun']
df['day'] = pd.Categorical(df['day'], categories=days_order, ordered=True)
df = df.sort_values('day')
fig = px.bar(df, x='day', y='total_bill', title='Cвязь между днем недели и размером счета')
fig.update_layout(
    xaxis_title='День недели',
    yaxis_title='Размер счета',
)
st.plotly_chart(fig)

# Cвязь между днем недели, размером чаевых и полом клиента
fig = px.scatter(tips, x='tip', y='day', color='sex', title='Cвязь между днем недели, размером чаевых и полом клиента')
fig.update_layout(
    xaxis_title='День недели',
    yaxis_title='Размер счета',
)
st.plotly_chart(fig)

# Сумма счетов по дням
fig = px.box(tips, x='day', y='total_bill', color='time', title='Сумма счетов по дням')
fig.update_layout(
    xaxis_title='День недели',
    yaxis_title='Сумма счетов',
)
st.plotly_chart(fig)

# Гистограммы чаевых
tips_lunch = tips[tips['time'] == 'Lunch']
tips_dinner = tips[tips['time'] == 'Dinner']

fig_lunch = px.histogram(tips_lunch, x='tip', color_discrete_sequence=['blue'],
                         title='Гистограмма чаевых на обед', labels={'tip': 'Чаевые'})
fig_dinner = px.histogram(tips_dinner, x='tip', color_discrete_sequence=['red'],
                          title='Гистограмма чаевых на ужин', labels={'tip': 'Чаевые'})
fig = make_subplots(rows=1, cols=2, subplot_titles=['Обед', 'Ужин'])
fig.add_trace(fig_lunch['data'][0], row=1, col=1)
fig.add_trace(fig_dinner['data'][0], row=1, col=2)

fig.update_layout(title='Гистограммы чаевых', showlegend=False)

st.plotly_chart(fig)

# Размер чаевых и счета у мужчин и женщин
fig = make_subplots(rows=1, cols=2, subplot_titles=['Для женщин', 'Для мужчин'])
female = px.scatter(tips[tips['sex'] == 'Female'], 
                            x='total_bill', y='tip', color='smoker',
                            title='Для женщин')
female_data = female['data'][0]
fig.add_trace(go.Scatter(female_data), row=1, col=1)

male = px.scatter(tips[tips['sex'] == 'Male'], 
                          x='total_bill', y='tip', color='smoker',
                          title='Для мужчин')
male_data = male['data'][0]
fig.add_trace(go.Scatter(male_data), row=1, col=2)

fig.update_layout(title='Размер чаевых и счета у мужчин и женщин', showlegend=False)

st.plotly_chart(fig)

# Тепловая карта корреляций числовых переменных
numeric_columns = tips.select_dtypes(include='number')
correlation_matrix = numeric_columns.corr()
fig = go.Figure(data=go.Heatmap(z=correlation_matrix.values,
                                x=correlation_matrix.columns,
                                y=correlation_matrix.index))
fig.update_layout(title='Тепловая карта корреляций числовых переменных')
st.plotly_chart(fig)