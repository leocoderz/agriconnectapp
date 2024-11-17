import streamlit as st
import requests
import matplotlib.pyplot as plt

# Function to fetch weather information
def fetch_weather(city):
    api_key = "6e865750f0934069aa674739240104"  # Replace with your actual API key
    base_url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}&days=1&aqi=yes&alerts=no"

    response = requests.get(base_url)
    if response.status_code == 200:
        return response.json()
    return None

# Function to create hourly temperature distribution bar chart
def create_temperature_bar_chart(weather_data):
    if weather_data:
        hourly_data = weather_data['forecast']['forecastday'][0]['hour']
        temperatures = [data['temp_c'] for data in hourly_data]
        hours = range(24)

        fig, ax = plt.subplots(figsize=(5, 3))  # Smaller figure size for mobile
        ax.bar(hours, temperatures, color='skyblue')
        ax.set_xlabel('Hour')
        ax.set_ylabel('Temp (°C)')
        ax.set_title('Hourly Temp Distribution')
        ax.set_xticks(hours[::3])  # Show fewer ticks for clarity
        ax.grid(True)
        st.pyplot(fig)

# Function to create humidity line chart
def create_humidity_line_chart(weather_data):
    if weather_data:
        hourly_data = weather_data['forecast']['forecastday'][0]['hour']
        humidity = [data['humidity'] for data in hourly_data]
        hours = range(24)

        fig, ax = plt.subplots(figsize=(5, 3))
        ax.plot(hours, humidity, marker='o', color='green', linestyle='-')
        ax.set_xlabel('Hour')
        ax.set_ylabel('Humidity (%)')
        ax.set_title('Hourly Humidity')
        ax.set_xticks(hours[::3])
        ax.grid(True)
        st.pyplot(fig)

# Function to create wind speed line chart
def create_wind_speed_line_chart(weather_data):
    if weather_data:
        hourly_data = weather_data['forecast']['forecastday'][0]['hour']
        wind_speed = [data['wind_kph'] for data in hourly_data]
        hours = range(24)

        fig, ax = plt.subplots(figsize=(5, 3))
        ax.plot(hours, wind_speed, marker='o', color='blue', linestyle='-')
        ax.set_xlabel('Hour')
        ax.set_ylabel('Wind Speed (km/h)')
        ax.set_title('Hourly Wind Speed')
        ax.set_xticks(hours[::3])
        ax.grid(True)
        st.pyplot(fig)

# Streamlit UI for mobile
def main():
    st.title("🌾 Agri Weather 🌦️")

    city = st.text_input("Enter city name:", "New York")

    if st.button("Get Weather", key="weather_button"):
        with st.spinner("Fetching data..."):
            weather_data = fetch_weather(city)
        
        if weather_data:
            st.subheader("Weather Details")
            st.markdown(
                f"""
                - 🌤️ **Condition:** {weather_data['current']['condition']['text']}
                - 🌡️ **Temperature:** {weather_data['current']['temp_c']}°C
                - 💧 **Humidity:** {weather_data['current']['humidity']}%
                - 💨 **Wind Speed:** {weather_data['current']['wind_kph']} km/h
                """
            )

            st.subheader("Charts")
            with st.expander("Temperature Distribution"):
                create_temperature_bar_chart(weather_data)
            with st.expander("Humidity Variation"):
                create_humidity_line_chart(weather_data)
            with st.expander("Wind Speed Variation"):
                create_wind_speed_line_chart(weather_data)
        else:
            st.error("Failed to fetch weather data. Please try again.")

if __name__ == "__main__":
    main()
