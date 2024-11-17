import streamlit as st
import pandas as pd
import folium
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_folium import st_folium

APP_TITLE = "Agriculture Crop Production in India"
APP_SUB_TITLE = "Source: Ministry of Agriculture and Farmers Welfare of India"


def display_insights(df, crop):
    st.subheader(f"Insights about {crop} Production")

    # Crop with highest production in each state
    max_production_crop = df[df["Crop"] == crop].groupby("State")["Production"].idxmax()
    max_production_info = df.loc[max_production_crop, ["State", "Crop", "Production"]]
    st.write("Crop with Highest Production in Each State:")
    st.write(max_production_info)

    # Best season for the selected crop in each state
    df_crop_state = df[(df["Crop"] == crop) & (df["Production"] > 0)]
    if not df_crop_state.empty:
        best_season = (
            df_crop_state.groupby(["State", "Season"])["Yield"].mean().idxmax()
        )
        st.write("Best Season for the Selected Crop in Each State:")
        st.write(best_season)
    else:
        st.write(
            "No data available to determine the best season for the selected crop."
        )


def display_map(df, year, crop, season):
    df = df[(df["Year"] == year) & (df["Season"] == season) & (df["Crop"] == crop)]

    map = folium.Map(
        location=[20, 80], zoom_start=4, scrollWheelZoom=False, tiles="CartoDB positron"
    )

    choropleth = folium.Choropleth(
        geo_data="data/states_india.geojson",
        data=df,
        columns=("State", "Yield"),
        key_on="feature.properties.st_nm",
        fill_color="YlGn",
        fill_opacity=0.7,
        line_opacity=0.8,
        highlight=True,
    )
    choropleth.geojson.add_to(map)

    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(["st_nm"], labels=False)
    )

    st_map = st_folium(map, width=700, height=400)

    state = ""
    if st_map["last_active_drawing"]:
        state = st_map["last_active_drawing"]["properties"]["st_nm"]

    return state


def display_time_filters(df):
    year_list = [""] + list(df["Year"].unique())
    year_list.sort(reverse=True)
    year = st.sidebar.selectbox("Year", year_list)
    season_list = [""] + list(df["Season"].unique())
    season = st.sidebar.selectbox("Season", season_list)
    st.header(f"{year} {season}")
    return year, season


def crop_filter(df):
    crop_list = [""] + list(df["Crop"].unique())
    crop_list.sort()
    return st.sidebar.selectbox("Crop", crop_list)


def display_state_filter(df, state):
    state_list = [""] + list(df["State"].unique())
    state_list.sort()
    state_index = state_list.index(state) if state and state in state_list else 0
    return st.sidebar.selectbox("State", state_list, state_index)


def main():
    st.title(APP_TITLE)
    st.caption(APP_SUB_TITLE)

    # LOAD DATA
    df_country = pd.read_csv("data/India Agriculture Crop Production.csv")

    # DISPLAY FILTERS AND MAP
    year, season = display_time_filters(df_country)
    state = display_map(df_country, year, "Rice", season)
    crop = crop_filter(df_country)
    state = display_state_filter(df_country, state)

    # DISPLAY INSIGHTS
    display_insights(df_country, crop)

    # PRODUCTION DISTRIBUTION (PIE CHART)
    st.subheader("Production Distribution")
    production_data = (
        df_country[df_country["Crop"] == crop]
        .groupby("State")["Production"]
        .sum()
        .reset_index()
    )
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(
        production_data["Production"],
        labels=production_data["State"],
        autopct="%1.1f%%",
    )
    st.pyplot(fig)

    # YIELD COMPARISON (BAR GRAPH)
    st.subheader("Yield Comparison")
    yield_data = (
        df_country[df_country["Crop"] == crop]
        .groupby("State")["Yield"]
        .sum()
        .reset_index()
    )
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(8, 5))
    sns.barplot(x="Yield", y="State", data=yield_data, palette="viridis")
    st.pyplot(plt)


if __name__ == "__main__":
    main()
