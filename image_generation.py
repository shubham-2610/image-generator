import streamlit as st
import base64
import boto3
import json
import os

st.title(" Image Generator")

prompt = st.text_input("Enter the description for the image")

model_id = "amazon.titan-image-generator-v1"

if st.button("Generate Image"):
    with st.spinner("Generating image..."):
        client = boto3.client("bedrock-runtime", region_name="us-east-1")

        native_request = {
            "textToImageParams": {"text": prompt},
            "taskType": "TEXT_IMAGE",
            "imageGenerationConfig": {"cfgScale": 8, "seed": 0, "width": 1024, "height": 1024, "numberOfImages": 1}
        }

        request = json.dumps(native_request)
        response = client.invoke_model(modelId=model_id, body=request)
        model_response = json.loads(response["body"].read())
        base64_image_data = model_response["images"][0]
        image_data = base64.b64decode(base64_image_data)
        output_dir = "output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        image_path = os.path.join(output_dir, "generated_image.png")
        with open(image_path, "wb") as file:
            file.write(image_data)
        st.image(image_path, caption="Generated Image")
        st.success(f"The generated image has been saved to {image_path}.")
