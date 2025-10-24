from sqlalchemy.orm import Session
from app.models.document import Document
from app.models.course import Course
from app.schemas.document import DocumentCreate


def create_document(db: Session, document: DocumentCreate, user_id: int) -> Document:
    """Créer un document - vérifie que l'utilisateur possède le cours"""
    # Vérifier que le cours existe et appartient à l'utilisateur
    course = db.query(Course).filter(
        Course.id == document.course_id,
        Course.user_id == user_id
    ).first()
    
    if not course:
        return None  # Cours n'existe pas ou ne belongs à l'user
    
    db_doc = Document(
        title=document.title,
        url=document.url,
        type=document.type,
        course_id=document.course_id
    )
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)
    return db_doc


def get_document(db: Session, doc_id: int) -> Document:
    """Récupérer un document par ID"""
    return db.query(Document).filter(Document.id == doc_id).first()


def get_documents_by_course(db: Session, course_id: int) -> list[Document]:
    """Récupérer tous les documents d'un cours"""
    return db.query(Document).filter(Document.course_id == course_id).all()


def get_all_documents(db: Session, user_id: int) -> list[Document]:
    """Récupérer tous les documents de l'utilisateur (via ses cours)"""
    return db.query(Document).join(Course).filter(Course.user_id == user_id).all()
