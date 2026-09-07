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
df= pd.merge(df,df_ports, how='inner', left_on='destination', right_on='ports')     #strictly consider online ports, flight routes that CX have 
print(df)
# Create numeric cancellation flag
df['is_cancelled'] = (df['status'].str.strip() == 'Cancelled').astype(int)
#df has flight_id, flight_no, airline, date, time, destination, status, status_code, flight_type. last_updated, is_cancelled

# --------------------------------------------------------------------
# STREAMLIT FRAMEWORK: PAGE CONFIG AND COMMON FILTERS   (current filtering affect every chart)
# get all the filtering options, then filter the df
# --------------------------------------------------------------------

st.title("Flight Cancellation Dashboard")
st.divider()
st.set_page_config(
    page_title="HKIA Cargo Departure Flight Dashboard",
    layout="wide"       #full screen width
)

# sidebar filters 
st.sidebar.header("Filters")

selected_airline= st.sidebar.multiselect(
    "Select Airline(s):",
    options=sorted(df['airline'].unique()),
    default=sorted(df['airline'].unique())      #by default select everything
)

selected_destination= st.sidebar.multiselect(
    "Select Destination(s):",
    options=sorted(df['destination'].unique()),
    default=sorted(df['destination'].unique())  #by default select everything
)

#filtering logic 
if not selected_airline and not selected_destination:
    st.sidebar.warning("Please select at least one airline/destination.")
    st.stop()
if not selected_destination and selected_airline:
    df = df.loc[df['airline'].isin(selected_airline)]
if not selected_airline and selected_destination:
    df = df.loc[df['destination'].isin(selected_destination)]
if selected_airline and selected_destination:
    df = df.loc[df['airline'].isin(selected_airline) & df['destination'].isin(selected_destination)]
    if df.empty:
        st.sidebar.warning("No data available for the selected airline(s) and destination(s). Please select different airline(s) or destination(s).")
        st.stop()


df['date']=pd.to_datetime(df['date'])   #get df ready for filtering by date

#pre processed grouped airline and destination to ignore future data
past_df = df[df['date']<pd.Timestamp.today()]  
grouped_airline= past_df    #exclude today + future data, hence consider historical records
grouped_dest= past_df         #exclude today + future data, hence consider historical records

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

#count flights in grouped by destination and cancelled or not
cancel_rate_dest = df.groupby(['destination', 'is_cancelled']).agg(
    count=('flight_id', 'count')
).reset_index()
cancel_rate_dest= cancel_rate_dest[cancel_rate_dest['is_cancelled']==1]
#count flights by airline
total_per_dest=df.groupby('destination')['flight_id'].count().reset_index(name='total_flights')
#merged
cancel_rate_dest=pd.merge(cancel_rate_dest, total_per_dest, on='destination', how='left')
print(cancel_rate_dest.head())


#cancellation % and count
cancel_rate_airline['cancel%'] = ((cancel_rate_airline['count'] / cancel_rate_airline['total_flights']) * 100).round(2)
top_airline_count= cancel_rate_airline.sort_values('count', ascending=False).iloc[0]
cancel_rate_airline=cancel_rate_airline[cancel_rate_airline['total_flights']>100]       #essentially only consider airlines with more than 100 flights, avoiding small sample size
top_airline_per = cancel_rate_airline.sort_values('cancel%', ascending=False).iloc[0]

#cancellation % and count
cancel_rate_dest['cancel%'] = ((cancel_rate_dest['count'] / cancel_rate_dest['total_flights']) * 100).round(2)
top_dest_count= cancel_rate_dest.sort_values('count', ascending=False).iloc[0]
cancel_rate_dest=cancel_rate_dest[cancel_rate_dest['total_flights']>100]       #essentially only consider airlines with more than 100 flights, avoiding small sample size
top_dest_per = cancel_rate_dest.sort_values('cancel%', ascending=False).iloc[0]

# --------------------------------------------------------------------
# 3. Stacked bar: cancellations seggregated by airline/ by destination 
# --------------------------------------------------------------------

grouped_airline = grouped_airline.groupby(['airline', 'is_cancelled']).agg(count=('flight_id','count')).reset_index()   #undo multilevelindex
grouped_airline['status_label'] = grouped_airline['is_cancelled'].map({1: 'Cancelled', 0: 'Dep/Schd'})

#get sorting based on the non-cancelled flights count
non_cancelled_airline = grouped_airline[grouped_airline['is_cancelled'] == 0]
sorted_airlines = non_cancelled_airline.sort_values('count', ascending=True)['airline'].tolist()

fig1_airline = px.bar(
    grouped_airline,
    x='airline',
    y='count',
    color='status_label',
    title='Flight Cancellations by Airline',
    barmode='group',
    text='count',
    color_discrete_map={'Cancelled': 'red', 'Dep/Schd': 'green'},
    category_orders={'airline': sorted_airlines}  #airlined orders is based on the calculated sorted_airlines list
)
fig1_airline.update_traces(textposition='inside')
data_max_airline= grouped_airline['count'].max()  

grouped_dest = grouped_dest.groupby(['destination', 'is_cancelled']).agg(count=('flight_id','count')).reset_index()
grouped_dest['status_label'] = grouped_dest['is_cancelled'].map({1: 'Cancelled', 0: 'Dep/Schd'})

non_cancelled_dest = grouped_dest[grouped_dest['is_cancelled'] == 0]
sorted_dest = non_cancelled_dest.sort_values('count', ascending=True)['destination'].tolist()

fig1_dest = px.bar(
    grouped_dest,
    x='destination',
    y='count',
    color='status_label',
    title='Flight Cancellations by Destination',
    barmode='group',
    text='count',
    color_discrete_map={'Cancelled': 'red', 'Dep/Schd': 'green'},
    category_orders={'destination': sorted_dest}  #airlined orders is based on the calculated sorted_airlines list
)
fig1_dest.update_traces(textposition='inside')
data_max_dest= grouped_dest['count'].max()  


# --------------------------------------------------------------------
# 4. RANKING CHART: top 5 highest cancellation rate: by airline/by destination
# --------------------------------------------------------------------

top_airline_per_5= cancel_rate_airline.sort_values('cancel%', ascending=False).head(5)
top_destination_per_5= cancel_rate_dest.sort_values('cancel%', ascending=False).head(5)
top_airline_count_5= cancel_rate_airline.sort_values('count', ascending=False).head(5)
top_destination_count_5= cancel_rate_dest.sort_values('count', ascending=False).head(5)


# --------------------------------------------------------------------
# STREAMLIT FRAMEWORK: PAGE LAYOUT
# --------------------------------------------------------------------

st.subheader("Historical flight cancellation analysis")
csv_past= past_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download Historical Data as CSV",
    data=csv_past,
    file_name=f"HKIA_flight_data_{date.today()}.csv",
    mime='text/csv',
)
a,b,c= st.columns(3)
a.metric("Total Flights", f"{total_data:,}", border=True)
b.metric("Cancelled Flights", f"{total_cancelled:,}", border= True)
c.metric("Active Flights", f"{total_noncancelled:,}",  border=True)

#change later: destination based or airline based
with st.container(border=True):
    st.caption("cancellation KPI consider combined flights >100")
    selected_dim= st.selectbox("Select Dimension for Top Cancellation Rate", options=['Airline', 'Destination'], key='selected_dim')
    col1, col2= st.columns(2)
    if selected_dim=='Airline':
        top_per=top_airline_per
        top_count=top_airline_count
        top_per_5=top_airline_per_5
        top_count_5=top_airline_count_5
    else:
        top_per=top_dest_per
        top_count=top_dest_count
        top_per_5=top_destination_per_5
        top_count_5=top_destination_count_5

    with col1:
        st.metric(
            label=f"Highest Cancellation Rate: ",
            value=f"{top_per['airline' if selected_dim=='Airline' else 'destination']} with {top_per['cancel%']} %",
            border=True
        )

    with col2:
        st.metric(
            label=f"Most Cancelled Flights: ",
            value=f"{top_count['airline' if selected_dim=='Airline' else 'destination']} with {int(top_count['count'])}",
            border=True
    )
    
    col3, col4= st.columns(2)
    with col3:
        st.dataframe(top_per_5[['airline' if selected_dim=='Airline' else 'destination','cancel%']], use_container_width=True)
    with col4:
        st.dataframe(top_count_5[['airline' if selected_dim=='Airline' else 'destination','count']], use_container_width=True)


tab1, tab2= st.tabs(['Airline','Destination'])
with tab1:
    fig1_airline.update_xaxes(rangeslider_visible=True, rangeslider_thickness=0.05)
    fig1_airline.update_yaxes(range=[0, data_max_airline * 1.1])  # give a little headroom
    st.plotly_chart(fig1_airline, use_container_width=True)

with tab2:
    fig1_dest.update_xaxes(rangeslider_visible=True, rangeslider_thickness=0.05)
    fig1_dest.update_yaxes(range=[0, data_max_dest * 1.1])  # give a little headroom
    st.plotly_chart(fig1_dest, use_container_width=True)

st.divider()
st.subheader("Future flight cancellation analysis")

future_df = df[df['date']>pd.Timestamp.today()]  
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
