import streamlit as st
import google.generativeai as genai
import os
import numpy as np
import matplotlib.pyplot as plt

# Configure Gemini API key
os.environ['API_KEY'] = "AIzaSyDAQJROTnyvmCgiZfzFbkAnaVvOTN5OicI"
genai.configure(api_key=os.environ['API_KEY'])

# Define function to interact with Gemini AI
def gemini_ai(query):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(query)
    return response.text

# Function for soil data analysis and crop recommendation
def analyze_soil_data(N, P, K, temp, humidity, ph, rainfall):
    # Set limits for soil parameters
    N_limit, P_limit, K_limit, temp_limit, humidity_limit, ph_limit, rainfall_limit = 1000, 1000, 1000, 100, 100, 14, 1000

    # Display set values and check limits
    st.subheader("Soil Parameters:")
    st.markdown(f"""
    - **Nitrogen**: {N}/{N_limit}
    - **Phosphorus**: {P}/{P_limit}
    - **Potassium**: {K}/{K_limit}
    - **Temperature**: {temp}/{temp_limit}°C
    - **Humidity**: {humidity}/{humidity_limit}%
    - **pH**: {ph}/{ph_limit}
    - **Rainfall**: {rainfall}/{rainfall_limit} mm
    """)

    # Bar graph for soil nutrient distribution
    st.subheader("Nutrient Distribution")
    fig, ax = plt.subplots(figsize=(5, 3))
    nutrients = ['Nitrogen', 'Phosphorus', 'Potassium']
    values = [N, P, K]
    ax.bar(nutrients, values, color=['blue', 'green', 'orange'])
    ax.set_ylabel('Nutrient Level')
    ax.set_title('Soil Nutrient Levels')
    st.pyplot(fig)

    # Soil suitability for crop cultivation
    crop_suitability = {
        'Wheat': (N > 100) and (P > 50) and (K > 100),
        'Rice': (N > 200) and (P > 100) and (K > 150),
        'Corn': (N > 150) and (P > 80) and (K > 120)
    }

    suitable_crops = [crop for crop, suitability in crop_suitability.items() if suitability]
    st.subheader("Crop Recommendations")
    if suitable_crops:
        st.write("The soil is suitable for the following crops:")
        st.write(", ".join(suitable_crops))
    else:
        st.write("The soil may not be suitable for any specific crop.")

# Main function for the app
def main():
    # App title
    st.title("🌾 Agriculture Chatbot 🤖")
    st.markdown("Optimized for mobile devices 📱")

    # Sidebar for navigation
    st.sidebar.title("Navigation")
    query_type = st.sidebar.radio("Select Query Type", ["Chat", "Soil Analysis"])

    # Chat feature
    if query_type == "Chat":
        st.subheader("Chat with Gemini AI")
        queries = st.text_input("Type your farming question:")
        if st.button("Submit"):
            if queries.strip():
                response = gemini_ai(queries)
                st.markdown(f"**Gemini AI Response:** {response}")
            else:
                st.warning("Please enter a question.")

    # Soil analysis feature
    elif query_type == "Soil Analysis":
        st.subheader("Soil Analysis 🌱")
        
        # Input sliders for soil parameters
        st.markdown("### Enter Soil Parameters:")
        N = st.slider("Nitrogen (N)", 0, 1000, 500, step=10)
        P = st.slider("Phosphorus (P)", 0, 1000, 500, step=10)
        K = st.slider("Potassium (K)", 0, 1000, 500, step=10)
        temp = st.slider("Temperature (°C)", 0.0, 100.0, 25.0, step=0.5)
        humidity = st.slider("Humidity (%)", 0.0, 100.0, 50.0, step=1.0)
        ph = st.slider("pH Level", 0.0, 14.0, 7.0, step=0.1)
        rainfall = st.slider("Rainfall (mm)", 0.0, 1000.0, 500.0, step=10)

        # Analyze button
        if st.button("Analyze Soil"):
            analyze_soil_data(N, P, K, temp, humidity, ph, rainfall)

if __name__ == "__main__":
    main()
