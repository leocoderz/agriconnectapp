import streamlit as st
import requests
from bs4 import BeautifulSoup
from requests.exceptions import SSLError, RequestException

# Function to fetch government schemes from the URL
def fetch_govt_schemes(url):
    try:
        # Bypass SSL verification (temporary solution)
        response = requests.get(url, verify=False)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            scheme_table = soup.find('table')  # Assuming the scheme information is in a table
            if scheme_table:
                schemes = []
                rows = scheme_table.find_all('tr')
                for row in rows[1:]:  # Skip the header row
                    columns = row.find_all('td')
                    scheme_details = [column.get_text(strip=True) for column in columns]
                    schemes.append(scheme_details)
                return schemes
        return None
    except SSLError as ssl_error:
        st.error(f"SSL Error: {ssl_error}. Could not verify the server's SSL certificate.")
        return None
    except RequestException as e:
        st.error(f"An error occurred while fetching the data: {e}")
        return None

# Main function to run the app
def main():
    # Custom CSS for better UI design
    st.markdown("""
    <style>
    .scheme-card {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s, box-shadow 0.3s;
        cursor: pointer;
    }
    .scheme-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    }
    .scheme-card-title {
        font-size: 18px;
        font-weight: bold;
        color: #00796b;
    }
    .scheme-card-description {
        font-size: 14px;
        color: #555;
    }
    .scheme-card-button {
        background-color: #00796b;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 4px;
        cursor: pointer;
    }
    .scheme-card-button:hover {
        background-color: #004d40;
    }
    </style>
    """, unsafe_allow_html=True)

    # App Title and Description
    st.title("🌾 Government Schemes for Farmers")
    st.markdown("Stay informed about agricultural welfare programs and subsidies. 🚜")

    # Fetch schemes from the URL
    url = "https://agriwelfare.gov.in/en/Major"  # Replace with the actual URL of the government schemes page
    with st.spinner("Fetching schemes..."):
        schemes = fetch_govt_schemes(url)

    # Display the schemes
    if schemes:
        st.success("Schemes fetched successfully! 📄")
        st.subheader("Available Government Schemes:")
        
        for scheme in schemes:
            # Create a card for each scheme
            st.markdown(f"""
            <div class="scheme-card">
                <div class="scheme-card-title">{scheme[0]}</div>
                <div class="scheme-card-description">
                    <b>Description:</b> {scheme[1]}<br>
                    <b>Eligibility:</b> {scheme[2]}<br>
                    <b>Benefits:</b> {scheme[3]}<br>
                </div>
                {f'<div><b>Application Process:</b> {scheme[4]}</div>' if len(scheme) > 4 else ''}
            </div>
            """, unsafe_allow_html=True)

            # Use Streamlit's button to handle the action
            if st.button(f"Apply for {scheme[0]}"):
                st.markdown(f"[Click here to apply for {scheme[0]}](https://example.com)")

            st.divider()  # Separator for better readability
    else:
        st.error("⚠️ Unable to fetch scheme information. Please check your connection or try again later.")

if __name__ == "__main__":
    main()
