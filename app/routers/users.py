from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app import repositories
from app.database import get_db
from app.schemas.user import UserCreate, UserResponse, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserResponse], summary="Listar usuários")
def list_users(
    skip: int = Query(0, ge=0, description="Registros a pular"),
    limit: int = Query(100, ge=1, le=200, description="Máximo de registros"),
    db: Session = Depends(get_db),
):
    return repositories.user.get_all(db, skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserResponse, summary="Buscar usuário por ID")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = repositories.user.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    return user


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED, summary="Criar usuário")
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    if repositories.user.get_by_email(db, payload.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="E-mail já cadastrado",
        )
    return repositories.user.create(db, payload)


@router.patch("/{user_id}", response_model=UserResponse, summary="Atualizar usuário")
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    user = repositories.user.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")

    if payload.email and payload.email != user.email:
        if repositories.user.get_by_email(db, payload.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="E-mail já cadastrado",
            )

    return repositories.user.update(db, user, payload)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Remover usuário")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = repositories.user.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    repositories.user.delete(db, user)
