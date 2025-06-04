from fastapi import FastAPI, UploadFile
from .db.collections.file import files_collection, FileSchema
from .utils.file import save_to_disk
from .queue.q import q
from .queue.workers import process_file

app = FastAPI()

@app.get('/')
def hello():
    return {'status' : 'healthy'}

@app.post('/upload')
async def upload_file(file: UploadFile):
    
    db_file = await files_collection.insert_one(
        document = FileSchema(
            file = file.filename,
            status = "saving"
        )
    )

    file_path = f"/mnt/uploads/{str(db_file.inserted_id)}/{file.filename}"

    await save_to_disk(file=await file.read(), path= file_path)

    # Push to Queued
    q.enqueue(process_file, str(db_file.inserted_id))

    # Mongodb Save
    await files_collection.update_one({'_id': db_file.inserted_id}, {
        '$set': {
            'status': 'Queued'
        }
    })

    return {'file_id': str(db_file.inserted_id)}