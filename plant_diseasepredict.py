# Library imports
import numpy as np
import streamlit as st
from PIL import Image
from keras.models import load_model
from openai import OpenAI

# Loading the Model
model = load_model('plant_disease_model.h5')

# OpenAI API Key
api_key = "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"
client = OpenAI(api_key=api_key)

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
        st.image(plant_image, caption="Uploaded Image", use_column_width=True)
    
    # Predict Button
    if st.button("🔍 Predict Disease"):
        if plant_image:
            with st.spinner("Analyzing the image..."):
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
        else:
            st.error("Please upload an image before proceeding.")

# Function to get recommendations from ChatGPT
def get_recommendations(plant_disease):
    # Prompt for ChatGPT
    prompt = f"I have detected {plant_disease}. Can you recommend a treatment or remedy to cure this plant disease? Also, which fertilizer can be used to avoid the disease in the future?"

    # Generate response from ChatGPT
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an agricultural assistant, skilled in providing recommendations for plant diseases and fertilizers."},
            {"role": "user", "content": prompt}
        ]
    )

    # Initialize treatment and fertilizer recommendations
    treatment = ""
    fertilizer = ""

    # Extracting recommendations
    for choice in completion.choices:
        message = choice.message.content
        if "Fertilizer Recommendation:" in message:
            fertilizer = message.split("Fertilizer Recommendation:")[1].strip()
        else:
            treatment = message.strip()

    return treatment, fertilizer

if __name__ == "__main__":
    main()
