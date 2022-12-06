import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(layout="wide")

# -- Create three columns
col1, col2, col3 = st.columns([10, 25, 10])
# -- Put the image in the middle column
# - Commented out here so that the file will run without having the image downloaded
with col1:
    st.image("eventbrite.jpg", width=350)
# -- Put the title in the last column
with col2:
    st.title("Event Search Engine - CS 410 Final Project")
with col3:
    st.image("Twitter.jpg", width=350)
# -- Put the title in the last column

# -- Get the user input
query_col, city_col = st.columns([5, 5])

with city_col:
    city_choice = st.selectbox(
        "Which city are you looking at?",
        ("All", "champaign", "chicago", "seattle", "arlington"),
    )

with query_col:
    text_input = st.text_input(
        "Enter your query here 👇",
    )
    if text_input:
        st.write("You entered this query: ", text_input)
    #st.subheader("Look at the below table for the results of your query:")


# -- Read in the data
EB_df = pd.read_csv("EventBrite_data.csv", encoding='windows-1252')
# -- Apply the continent filter
if city_choice != "All":
    EB_df = EB_df[EB_df.city == city_choice]

ranked_table = st.container()
with ranked_table:
    st.title("Ranked List of Events:")
    table = go.Figure(data=go.Table(columnorder = [1,2,3,4,5,6], columnwidth = [10,50,40,40,50,40],
    header=dict(values=list(EB_df[['Rank','title','time','venue','URL','user']].columns), height=60,
    font=dict(color='black'), fill_color='#546e9c', align='center',line_color='black',font_size = 30), 
    cells=dict(values=[EB_df.Rank,EB_df.title,EB_df.time,EB_df.venue,EB_df.URL,EB_df.user],
    font=dict(color='black'), fill_color = "#8ca5d1", align='left',line_color='black',font_size = 20)))
    
    table.update_layout(width=1800, height=800)
    st.write(table)



# # -- Create the figure in Plotly
# fig = px.scatter(
#     filtered_df,
#     x="gdpPercap",
#     y="lifeExp",
#     size="pop",
#     color="continent",
#     hover_name="country",
#     size_max=60,
# )
# fig.update_layout(title="GDP per Capita vs. Life Expectancy")
# # -- Input the Plotly chart to the Streamlit interface
# st.plotly_chart(fig, use_container_width=True)