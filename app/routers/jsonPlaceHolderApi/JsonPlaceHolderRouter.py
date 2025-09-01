# app/routers/external_data.py
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from services.jsonPlaceHolderApi.serviceImpl.JsonPlaceHolderServiceImpl import JsonPlaceHolderServiceImpl
from schemas.jsonPlaceHolderApi.PostDtoRequest import Post

router = APIRouter(prefix="/external-data", tags=["External Data"])

# Dependencia para inyectar el servicio de datos externos
def get_external_data_service() -> JsonPlaceHolderServiceImpl:
    """Provee una instancia del servicio de datos externos."""
    return JsonPlaceHolderServiceImpl(base_url="https://jsonplaceholder.typicode.com")

@router.get(
    "/posts",
    response_model=List[Post],
    summary="Obtiene todos los posts",
    description="Recupera una lista completa de todos los posts disponibles de la API externa.",
)
async def get_all_posts(
    service: JsonPlaceHolderServiceImpl = Depends(get_external_data_service)
) -> List[Post]:
    """
    Endpoint para obtener todos los posts.
    """
    try:
        return await service.get_items()
    except HTTPException as e:
        raise e

@router.get(
    "/posts/filter",
    response_model=Optional[List[Post]],
    summary="Filtra posts por una palabra clave",
    description="Filtra la lista de posts por un campo ('title' o 'body') y una palabra clave específica.",
)
async def get_posts_by_keyword(
    field: str = Query(..., title="Campo de filtro", description="El campo del post por el cual filtrar: 'title' o 'body'"),
    key_word: str = Query(..., title="Palabra clave", description="La palabra clave a buscar dentro del campo especificado."),
    service: JsonPlaceHolderServiceImpl = Depends(get_external_data_service),
) -> Optional[List[Post]]:
    """
    Endpoint para buscar posts por una palabra clave en un campo específico.
    """
    try:
        posts = await service.get_items_by_key_word(field, key_word)
        return posts
    except HTTPException as e:
        raise e

@router.get(
    "/posts/{post_id}",
    response_model=Optional[Post],
    summary="Obtiene un post por ID",
    description="Recupera un post específico de la API externa utilizando su ID.",
)
async def get_single_post(
    post_id: int,
    service: JsonPlaceHolderServiceImpl = Depends(get_external_data_service)
) -> Optional[Post]:
    """
    Endpoint para obtener un post por su ID.
    """
    try:
        post = await service.get_item_by_id(post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        return post
    except HTTPException as e:
        raise e

