from fastapi import FastAPI
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",  # Your React frontend's origin
    # Add other allowed origins if necessary, e.g., your deployed frontend URL
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,           # allowed origins
    allow_credentials=True,
    allow_methods=["*"],             # allow all methods
    allow_headers=["*"],             # allow all headers
)

@app.get("/current-time")
async def get_current_time():
    return {"current_time": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)   