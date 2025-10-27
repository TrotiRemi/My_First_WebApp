from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from sqlalchemy.orm import Session
import os
from app.db.session import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.document import Document
from app.schemas.document import DocumentCreate, DocumentResponse
from app.crud.document import create_document, get_document, get_documents_by_course, get_all_documents

router = APIRouter()

# Dossier pour stocker les fichiers uploadés
UPLOAD_DIR = "/app/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
def add_document(
    document: DocumentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Créer un nouveau document pour un cours (authentifié)"""
    doc = create_document(db=db, document=document, user_id=current_user.id)
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Course not found or you don't have permission"
        )
    return doc


@router.post("/upload/{course_id}", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    course_id: int,
    file: UploadFile = File(...),
    title: str = Form(...),
    doc_type: str = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Uploader un fichier et créer un document"""
    from app.models.course import Course
    
    # Vérifier que le cours appartient à l'utilisateur
    course = db.query(Course).filter(
        Course.id == course_id,
        Course.user_id == current_user.id
    ).first()
    
    if not course:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    # Sauvegarder le fichier
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required")
    
    # Générer un nom de fichier sécurisé
    import uuid
    file_ext = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    # Écrire le fichier
    contents = await file.read()
    with open(file_path, 'wb') as f:
        f.write(contents)
    
    # Créer le document
    doc_title = title if title else file.filename
    download_url = f"http://localhost:8000/api/v1/documents/download/{unique_filename}"
    
    doc = Document(
        title=doc_title,
        url=download_url,
        file_path=file_path,
        type=doc_type,
        course_id=course_id
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    
    return doc


@router.get("/download/{filename}")
def download_document(filename: str):
    """Télécharger un fichier"""
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    # Sécurité : vérifier que le fichier est dans le bon dossier
    if not os.path.abspath(file_path).startswith(os.path.abspath(UPLOAD_DIR)):
        raise HTTPException(status_code=403, detail="Access denied")
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    from fastapi.responses import FileResponse
    return FileResponse(file_path)


@router.get("/{doc_id}", response_model=DocumentResponse)
def get_doc(
    doc_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer un document spécifique"""
    doc = get_document(db=db, doc_id=doc_id)
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    
    # Vérifier que l'utilisateur possède le cours du document
    if doc.course.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    return doc


@router.get("/course/{course_id}", response_model=list[DocumentResponse])
def get_docs_by_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer tous les documents d'un cours"""
    from app.models.course import Course
    
    # Vérifier que le cours appartient à l'utilisateur
    course = db.query(Course).filter(
        Course.id == course_id,
        Course.user_id == current_user.id
    ).first()
    
    if not course:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    return get_documents_by_course(db=db, course_id=course_id)


@router.get("/", response_model=list[DocumentResponse])
def get_all_docs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer tous les documents de l'utilisateur connecté"""
    return get_all_documents(db=db, user_id=current_user.id)


@router.delete("/{doc_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_doc(
    doc_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Supprimer un document (seulement le propriétaire du cours peut le faire)"""
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Vérifier que l'utilisateur possède le cours du document
    if doc.course.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this document")
    
    # Supprimer le fichier du disque s'il existe
    if doc.file_path and os.path.exists(doc.file_path):
        try:
            os.remove(doc.file_path)
        except Exception as e:
            print(f"Erreur lors de la suppression du fichier: {e}")
    
    db.delete(doc)
    db.commit()

