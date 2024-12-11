import openai
from openai.error import AuthenticationError, OpenAIError  # Import specific exceptions

# Function to get recommendations from ChatGPT
def get_recommendations(plant_disease):
    # Prompt for ChatGPT
    prompt = f"I have detected {plant_disease}. Can you recommend a treatment or remedy to cure this plant disease? Also, which fertilizer can be used to avoid the disease in the future?"

    try:
        # Generate response from ChatGPT
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an agricultural assistant, skilled in providing recommendations for plant diseases and fertilizers."},
                {"role": "user", "content": prompt}
            ]
        )

        # Extracting treatment and fertilizer recommendations
        response = completion.choices[0].message.content.strip()
        treatment = response
        fertilizer = ""

        # Split response if fertilizer recommendation is included
        if "Fertilizer Recommendation:" in response:
            treatment, fertilizer = response.split("Fertilizer Recommendation:")
            treatment = treatment.strip()
            fertilizer = fertilizer.strip()

        return treatment, fertilizer
    except AuthenticationError:
        return "Unable to authenticate with OpenAI. Check your API key.", ""
    except OpenAIError as e:
        return f"An OpenAI error occurred: {str(e)}", ""
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}", ""
