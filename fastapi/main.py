from fastapi import FastAPI, HTTPException, Depends
from utils.db_utils import models, schemas, engine, SessionLocal, crud
from sqlalchemy.orm import Session
# from utils.db_utils import models, engine, SessionLocal, schemas, crud, common, pipeline

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="SoundJot")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/api/v1/health")
async def check() -> dict:
    return {"message": "OK"}

@app.post("/api/v1/user", response_model=schemas.UserCreate)
async def register_user(user_input: schemas.UserCreate, db: Session = Depends(get_db)):
    if not (user_input.username and
            user_input.password and
            user_input.cnf_password and
            user_input.firstname and
            user_input.lastname):
        raise HTTPException(
            status_code=404, detail=r"Username and password cannot be empty")
    if user_input.password != user_input.cnf_password:
        raise HTTPException(
            status_code=404, detail=r"Provided passwords do not match")
    return crud.create_user(db, user_input)
