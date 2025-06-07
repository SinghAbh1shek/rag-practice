from fastapi import FastAPI, UploadFile, Path
from .db.collections.file import files_collection, FileSchema
from .utils.file import save_to_disk
from .queue.q import q
from .queue.workers import process_file
from bson import ObjectId

app = FastAPI()

@app.get("/{id}")
async def get_file_by_id(id: str = Path(..., description = "ID of the file")):
    db_file = await files_collection.find_one({'_id': ObjectId(id)})
    return {
        "id": str(db_file["_id"]),
        "name": db_file["name"],
        "status": db_file["status"],
        "result": db_file["result"] if 'result' in db_file else None,
    }

@app.get('/')
def hello():
    return {'status' : 'healthy'}

@app.post('/upload')
async def upload_file(file: UploadFile):
    
    db_file = await files_collection.insert_one(
        document = FileSchema(
            name = file.filename,
            status = "saving"
        )
    )

    file_path = f"/mnt/uploads/{str(db_file.inserted_id)}/{file.filename}"

    await save_to_disk(file=await file.read(), path= file_path)

    # Push to Queued
    q.enqueue(process_file, str(db_file.inserted_id), file_path)

    # Mongodb Save
    await files_collection.update_one({'_id': db_file.inserted_id}, {
        '$set': {
            'status': 'Queued'
        }
    })

    return {'file_id': str(db_file.inserted_id)}






from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for security in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
