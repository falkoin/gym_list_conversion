from cmath import phase
import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np
import sqlite3

st.set_page_config(page_title="Trampoline Dashboard",
                   page_icon=":running:",
                   layout="wide")


# Defaults
hash_val = 'empty'
## SQLite Connection
connection = sqlite3.connect("trampoline.db")
cursor = connection.cursor()

df = pd.read_sql("SELECT * from ranklists", connection)
df['Event Name'] = df["Year"].astype(str) + " " + df["Event"]

## Sidebar
st.markdown("### Main Overview")

# Event

event_str = st.sidebar.selectbox(
     'Select Event:',
     (['All'] + df["Event Name"].unique().tolist())
    )

df_temp = df[df['Event Name']==event_str]
df_temp.reset_index(inplace=True)
# st.write(df_temp["Year"])
sql_str = ""

if event_str is 'All':
    sql_str = "SELECT * from ranklists"
else:
    sql_str = "SELECT * from ranklists where event=" + "'" + df_temp["Event"][0] + "' and year=" + "'" + df_temp["Year"][0].astype(str) + "'"
    # st.write(sql_str)

df_select = pd.read_sql(sql_str, connection)

# Gender

gender = st.sidebar.selectbox(
     'Select Gender:',
     (['All'] + df_select["Gender"].unique().tolist())
    )

if gender is 'All':
    sql_str = "SELECT * from " + "(" + sql_str + ")"
else:
    sql_str = "SELECT * from " + "(" + sql_str + ")" + "where gender=" + "'" + gender + "'"
    # st.write(sql_str)

df_select = pd.read_sql(sql_str, connection)

# Athlte

athlete = st.sidebar.selectbox(
     'Select Athlete:',
     (['All'] + df_select["Name"].unique().tolist())
    )

if athlete is 'All':
    sql_str = "SELECT * from " + "(" + sql_str + ")"
else:
    sql_str = "SELECT * from " + "(" + sql_str + ")" + "where name=" + "'" + athlete + "'"

df_select = pd.read_sql(sql_str, connection)
    
# df_select.droplevel("index")
df_select.drop(['index'], axis=1, inplace=True)
st.dataframe(df_select)

exercise = st.sidebar.selectbox(
     'Select Exercise:',
     (['All'] + [str(i) for i in np.arange(0, len(df_select))] )
    )
debug = st.sidebar.checkbox('Debug')
if exercise is not 'All':
    athlete_name = athlete.split()
    athlete_name = athlete_name[0].capitalize() + ' ' + athlete_name[1]
    phase_select = df_select["Phase"].loc[int(exercise)]
    routine_select = df_select["Routine"].loc[int(exercise)]

    sql_str = "SELECT * from '" + event_str.replace(" ", "_").lower() + "_" + gender.lower() + "' where name=" + "'" + athlete_name + "' and phase=" + "'" + phase_select + "' and Routine=" + "'" + routine_select + "'"
    # sql_str = 'SELECT * from "2021_world_championships_men"'

    if debug:
        st.write(sql_str)
    df_athlete = pd.read_sql(sql_str, connection)
    if debug:
        st.write(df_athlete)
    hash_val = df_athlete["Hash"].iloc[0]

    if hash_val is not '':
        sql_str = "SELECT * from '" + hash_val + "'"
        df_exercisedata = pd.read_sql(sql_str, connection)
        df_exercisedata = df_exercisedata.astype(float)
# st.write(df_exercisedata)

left_column, right_column = st.columns(2)


with left_column:
    if len(athlete) > 3:
        df_polar = pd.melt(df_select, id_vars=['Rank','Name','Event', 'Routine', 'Country', 'Pen.', 'Total', 'End', 'Phase', 'Qualified', 'Location', 'Year', 'Gender'], var_name='Rating').sort_values(['Rank', 'Name'])
        df_polar['Exercises'] = df_polar["Year"].astype(str) + " " + df_polar["Event"] + " " + df_polar["Phase"] + " " + df_polar["Routine"]

        fig = px.line_polar(
            
            df_polar,
            title=athlete,
            r="value",
            theta="Rating",
            line_close=True,
            color="Exercises",
            range_r = [0, 20]
            
        )
        st.plotly_chart(fig)
        # st.write(df_exercisedata)
        if hash_val is not '':
            if exercise is not 'All':
                bar_text = df_exercisedata["index"]+1
                fig3 = px.bar(
                    df_exercisedata,
                    x=bar_text,
                    y='T',
                    title='Time of Flight'
                    )
                fig3.update_xaxes(title_text='Jumps')
                fig3.update_yaxes(title_text='Time (s)')
                st.plotly_chart(fig3)
        

with right_column:
    if hash_val is not '':
        if exercise is not 'All':
            scatter_text = df_exercisedata["index"]+1
            fig2 = px.scatter(
                df_exercisedata,
                x='x',
                y='y',
                text=scatter_text,
                color='H',
                range_color=(0.7,1)
                )
            fig2.update_traces(textposition='bottom right')
            fig2.update_layout(
                xaxis_range=[-214, 214],
                yaxis_range=[-107, 107],
                xaxis_visible=False,
                xaxis_showticklabels=False,
                yaxis_visible=False,
                yaxis_showticklabels=False,
                coloraxis={"colorscale": [[0, "red"], [0.5, "yellow"], [1, "green"]]}
                )
            fig2.add_trace(
                    px.line(
                        x=[54, 54, -54, -54, 54],
                        y=[54, -54, -54, 54, 54],
                        color_discrete_sequence=['#7f7f7f']
                    ).data[0]
                )
            fig2.add_trace(
                    px.line(
                        x=[214, -214],
                        y=[54, 54],
                        color_discrete_sequence=['#7f7f7f']
                    ).data[0]
                ) 
            fig2.add_trace(
                    px.line(
                        x=[214, -214],
                        y=[-54, -54],
                        color_discrete_sequence=['#7f7f7f']
                    ).data[0]
                )
            fig2.add_trace(
                    px.line(
                        x=[-107.5, -107.5],
                        y=[-107, 107],
                        color_discrete_sequence=['#7f7f7f']
                    ).data[0]
                )      
            fig2.add_trace(
                    px.line(
                        x=[107.5, 107.5],
                        y=[-107, 107],
                        color_discrete_sequence=['#7f7f7f']
                    ).data[0]
                )
            fig2.add_trace(
                    px.line(
                        x=[-35, 35],
                        y=[0, 0],
                        color_discrete_sequence=['#7f7f7f']
                    ).data[0]
                )
            fig2.add_trace(
                    px.line(
                        x=[0, 0],
                        y=[-35, 35],
                        color_discrete_sequence=['#7f7f7f']
                    ).data[0]
                )
            st.plotly_chart(fig2)
    else:
        st.write('Exercise file not available')