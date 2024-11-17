import streamlit as st
from streamlit_option_menu import option_menu
import chatbot
import weather_forecast
import plant_diseasepredict
import govtscheme
import agri_analysis

def main():
    st.set_page_config(
        page_title="🌾 AgriSmartHub 🛠️", 
        layout="centered",  # Optimized for mobile devices
        initial_sidebar_state="collapsed"
    )

    # Custom CSS for better mobile design and fonts
    st.markdown(
        """
        <style>
        /* Importing Google Fonts for better typography */
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
        
        body {
            background-color: #f9f9f9;
            color: #333333;
            font-size: 16px;
            font-family: 'Poppins', sans-serif;
            margin: 0;
            padding: 0;
        }

        .stApp {
            margin: 0 auto;
            max-width: 480px;  /* Mobile-friendly width */
            padding: 15px;
        }

        h1 {
            font-size: 2.5em;
            color: #00796b;
            text-align: center;
            padding-top: 20px;
            font-weight: 600;
            text-shadow: 1px 1px 5px rgba(0, 0, 0, 0.1);
        }

        .stMarkdown {
            font-size: 16px;
            text-align: center;
            line-height: 1.6;
        }

        .navbar {
            display: flex;
            justify-content: space-around; 
            background-color: #00796b; 
            padding: 12px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        .nav-link {
            font-size: 14px;
            color: #fff;
            padding: 10px 15px;
            text-align: center;
            border-radius: 6px;
            transition: background-color 0.3s ease;
        }

        .nav-link:hover, .nav-link-selected {
            background-color: #004d40;
        }

        /* Styling for the content section */
        .content {
            padding-top: 20px;
            text-align: center;
        }

        .content h2 {
            font-size: 1.8em;
            color: #333;
            font-weight: 600;
        }

        .content p {
            font-size: 16px;
            color: #555;
            line-height: 1.7;
        }

        .stButton button {
            background-color: #00796b;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 5px;
            font-size: 14px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }

        .stButton button:hover {
            background-color: #004d40;
        }
        </style>
        """, 
        unsafe_allow_html=True
    )

    # Compact Navbar
    selected = option_menu(
        menu_title=None,
        options=["Home", "Chatbot", "Weather", "Disease", "Schemes", "Analysis"],
        icons=["house", "chat", "cloud-sun", "bug", "bank", "bar-chart"],
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0"},
            "nav-link": {"font-size": "14px", "padding": "5px"},
            "icon": {"font-size": "18px"},
        },
    )

    # Navigation Logic
    if selected == "Home":
        st.markdown("""
        <div class="content">
            <h2>Welcome to AgriConnect 🌍</h2>
            <p><strong>Your one-stop solution for agricultural needs. Explore:</strong></p>
            <ul>
                <li>🌟 <strong>Chatbot:</strong> AI-powered assistance for your queries.</li>
                <li>🌤️ <strong>Weather:</strong> Latest forecasts for your area.</li>
                <li>🌱 <strong>Disease Prediction:</strong> Identify crop diseases.</li>
                <li>📊 <strong>Analysis:</strong> Gain insights from agricultural data.</li>
                <li>🏦 <strong>Schemes:</strong> Discover relevant government schemes.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    elif selected == "Chatbot":
        chatbot.main()

    elif selected == "Weather":
        weather_forecast.main()

    elif selected == "Disease":
        plant_diseasepredict.main()

    elif selected == "Schemes":
        govtscheme.main()

    elif selected == "Analysis":
        agri_analysis.main()

if __name__ == "__main__":
    main()
