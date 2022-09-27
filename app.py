from cmath import phase
import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np
import sqlite3
from scipy.spatial import ConvexHull

## Functions

def calcArea(x, y, in_hd):
    test_nan = np.sum(np.isnan(x))
    # print(test_nan)
    valid_values = len(x)-test_nan
    x = x[0:valid_values]
    y = y[0:valid_values]
    in_hd = (in_hd/10) * valid_values
    
    m = 35
    n = 35
    x_min = np.array([-m, m, -m, m, -m, m, -m, m, -m, m])
    y_min = np.array([-n, -n, n, n, -n, -n, n, n, -n, -n])
    hull_min = ConvexHull(np.column_stack((x_min, y_min)))
    a = 214
    b = 107
    x_max = np.array([-a, a, -a, a, -a, a, -a, a, -a, a])
    y_max = np.array([-b, -b, b, b, -b, -b, b, b, -b, -b])
    hull_max = ConvexHull(np.column_stack((x_max, y_max)))

    hd_max = in_hd
    slices = valid_values+1
    hd_range = np.linspace(0, hd_max, slices)
    # hd_range = np.append(hd_range, 5)
    area_range = np.linspace(hull_min.volume, hull_max.volume, 10)
    # print(hd_range)
    # print(area_range)
    if test_nan < 8:
        in_area = ConvexHull(np.hstack((x,y))).volume
        below_range = np.sum(in_area >= area_range)
        # print(np.sum(in_area > area_range))
        return(len(x)-hd_range[below_range])
    else:
        return(len(x))


def calcDistance(x, y, in_hd):
    test_nan = np.sum(np.isnan(x))
    # print(test_nan)
    valid_values = len(x)-test_nan
    x = x[0:valid_values]
    y = y[0:valid_values]
    in_hd = (in_hd/10) * valid_values

    in_distance = np.sum(np.sqrt(x**2+y**2))
    m = 35
    n = 35
    x_min = np.array([-m, m, -m, m, 0, m, 0, m, 0, 0])
    y_min = np.array([-n, -n, 0, 0, -n, -n, n, n, 0, 0])
    optimum_distance = np.sum(np.sqrt(x_min**2+y_min**2)) 

    a = 214
    b = 107
    x_max = np.array([-a, a, -a, a, -107.5, 107.5, -107.5, 107.5, -a, a])
    y_max = np.array([-b, -b, b, b, -b, -b, b, b, 0, 0])
    worst_distance = np.sum(np.sqrt(x_max**2+y_max**2))

    hd_max = in_hd
    slices = valid_values+1
    hd_range = np.linspace(0, hd_max, slices)
    # hd_range = np.append(hd_range, 5)
    area_range = np.linspace(optimum_distance, worst_distance, 10)
    # print(hd_range)
    # print(area_range)

    below_range = np.sum(in_distance >= area_range)
    # print(np.sum(in_area > area_range))
    return(len(x)-hd_range[below_range])

def calcError(x, y, in_hd):
    test_nan = np.sum(np.isnan(x))
    # print(test_nan)
    valid_values = len(x)-test_nan
    x = x[0:valid_values]
    y = y[0:valid_values]
    in_hd = (in_hd/10) * valid_values

    distance = np.sqrt(x**2+2*y**2)
    mean_distance = np.mean(distance)
    ce = np.sum(distance)/len(x)
    ve = np.sqrt(np.sum((distance - mean_distance)**2/len(x)))
    current_error = ce + ve
    # print(current_error)
    m = 35
    n = 35
    x_min = np.array([-m, m, -m, m, 0, m, 0, m, 0, 0])
    y_min = np.array([-n, -n, 0, 0, -n, -n, n, n, 0, 0])

    distance = np.sqrt(x_min**2+2*y_min**2)
    mean_distance = np.mean(distance)
    ce = np.sum(distance)/len(x_min)
    ve = np.sqrt(np.sum((distance - mean_distance)**2/len(x_min)))
    optimum_error = ce + ve

    a = 214
    b = 107
    x_max = np.array([-a, a, -a, a, -107.5, 107.5, -107.5, 107.5, -a, a])
    y_max = np.array([-b, -b, b, b, -b, -b, b, b, 0, 0])

    distance = np.sqrt(x_max**2+2*y_max**2)
    mean_distance = np.mean(distance)
    ce = np.sum(distance)/len(x_max)
    ve = np.sqrt(np.sum((distance - mean_distance)**2/len(x_max)))
    worst_error = ce + ve

    hd_max = in_hd
    slices = int(round(in_hd/0.05) + 1)
    hd_range = np.linspace(0, hd_max, slices)
    # hd_range = np.append(hd_range, 5)
    area_range = np.linspace(optimum_error, worst_error, slices-1)
    # print(hd_range)
    # print(area_range)

    below_range = np.sum(current_error >= area_range)
    # print(np.sum(in_area > area_range))
    return(len(x)-hd_range[below_range])

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
        x = df_exercisedata[['x']].values
        y = df_exercisedata[['y']].values
        # hull
        hd_hull3 = calcArea(x, y, in_hd=3)
        hd_hull5 = calcArea(x, y, in_hd=5)
        # distance
        hd_distance3 = calcDistance(x, y, 3)
        hd_distance5 = calcDistance(x, y, 5)
        # error
        hd_error3 = calcError(x, y, 3)
        hd_error5 = calcError(x, y, 5)

        hd_title = 'HD: {0}  HD_H: {1}|{2}  HD_D: {3}|{4}  HD_E: {5}|{6}'.format(
            df_select["H"].loc[int(exercise)],
            hd_hull3,
            hd_hull5,
            hd_distance3,
            hd_distance5,
            hd_error3,
            hd_error5
            )
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
            # st.write('HD:')
            scatter_text = df_exercisedata["index"]+1
            fig2 = px.scatter(
                df_exercisedata,
                x='x',
                y='y',
                text=scatter_text,
                color='H',
                range_color=(0.7,1),
                title=hd_title
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
        
st.sidebar.write('HD Analysis')

phase = st.sidebar.selectbox(
     'Select Phase:',
     (df_select["Phase"].unique().tolist() )
    )

sql_str = "SELECT * from " + "(" + sql_str + ")" + "where Phase=" + "'" + phase + "'"

df_ranking = pd.read_sql(sql_str, connection)
rating_str = ("H3 Original", "H3 Distance", "H5 Distance", "H3 Error", "H5 Error", "H3 Hull", "H5 Hull")
rating = st.sidebar.selectbox(
     'Select Rating:',
     (rating_str )
    )


df_event = df_ranking.reset_index()
sumlist = ("H3 Distance", "H5 Distance", "H3 Error", "H5 Error", "H3 Hull", "H5 Hull")
hd_distance3_list = []
hd_distance5_list = []
hd_error3_list = []
hd_error5_list = []
hd_hull3_list = []
hd_hull5_list = []
for idx, row in df_event.iterrows():
    gender = row['Gender']
    athlete = row['Name']
    athlete_name = athlete.split()
    athlete_name = athlete_name[0].capitalize() + ' ' + athlete_name[1]
    if row['Routine'] == '1st':
        exercise = 0
    elif row['Routine'] == '2nd':
        exercise = 1
    phase_select = df_event["Phase"].iloc[int(exercise)]
    routine_select = df_event["Routine"].iloc[int(exercise)]
    sql_str = "SELECT * from '" + event_str.replace(" ", "_").lower() + "_" + gender.lower() + "' where name=" + "'" + athlete_name + "' and phase=" + "'" + phase_select + "' and Routine=" + "'" + routine_select + "'"
    df_athlete = pd.read_sql(sql_str, connection)
    if len(df_athlete) > 0:
        hash_val = df_athlete["Hash"].iloc[0]

        if hash_val is not '':
            sql_str = "SELECT * from '" + hash_val + "'"
            df_exercisedata = pd.read_sql(sql_str, connection)
            df_exercisedata = df_exercisedata.astype(float)
            x = df_exercisedata[['x']].values
            y = df_exercisedata[['y']].values
            # hull
            hd_hull3 = calcArea(x, y, in_hd=3)
            hd_hull5 = calcArea(x, y, in_hd=5)
            hd_hull3_list.append(hd_hull3)
            hd_hull5_list.append(hd_hull5)
            # distance
            hd_distance3 = calcDistance(x, y, 3)
            hd_distance3_list.append(hd_distance3)
            hd_distance5 = calcDistance(x, y, 5)
            hd_distance5_list.append(hd_distance5)

            # error
            hd_error3 = calcError(x, y, 3)
            hd_error5 = calcError(x, y, 5)
            hd_error3_list.append(hd_error3)
            hd_error5_list.append(hd_error5)
        else:
            hd_hull3_list.append(0)
            hd_hull5_list.append(0)
            hd_distance3_list.append(0)
            hd_distance5_list.append(0)
            hd_error3_list.append(0)
            hd_error5_list.append(0)
    else:
        hd_hull3_list.append(0)
        hd_hull5_list.append(0)
        hd_distance3_list.append(0)
        hd_distance5_list.append(0)
        hd_error3_list.append(0)
        hd_error5_list.append(0)

if rating == "H3 Distance":
    df_event["H3 Distance"] = hd_distance3_list
if rating == "H5 Distance":
    df_event["H5 Distance"] = hd_distance5_list
if rating == "H3 Error":
    df_event["H3 Error"] = hd_error3_list
if rating == "H5 Error":
    df_event["H5 Error"] = hd_error5_list
if rating == "H3 Hull":
    df_event["H3 Hull"] = hd_hull3_list
if rating == "H5 Hull":
    df_event["H5 Hull"] = hd_hull5_list


if rating != "H3 Original":
    entry = rating
        # print(entry)
    df_event['Sum ' + entry] = df_event['D'] + df_event['T'] + df_event['E'] + df_event[entry]
        # df_event
    rankchange_list = []
    meanchange_list = []
    entry_full = 'Sum ' + entry
    idx_list = []
    for idx2, row2 in df_event.iterrows():
        if idx2 > 0:
            if row2[entry] == 0.0:
                    # print("Dropped because no file")
                    idx_list.append(idx2)
            else:
                if phase == "Qualification":
                    if (row2["Routine"] == '2nd') and df_event.iloc[idx2-1]["Routine"] == '1st':
                        if (row2[entry] > df_event.iloc[idx-1][entry]):
                            idx_list.append(idx2-1)
                        else:
                            idx_list.append(idx2)

    df_result = df_event.drop(idx_list, axis=0)
    df_result = df_result.sort_values(by=[entry_full], ascending=False)
    new_rank = df_result["Rank"]
    df_result['New Rank'] = np.sort(new_rank)
    rank_change_unsigned = df_result['New Rank']-df_result['Rank']
    rank_change_unsigned_str = [str(-i) if i >= 0 else "+"+str(-i) for i in rank_change_unsigned]
    rank_change = np.abs(rank_change_unsigned)
    rankchange_list.append(np.sum(rank_change!=0))
    meanchange_list.append(np.mean(rank_change))
    df_result["Rankchange"] = rank_change_unsigned_str
else:
    df_result = df_event
    df_result['Rank'] = np.arange(1, len(df_result)+1)

df_result = df_result.drop(["Event", "Phase", "Year", "Location", "Year", "level_0", "index", "Gender", "Routine", "Rank", "Qualified"], axis=1)
st.markdown("### Rank Analysis")
st.write(df_result)