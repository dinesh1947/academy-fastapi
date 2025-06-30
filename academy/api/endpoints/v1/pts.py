
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session, joinedload
from config.database import get_sync_db  
from api.models.v1.PtsModel import *
from api.schemas.v1.PtsSchema import *
from utils.project_jwt import *
from math import ceil
from utils.common import *
from utils.pagination import *
from datetime import datetime
import shutil
from uuid import uuid4
router = APIRouter()
from botocore.exceptions import NoCredentialsError
from datetime import datetime
from uuid import uuid4
from botocore.exceptions import NoCredentialsError
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session






from dotenv import load_dotenv
load_dotenv()
import os
import boto3


router = APIRouter()


# # Fetch AWS credentials from environment variables
# AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
# AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
# AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME')

# # Validate that credentials exist
# if not all([AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME, AWS_S3_REGION_NAME]):
#     raise RuntimeError("Missing AWS configuration in environment variables")

# # S3 folder inside the bucket
# S3_FOLDER = "pts/test_series"

# # Create boto3 S3 client using loaded credentials
# s3_client = boto3.client(
#     "s3",
#     region_name=AWS_S3_REGION_NAME,
#     aws_access_key_id=AWS_ACCESS_KEY_ID,
#     aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
# )























def upload_file_to_s3(file: UploadFile, folder: str) -> str:
    ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid4().hex}{ext}"
    key = f"{folder}/{filename}"  # this is what you'll store in the DB

    try:
        s3_client.upload_fileobj(
            file.file,
            AWS_STORAGE_BUCKET_NAME,
            key,
            ExtraArgs={
                "ContentType": file.content_type  # Recommended for correct MIME type
                # Removed ACL to avoid AccessDenied error due to BlockPublicAcls
            }
        )
        return key  # Return full key including folder
    except NoCredentialsError:
        raise HTTPException(status_code=500, detail="AWS credentials not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload to S3: {str(e)}")





def get_signed_url(key: str, expires_in=3600 * 24 * 365 * 10):  # 10 years by default
    return s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': AWS_STORAGE_BUCKET_NAME, 'Key': key},
        ExpiresIn=expires_in
    )







@router.post("/test-series/", status_code=status.HTTP_201_CREATED)
async def create_test_series(
    name: str = Form(...),
    mode: Optional[str] = Form(None),
    meta_title: Optional[str] = Form(None),
    meta_description: Optional[str] = Form(None),
    slug: Optional[str] = Form(None),
    publish_status: str = Form(...),
    short_description: str = Form(...),
    long_description: str = Form(...),
    start_date_time: Optional[datetime] = Form(None),
    end_date_time: Optional[datetime] = Form(None),
    url: Optional[str] = Form(None),
    official_email: Optional[str] = Form(None),
    test: Optional[int] = Form(0),
    status: str = Form("active"),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_sync_db)
):
    # Check for duplicate name
    existing = db.query(TestSeries).filter_by(name=name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Test Series with this name already exists.")

    image_url = None
    if image:
        image_url = upload_file_to_s3(image, S3_FOLDER)

    now = datetime.utcnow()
    new_test_series = TestSeries(
        name=name,
        mode=mode,
        meta_title=meta_title,
        meta_description=meta_description,
        slug=slug,
        publish_status=publish_status,
        short_description=short_description,
        long_description=long_description,
        start_date_time=start_date_time,
        end_date_time=end_date_time,
        url=url,
        official_email=official_email,
        test=test,
        status=status,
        image=image_url,
        created_at=now,
        updated_at=now,
    )

    db.add(new_test_series)
    db.commit()
    db.refresh(new_test_series)

    return {"id": new_test_series.id, "message": "Test Series created successfully"}


@router.get("/test-series/{test_series_id}")
def get_test_series(test_series_id: int, db: Session = Depends(get_sync_db)):
    test_series = db.query(TestSeries).filter_by(id=test_series_id).first()
    if not test_series:
        raise HTTPException(status_code=404, detail="Test Series not found")

    # Use signed URL to provide secure temporary access to the image
    image_url = get_signed_url(test_series.image) if test_series.image else None

    return {
        "id": test_series.id,
        "name": test_series.name,
        "mode": test_series.mode,
        "meta_title": test_series.meta_title,
        "meta_description": test_series.meta_description,
        "slug": test_series.slug,
        "publish_status": test_series.publish_status,
        "short_description": test_series.short_description,
        "long_description": test_series.long_description,
        "start_date_time": test_series.start_date_time,
        "end_date_time": test_series.end_date_time,
        "url": test_series.url,
        "official_email": test_series.official_email,
        "test": test_series.test,
        "status": test_series.status,
        "image_url": image_url,
        "created_at": test_series.created_at,
        "updated_at": test_series.updated_at,
    }















































@router.get("/test-list/", response_model=PaginatedResponse[TestSchema])
def read_tests(
    request: Request,
    db: Session = Depends(get_sync_db),
    page: int = 1,
    page_size: int = 10
):
    query = db.query(Test)
    return paginate_query(
        request=request,
        query=query,
        schema=TestSchema,
        page=page,
        page_size=page_size
    )


@router.get("/admin/test-list/", response_model=PaginatedResponse[TestSchema])
def admin_read_tests(
    request: Request,
    db: Session = Depends(get_sync_db),
    current_user: dict = Depends(admin_required),
    page: int = 1,
    page_size: int = 10
):
    query = db.query(Test)
    return paginate_query(
        request=request,
        query=query,
        schema=TestSchema,
        page=page,
        page_size=page_size
    )


@router.get("/question-paper-list/", response_model=PaginatedResponse[QuestionPaperSchema])
def read_question_papers(
    request: Request,
    db: Session = Depends(get_sync_db),
    page: int = 1,
    page_size: int = 10
):
    query = db.query(QuestionPaper)
    return paginate_query(
        request=request,
        query=query,
        schema=QuestionPaperSchema,
        page=page,
        page_size=page_size
    )


@router.get("/admin/question-paper-list/", response_model=PaginatedResponse[QuestionPaperSchema])
def admin_qp_tests(
    request: Request,
    db: Session = Depends(get_sync_db),
    current_user: dict = Depends(admin_required),
    page: int = 1,
    page_size: int = 10
):
    query = db.query(QuestionPaper)
    return paginate_query(
        request=request,
        query=query,
        schema=QuestionPaperSchema,
        page=page,
        page_size=page_size
    )


@router.get("/question-list/", response_model=PaginatedResponse[QuestionSchema])
def read_questions(
    request: Request,
    db: Session = Depends(get_sync_db),
    page: int = 1,
    page_size: int = 10
):
    query = db.query(Question)
    return paginate_query(
        request=request,
        query=query,
        schema=QuestionSchema,
        page=page,
        page_size=page_size
    )


@router.get("/question-list-a/", response_model=PaginatedResponse[QuestionSchema])
def read_questions_filtered(
    request: Request,
    db: Session = Depends(get_sync_db),
    page: int = 1,
    page_size: int = 10,
    question_paper_id: Optional[int] = None
):
    query = db.query(Question).options(joinedload(Question.question_paper))

    if question_paper_id:
        query = query.filter(Question.question_paper_id == question_paper_id)

    return paginate_query(
        request=request,
        query=query,
        schema=QuestionSchema,
        page=page,
        page_size=page_size
    )











































