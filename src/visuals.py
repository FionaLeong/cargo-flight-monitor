import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, date

# --------------------------------------------------------------------
# LOAD DATA
# --------------------------------------------------------------------
df_ports=pd.read_csv("/Users/fionaleong/HKIA_flight_monitor/data/online_ports.csv") #where do i get this....
df = pd.read_csv("/Users/fionaleong/HKIA_flight_monitor/data/HKIA_merged.csv", header=0)
df= pd.merge(df,df_ports, how='inner', left_on='port', right_on='ports')     #strictly consider online ports, flight routes that CX have 
print(df)
# Create numeric cancellation flag
df['is_cancelled'] = (df['status'].str.strip() == 'Cancelled').astype(int)
#df has flight_id, flight_no, airline, date, time, destination, status, status_code, flight_type. last_updated, is_cancelled

# --------------------------------------------------------------------
# STREAMLIT FRAMEWORK: PAGE CONFIG AND COMMON FILTERS   (current filtering affect every chart)
# get all the filtering options, then filter the df
# --------------------------------------------------------------------

st.title("HKIA Cargo Flight Cancellation Dashboard")
st.set_page_config(
    page_title="HKIA Cargo Departure Flight Dashboard",
    layout="wide"       #full screen width
)

# sidebar filters 
st.sidebar.header("Filters")

selected_type= st.sidebar.multiselect(
    "Select Flight Type(s):",
    options=sorted(df['flight_type'].unique()),
    default=sorted(df['flight_type'].unique())      #by default select everything
)

selected_airline= st.sidebar.multiselect(
    "Select Airline(s):",
    options=sorted(df['airline'].unique()),
    default=sorted(df['airline'].unique())      #by default select everything
)

selected_port= st.sidebar.multiselect(
    "Select Port(s):",
    options=sorted(df['port'].unique()),
    default=sorted(df['port'].unique())  #by default select everything
)

#filtering logic 
if not selected_type:
    st.sidebar.warning("Please select at least one flight type.")
    st.stop()
if not selected_airline and not selected_port:
    st.sidebar.warning("Please select at least one airline/port.")
    st.stop()
if not selected_port and selected_airline:
    df = df.loc[df['airline'].isin(selected_airline)]
if not selected_airline and selected_port:
    df = df.loc[df['port'].isin(selected_port)]
if selected_airline and selected_port:
    df = df.loc[df['airline'].isin(selected_airline) & df['port'].isin(selected_port)]
    if df.empty:
        st.sidebar.warning("No data available for the selected airline(s) and port(s). Please select different airline(s) or port(s).")
        st.stop()

df=df.loc[df['flight_type'].isin(selected_type)] #arrival/departure or both

st.caption('Competitor Analysis exclusive on CX online ports')
st.divider()

df['date']=pd.to_datetime(df['date'])   #get df ready for filtering by date

#pre processed grouped airline and destination to ignore future data
past_df = df[df['date']<pd.Timestamp.today()]  
grouped_airline= past_df    #exclude today + future data, hence consider historical records
grouped_port= past_df         #exclude today + future data, hence consider historical records

# --------------------------------------------------------------------
# 1. KPI: total flights and total cancellation
# --------------------------------------------------------------------
total_data=len(df)
total_cancelled=df['is_cancelled'].sum()
total_noncancelled=total_data-total_cancelled

# --------------------------------------------------------------------
# 2. KPI: showing top percentage/top count of the destination with the highest cancellation rate
# --------------------------------------------------------------------

#count flights in grouped by airline and cancelled or not
cancel_rate_airline = df.groupby(['airline', 'is_cancelled']).agg(
    count=('flight_id', 'count')
).reset_index()
cancel_rate_airline= cancel_rate_airline[cancel_rate_airline['is_cancelled']==1]
#count flights by airline
total_per_airline=df.groupby('airline')['flight_id'].count().reset_index(name='total_flights')
#merged
cancel_rate_airline=pd.merge(cancel_rate_airline, total_per_airline, on='airline', how='left') 

#count flights in grouped by origin/dest and cancelled or not
cancel_rate_port = df.groupby(['port', 'is_cancelled']).agg(
    count=('flight_id', 'count')
).reset_index()
cancel_rate_port= cancel_rate_port[cancel_rate_port['is_cancelled']==1]
#count flights by airline
total_per_port=df.groupby('port')['flight_id'].count().reset_index(name='total_flights')
#merged
cancel_rate_port=pd.merge(cancel_rate_port, total_per_port, on='port', how='left')
print(cancel_rate_port.head())


#cancellation % and count
cancel_rate_airline['cancel%'] = ((cancel_rate_airline['count'] / cancel_rate_airline['total_flights']) * 100).round(2)
top_airline_count= cancel_rate_airline.sort_values('count', ascending=False).iloc[0]
cancel_rate_airline=cancel_rate_airline[cancel_rate_airline['total_flights']>100]       #essentially only consider airlines with more than 100 flights, avoiding small sample size
top_airline_per = cancel_rate_airline.sort_values('cancel%', ascending=False).iloc[0]

#cancellation % and count
cancel_rate_port['cancel%'] = ((cancel_rate_port['count'] / cancel_rate_port['total_flights']) * 100).round(2)
top_port_count= cancel_rate_port.sort_values('count', ascending=False).iloc[0]
cancel_rate_port=cancel_rate_port[cancel_rate_port['total_flights']>100]       #essentially only consider airlines with more than 100 flights, avoiding small sample size
top_port_per = cancel_rate_port.sort_values('cancel%', ascending=False).iloc[0]

# --------------------------------------------------------------------
# 3. Stacked bar: cancellations seggregated by airline/ by destination 
# --------------------------------------------------------------------

grouped_airline = grouped_airline.groupby(['airline', 'is_cancelled']).agg(count=('flight_id','count')).reset_index()   #undo multilevelindex
grouped_airline['status_label'] = grouped_airline['is_cancelled'].map({1: 'Cancelled', 0: 'Flown'})

#get sorting based on the non-cancelled flights count
non_cancelled_airline = grouped_airline[grouped_airline['is_cancelled'] == 0]
sorted_airlines = non_cancelled_airline.sort_values('count', ascending=True)['airline'].tolist()

fig1_airline = px.bar(
    grouped_airline,
    x='airline',
    y='count',
    color='status_label',
    title='Flight Cancellations by Airline',
    subtitle='Sorted by Non-Cancelled Flights',
    barmode='group',
    text='count',
    color_discrete_map={'Cancelled': 'red', 'Flown': 'green'},
    category_orders={'airline': sorted_airlines}  #airlined orders is based on the calculated sorted_airlines list
)
fig1_airline.update_traces(textposition='inside')
data_max_airline= grouped_airline['count'].max()  

grouped_port = grouped_port.groupby(['port', 'is_cancelled']).agg(count=('flight_id','count')).reset_index()
grouped_port['status_label'] = grouped_port['is_cancelled'].map({1: 'Cancelled', 0: 'Flown'})

non_cancelled_port = grouped_port[grouped_port['is_cancelled'] == 0]
sorted_port = non_cancelled_port.sort_values('count', ascending=True)['port'].tolist()

fig1_port = px.bar(
    grouped_port,
    x='port',
    y='count',
    color='status_label',
    title='Flight Cancellations by port',
    subtitle='Sorted by Non-Cancelled Flights',
    barmode='group',
    text='count',
    color_discrete_map={'Cancelled': 'red', 'Flown': 'green'},
    category_orders={'port': sorted_port}  #airlined orders is based on the calculated sorted_airlines list
)
fig1_port.update_traces(textposition='inside')
data_max_port= grouped_port['count'].max()  


# --------------------------------------------------------------------
# 4. RANKING CHART: top 5 highest cancellation rate: by airline/by destination
# --------------------------------------------------------------------

top_airline_per_5= cancel_rate_airline.sort_values('cancel%', ascending=False).head(5)
top_port_per_5= cancel_rate_port.sort_values('cancel%', ascending=False).head(5)
top_airline_count_5= cancel_rate_airline.sort_values('count', ascending=False).head(5)
top_port_count_5= cancel_rate_port.sort_values('count', ascending=False).head(5)


# --------------------------------------------------------------------
# STREAMLIT FRAMEWORK: PAGE LAYOUT
# --------------------------------------------------------------------

a,b,c= st.columns(3)
a.metric("Total Flights", f"{total_data:,}", border=True)
b.metric("Cancelled Flights", f"{total_cancelled:,}", border= True)
c.metric("Active Flights", f"{total_noncancelled:,}",  border=True)

st.subheader("Historical flight cancellation analysis")
csv_past= past_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download Historical Data as CSV",
    data=csv_past,
    file_name=f"HKIA_flight_data_{date.today()}.csv",
    mime='text/csv',
)

#change later: destination based or airline based
with st.container(border=True):
    st.caption("cancellation KPI consider combined flights >100")
    selected_dim= st.selectbox("Select Dimension for Top Cancellation Rate", options=['Airline', 'Port'], key='selected_dim')
    col1, col2= st.columns(2)
    if selected_dim=='Airline':
        top_per=top_airline_per
        top_count=top_airline_count
        top_per_5=top_airline_per_5
        top_count_5=top_airline_count_5
    else:
        top_per=top_port_per
        top_count=top_port_count
        top_per_5=top_port_per_5
        top_count_5=top_port_count_5

    with col1:
        st.metric(
            label=f"Highest Cancellation Rate: ",
            value=f"{top_per['airline' if selected_dim=='Airline' else 'port']} with {top_per['cancel%']} %",
            border=True
        )

    with col2:
        st.metric(
            label=f"Most Cancelled Flights: ",
            value=f"{top_count['airline' if selected_dim=='Airline' else 'port']} with {int(top_count['count'])}",
            border=True
    )
    
    col3, col4= st.columns(2)
    with col3:
        st.dataframe(top_per_5[['airline' if selected_dim=='Airline' else 'port','cancel%']], use_container_width=True)
    with col4:
        st.dataframe(top_count_5[['airline' if selected_dim=='Airline' else 'port','count']], use_container_width=True)


tab1, tab2= st.tabs(['Airline','Port'])
with tab1:
    fig1_airline.update_xaxes(rangeslider_visible=True, rangeslider_thickness=0.05)
    fig1_airline.update_yaxes(range=[0, data_max_airline * 1.1])  # give a little headroom
    st.plotly_chart(fig1_airline, use_container_width=True)

with tab2:
    fig1_port.update_xaxes(rangeslider_visible=True, rangeslider_thickness=0.05)
    fig1_port.update_yaxes(range=[0, data_max_port * 1.1])  # give a little headroom
    st.plotly_chart(fig1_port, use_container_width=True)

st.divider()
st.subheader("Today + Future flight cancellation analysis")

print(pd.Timestamp.today())
future_df = df[df['date']>=pd.Timestamp.today().normalize()]  #include today but why is it not including
future_df['date'] = future_df['date'].dt.date
csv_future= future_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download Future Data as CSV",
    data=csv_future,
    file_name=f"HKIA_future_flight_data_{date.today()}.csv",
    mime='text/csv',
)
future_df['is_cancelled']=future_df['is_cancelled'].map({1: 'Cancelled', 0: 'Scheduled'})
selected_status= st.selectbox("Status", options= future_df['is_cancelled'].unique().tolist() )
future_df=future_df[future_df['is_cancelled']==selected_status]
st.dataframe(future_df.drop(columns=[ 'ports', 'status_code']), use_container_width =True)
