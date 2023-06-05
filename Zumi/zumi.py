import streamlit as st
import pandas as pd 
import numpy as np 
import plotly.express as px 
import plotly.graph_objects as go
st.set_page_config(layout='wide')
# from streamlit_card import card
from st_card_component import card_component as card
from streamlit_option_menu import option_menu


def main():
    st.title("Zumi BI Assesment")

    with st.sidebar:
        selected = option_menu(
            menu_title=None,
            options=["Data 1","Data 2", "Data 3"],
            styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "icon": {"color": "orange", "font-size": "25px"},
                "nav-link": {
                    "font-size": "25px",
                    "text-align": "left",
                    "color": "black",
                    "margin": "0px",
                    "--hover-color": "#eee",
                },
                "nav-link-selected": {"background-color": "green"},
            },
        )
    if selected == "Data 1":
        st.subheader("Academy Awards Dataset")
        st.cache()
        def load_data():
            df = pd.read_csv("full_data1.csv")
            return df
            # df.index.name = "Date"
            # print(df.index.name)
        df = load_data()
        st.write(df)

        # list of years 
        year_list = df["Year"].to_list()
        year_list1 = [int(x) for x in year_list]
        year_list2 = set(year_list1)
        selected_years = st.multiselect("Select at least 1 Year", year_list2, [2015, 2014, 2013, 2012, 2011])

        award_list = ["Actor", "Actress", 'Actress in a Leading Role', 'Actress in a Supporting Role', 'Actor in a Leading Role', 'Actor in a Supporting Role']

        def new_df():
            new_dt = df[df.Award.isin(award_list)]
            new_dt["Nominated"] = new_dt["Award"].replace([np.nan, 1], ['failed', 'win'])
            new_dt = new_dt[new_dt["Year"].isin(selected_years)]
            d = pd.pivot_table(
            new_dt,
            index=['Name'],
            aggfunc={'Winner': np.sum, 'Film': len, 'Nominated':len}
            ).rename(columns={'Winner': 'Number of Awards Won', "Film": "Number of Films Featured", 'Nominated':"Number of Award nominations"}).reset_index()
            d = d.nlargest(n=10, columns=['Number of Awards Won', 'Number of Films Featured'])
            st.write("Top 10 Actors and Actress based on the Years Selected")
            st.write(d)
        new_df()


    if selected == "Data 2":
        st.subheader("Highest Hollywood Grossing Movies Dataset")
        st.cache()
        def load_data():
            df = pd.read_csv("Highest hollywood grossing movies.csv")
            return df
            # df.index.name = "Date"
            # print(df.index.name)
        df = load_data()
        st.write(df)

        year_list = df["Release Year"].to_list()
        year_list2 = set(year_list)
        selected_year = st.selectbox("Select Year", year_list2)
        def new_df():
            new_df_ = df[df["Release Year"]==selected_year]
            new_df_ = new_df_.groupby('Genre')[[' World Sales (in $) ']].sum().reset_index()
            new_df_ = new_df_.nlargest(n=10, columns = ' World Sales (in $) ')
            new_df_ = new_df_.sort_values(ascending=True, by=' World Sales (in $) ')
            return new_df_
        new_df_ = new_df()
        

        def visualization():
            
            fig = px.bar(data_frame= new_df_, x=' World Sales (in $) ', y="Genre", orientation='h', template='ggplot2')
            fig.update_traces(textposition = "outside")
            fig.update_layout(title = "Total World Sales in Release Year "+str(selected_year), title_x=0.5)
            st.plotly_chart(fig, use_container_width=True)
        visualization()

        def visualization1():
            
            new_df_ = df[df["Release Year"]==selected_year]
            new_df_ = new_df_.groupby('Distributor')[[' World Sales (in $) ']].sum().reset_index()
            new_df_ = new_df_.nlargest(n=10, columns = ' World Sales (in $) ')
            new_df_ = new_df_.sort_values(ascending=True, by=' World Sales (in $) ')

            fig = px.bar(data_frame= new_df_, x=' World Sales (in $) ', y="Distributor", orientation='h')
            fig.update_traces(textposition = "outside")
            fig.update_layout(title = "Total World Sales in Release Year "+str(selected_year), title_x=0.5)
            st.plotly_chart(fig, use_container_width=True)
        visualization1()

        distributor_list = ['All', 'Roadside Attractions',
            'Fox Searchlight Pictures',
            'New Line Cinema',
            'Focus Features',
            'United Artists Releasing',
            'Screen Gems',
            '20th Century Studios',
            'Metro-Goldwyn-Mayer (MGM)',
            'Paramount Pictures',
            'Dimension Films',
            'Revolution Studios',
            'Lionsgate',
            'Relativity Media',
            'Warner Bros.',
            'Universal Pictures',
            'DreamWorks',
            'DreamWorks Distribution',
            'Twentieth Century Fox',
            'Sony Pictures Classics',
            'United Artists',
            'IFC Films',
            'FilmDistrict',
            'Newmarket Films',
            'The Weinstein Company',
            'Sony Pictures Entertainment (SPE)',
            'USA Films',
            'Artisan Entertainment',
            'Walt Disney Studios Motion Pictures',
            'Summit Entertainment',
            'Miramax',
            'Columbia Pictures',
            'TriStar Pictures',
            'STX Entertainment',
            'Orion Pictures']

        def dist_selector():
            
            selected_distributor = st.selectbox("Select Distributor", distributor_list)
            if selected_distributor == "All":
                df1 = df
            else:
                df1 = df[df['Distributor']==selected_distributor]
            return df1
        df1 = dist_selector()

        def plot_raw_data():

            lin_df = df1.groupby('Release Year')[[' World Sales (in $) ']].mean().reset_index()
            fig = go.Figure()
            fig.add_trace(go.Scatter(
            name="Average World Sales for Movies",
            x=lin_df['Release Year'], 
            y=lin_df[' World Sales (in $) '],
            showlegend=True,
            line=dict(color='rgb(31, 119, 180)')))

            fig.layout.update(xaxis_rangeslider_visible=True,
            xaxis_title="Year", yaxis_title="Median World Sales", hovermode='x')
            fig.update_layout(title = "Mean Movie Sales over years for ", title_x=0.5)
            st.plotly_chart(fig, use_container_width=True)
        plot_raw_data()


    if selected == "Data 3":
        st.subheader("Netflix Titles Dataset")
        st.cache()
        def load_data():
            df = pd.read_csv("Netflix.csv")
            return df
            # df.index.name = "Date"
            # print(df.index.name)
        df = load_data()
        st.write(df)

        def plot_raw_data():
            lin_df = df.groupby('release_year')[['show_id']].count().reset_index()
            fig = go.Figure()
            fig.add_trace(go.Scatter(
            name="Trend of Movie and TV Shows Release",
            x=lin_df['release_year'], 
            y=lin_df['show_id'],
            showlegend=True,
            line=dict(color='rgb(31, 119, 180)')))

            fig.layout.update(xaxis_rangeslider_visible=True,
            xaxis_title="Year", yaxis_title="Number of Movie Released", hovermode='x')
            fig.update_layout(title = "Number of Netflix Released Movies and TVs over years", title_x=0.5)
            st.plotly_chart(fig, use_container_width=True)
        plot_raw_data()

        col1, col2 = st.columns(2)
        with col1:
            def donut():
                type_dist = df.groupby('type')[['show_id']].count().reset_index()
                fig = px.pie(type_dist, values='show_id', names='type', title='Distribution of Type', hole=0.5, template='ggplot2', labels={'show_id':'Total Count'})
                fig.update_traces(textinfo = 'percent + value', textfont_size=15)
                fig.update_layout(title_text = "Distribution of Category Type", title_x = 0.7)
                fig.update_layout(legend = dict(
                                    orientation = 'h', 
                                    yanchor = 'bottom', 
                                    y = -0.1, 
                                    xanchor = 'center', 
                                    x = 0.5
                                ))
                st.plotly_chart(fig, use_container_width=True)
            donut()

        with col2:
            def rating():
                rating_df = df.groupby('rating')[['show_id']].count().reset_index()
                rating_df = rating_df.nlargest(18, columns='show_id')
                fig = px.bar(data_frame=rating_df, x='rating', y="show_id", orientation='v', 
                labels={'show_id': 'Number of Movies and TVs Rated', 'rating':'Rating Type'})
                fig.update_traces(textposition = "outside")
                fig.update_layout(title = "Rating Distribution", title_x=0.5)
                st.plotly_chart(fig, use_container_width=True)
            rating()
        def country():
                country_df = df.groupby('country')[['show_id']].count().reset_index()
                country_df = country_df.nlargest(10, columns='show_id')
                country_df = country_df.sort_values(by='show_id')
                fig = px.bar(data_frame=country_df, y='country', x="show_id", orientation='h', 
                labels={'show_id': 'Number of Movies and TVs Produced', 'country':'Production Country'})
                fig.update_traces(textposition = "outside")
                fig.update_layout(title = "Top 10 Producing Countries on Netflix", title_x=0.5)
                st.plotly_chart(fig, use_container_width=True)
        country()
        def genre():
                genre_df = df.groupby('listed_in')[['show_id']].count().reset_index()
                genre_df = genre_df.nlargest(10, columns='show_id')
                genre_df = genre_df.sort_values(by='show_id')
                fig = px.bar(data_frame=genre_df, y='listed_in', x="show_id", orientation='h', template="ggplot2",
                labels={'show_id': 'Number of Movies and TVs Produced', 'listed_in':'Genre Category'})
                fig.update_traces(textposition = "outside")
                fig.update_layout(title = "Top 10 Movie and TV Show Genres on Netflix", title_x=0.5)
                st.plotly_chart(fig, use_container_width=True)
        genre()

        def top_directors():
            director = df.groupby('director')[['show_id']].count().reset_index()
            director = director[director['director'] != 'Not Indicated']
            director = director.nlargest(10, columns='show_id')
            director = director.sort_values(by='show_id')
            fig = px.bar(data_frame=director, y='director', x="show_id", orientation='h', template="seaborn",
            labels={'show_id': 'Number of Movies or TVs Directed', 'director':'Director'})
            fig.update_traces(textposition = "outside")
            fig.update_layout(title = "Top 10 Directors on Netflix", title_x=0.5)
            st.plotly_chart(fig, use_container_width=True)
        top_directors()
            



if __name__ == "__main__":
    main()
