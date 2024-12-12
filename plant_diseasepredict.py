# Library imports
import numpy as np
import streamlit as st
from PIL import Image
from keras.models import load_model
import openai

# OpenAI API Key
api_key = "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"  # Directly set your OpenAI API key here
openai.api_key = api_key  # Assign the API key to openai

# Load the Model
model = load_model('plant_disease_model.h5')

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

# Function to get recommendations from OpenAI Chat models (new API interface)
def get_recommendations(plant_disease):
    # Prompt for OpenAI Chat model
    prompt = f"I have detected {plant_disease}. Can you recommend a treatment or remedy to cure this plant disease? Also, which fertilizer can be used to avoid the disease in the future?"

    try:
        # Generate response from OpenAI GPT-4 model (or GPT-3.5)
        response = openai.ChatCompletion.create(
            model="gpt-4",  # You can also use "gpt-3.5-turbo" if you prefer
            messages=[
                {"role": "system", "content": "You are an agricultural assistant, skilled in providing recommendations for plant diseases and fertilizers."},
                {"role": "user", "content": prompt}
            ]
        )

        # Extracting treatment and fertilizer recommendations
        result = response['choices'][0]['message']['content'].strip()
        treatment = result
        fertilizer = ""

        # Split response if fertilizer recommendation is included
        if "Fertilizer Recommendation:" in result:
            treatment, fertilizer = result.split("Fertilizer Recommendation:")
            treatment = treatment.strip()
            fertilizer = fertilizer.strip()

        return treatment, fertilizer

    except openai.APIConnectionError as e:
        return "The server could not be reached. Please check your network connection.", ""
    except openai.RateLimitError as e:
        return "Too many requests. Please try again later.", ""
    except openai.APIStatusError as e:
        return f"Error {e.status_code}: {e.response}. Please try again later.", ""
    except openai.APIError as e:
        return f"An unexpected error occurred: {str(e)}", ""
    except Exception as e:
        return f"An error occurred: {str(e)}", ""

if __name__ == "__main__":
    main()
