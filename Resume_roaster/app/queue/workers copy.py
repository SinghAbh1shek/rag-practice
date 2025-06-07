from ..db.collections.file import files_collection
from bson import ObjectId
from pdf2image import convert_from_path
import os


import base64
from openai import OpenAI

client = OpenAI(
    api_key=""
)

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


async def process_file(id: str, file_path: str):
    await files_collection.update_one({'_id': ObjectId(id)} , {
        '$set': {
            "status": "Processing..."
        }
    })
    await files_collection.update_one({'_id': ObjectId(id)} , {
        '$set': {
            "status": "Converting to images..."
        }
    })
    
    pages = convert_from_path(file_path)
    images = []

    for i, page in enumerate(pages):
        image_save_path = f"/mnt/uploads/images/{id}/image-{i}.jpg"
        os.makedirs(os.path.dirname(image_save_path), exist_ok=True)
        page.save(image_save_path, 'JPEG')
        images.append(image_save_path)
        
    await files_collection.update_one({'_id': ObjectId(id)} , {
        '$set': {
            "status": "Converting to success!"
        }
    })
    
    
    images_base64 = [encode_image(img) for img in images]

    result = client.responses.create(
        model="gpt-4.1",
        input=[
            {
                "role": "user",
                "content": [
                    { "type": "input_text", "text": "Roast this resume" },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{images_base64[0]}",
                    },
                ],
            }
        ],
    )
    
    
    # print(result.output_text)

    await files_collection.update_one({'_id': ObjectId(id)} , {
        '$set': {
            "status": "Processed!",
            "result": result.output_text
        }
    })
