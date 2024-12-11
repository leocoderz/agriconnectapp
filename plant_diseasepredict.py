# Library imports
import numpy as np
import streamlit as st
from PIL import Image
from keras.models import load_model
import google.generativeai as genai
import os

# Load the Model
model = load_model('plant_disease_model.h5')

# Set Google Generative AI Key securely (Ensure Google Cloud credentials are set up)
genai.credentials.api_key = os.getenv("GOOGLE_API_KEY")  # Ensure this environment variable is set

# Name of Classes
CLASS_NAMES = ('Tomato-Bacterial_spot', 'Potato-Early_blight', 'Corn-Common_rust')

# Main function
def main():
    # App Title and Description
    st.title("🌱 Plant Disease Detection 📸")
    st.markdown("Upload a clear image of a plant leaf to detect possible diseases.")

    # Upload Image Section
    plant_image = st.file_uploader("📤 Upload an image (JPG only):", type="jpg")
    if plant_image:
        # Displaying the uploaded image
        st.image(plant_image, caption="Uploaded Image", use_container_width=True)
    
    # Predict Button
    if st.button("🔍 Predict Disease"):
        if plant_image:
            with st.spinner("Analyzing the image..."):
                try:
                    # Process and Predict
                    image = Image.open(plant_image).resize((256, 256))
                    image_array = np.array(image) / 255.0
                    image_array = np.expand_dims(image_array, axis=0)

                    # Model Prediction
                    Y_pred = model.predict(image_array)
                    result = CLASS_NAMES[np.argmax(Y_pred)]
                    disease_name, disease_type = result.split('-')
                    
                    # Display Prediction
                    st.success(f"🌿 This is a **{disease_name}** leaf with **{disease_type}**.")

                    # Get Recommendations
                    treatment, fertilizer = get_recommendations(result)

                    # Show Recommendations in Expanders
                    with st.expander("💊 Recommended Treatment"):
                        st.write(treatment)
                    if fertilizer:
                        with st.expander("🌾 Fertilizer Recommendation"):
                            st.write(fertilizer)
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
        else:
            st.error("Please upload an image before proceeding.")

# Function to get recommendations from Google's Generative AI
def get_recommendations(plant_disease):
    # Prompt for Generative AI
    prompt = f"I have detected {plant_disease}. Can you recommend a treatment or remedy to cure this plant disease? Also, which fertilizer can be used to avoid the disease in the future?"

    try:
        # Generate response from Google Generative AI
        response = genai.ChatMessage.create(
            model="chat-bison",  # You can change the model as per your requirement
            messages=[
                {"role": "system", "content": "You are an agricultural assistant, skilled in providing recommendations for plant diseases and fertilizers."},
                {"role": "user", "content": prompt}
            ]
        )

        # Extracting treatment and fertilizer recommendations
        response_text = response['text'].strip()
        treatment = response_text
        fertilizer = ""

        # Split response if fertilizer recommendation is included
        if "Fertilizer Recommendation:" in response_text:
            treatment, fertilizer = response_text.split("Fertilizer Recommendation:")
            treatment = treatment.strip()
            fertilizer = fertilizer.strip()

        return treatment, fertilizer
    except genai.errors.AuthenticationError:
        return "Unable to authenticate with Google Generative AI. Check your API key.", ""
    except genai.errors.InvalidRequestError as e:
        return f"Request error: {str(e)}", ""
    except Exception as e:
        return f"An error occurred: {str(e)}", ""

if __name__ == "__main__":
    main()
