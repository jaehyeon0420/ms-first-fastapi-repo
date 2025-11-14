#pip install azure-cognitiveservices-vision-customvision
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials

#pip install pillow
from PIL import Image

#pip install matplotlib
import matplotlib.pyplot as plt

#.env Read
from app.core.config import settings


# Custom Vision Model Request & Response
def estimate_custom_vision(saved_files) :
    
    # Custom Vision API Key
    prediction_key = settings.CUSTOM_VISION_KEY
    # Custom Vision EndPoint
    prediction_endpoint = settings.CUSTOM_VISION_ENDPOINT
    # Custom Vision Model Project ID
    project_id = settings.CUSTOM_VISION_PROJECT_ID
    # Custom Vision Model Name
    model_name = settings.CUSTOM_VISION_MODEL_NAME

    credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
    predictor = CustomVisionPredictionClient(endpoint=prediction_endpoint, credentials=credentials)
    
    response = {}
    
    for save_file in saved_files :

        # Ex) app/upload/20251114/20251114111219198_08830.jfif
        image_file = save_file['save_path']

        # 1) Custom Vision Model Request
        with open(image_file, mode="rb") as image_data:
            results = predictor.classify_image(project_id, model_name, image_data)
            print(results)

        # 2) Custom Vision Model Response
        for prediction in results.predictions:
            print(f"Tag: {prediction.tag_name}, Probability: {prediction.probability:.2f}")
            response[prediction.tag_name] =  prediction.probability
        
    return response
        # 3) Calculator Cost
            
    