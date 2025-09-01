# app/services/external_api.py
from schemas.jsonPlaceHolderApi.PostDtoRequest import Post
from services.jsonPlaceHolderApi.useCase.JsonPlaceHolderUseCase import JsonPlaceHolderUseCase
from services.genericUseCase.GenericUseCase import GenericUseCase
import httpx
from fastapi import HTTPException
from typing import List, Optional

class JsonPlaceHolderServiceImpl(GenericUseCase[Post], JsonPlaceHolderUseCase):

    def __init__(self, base_url: str):
        self.base_url = base_url

    async def _get_all_posts(self) -> List[Post]:
        """Método privado para obtener todos los posts de la API externa."""
        async with httpx.AsyncClient(base_url=self.base_url) as client:
            try:
                response = await client.get("/posts", timeout=10.0)
                response.raise_for_status()
                return [Post(**item) for item in response.json()]
            except httpx.HTTPStatusError as e:
                raise HTTPException(status_code=e.response.status_code, detail=f"Error de la API externa: {e.response.status_code}")
            except httpx.RequestError as e:
                raise HTTPException(status_code=500, detail=f"Error de conexión con la API externa: {e}")

    async def get_items(self) -> List[Post]:
        """
        Obtiene todos los posts de la API externa.
        """
        return await self._get_all_posts()

    async def get_item_by_id(self, post_id: int) -> Optional[Post]:
        """Método para obtener un post por ID desde la API externa."""
        async with httpx.AsyncClient(base_url=self.base_url) as client:
            try:
                response = await client.get(f"/posts/{post_id}", timeout=10.0)
                response.raise_for_status()
                return Post(**response.json())
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    raise HTTPException(status_code=404, detail=f"Error de la API externa: No se encontró el post con ID {post_id}")
                raise HTTPException(status_code=e.response.status_code, detail=f"Error de la API externa: {e.response.status_code}")
            except httpx.RequestError as e:
                raise HTTPException(status_code=500, detail=f"Error de conexión con la API externa: {e}")
    
    async def get_items_by_key_word(self, field: str, key_word: str) -> Optional[List[Post]]:
        """
        Método para obtener y filtrar posts de la API externa por una palabra clave.
        """
        # 1. Método privado para obtener los posts
        posts = await self._get_all_posts()

        # 2. Filtrar los posts localmente
        normalized_key_word = key_word.lower()
        try:
            filtered_posts = [
                post for post in posts
                if normalized_key_word in getattr(post, field, '').lower()
            ]
            # 3. Devolver la lista filtrada o None si está vacía
            return filtered_posts 
        except AttributeError:
            raise HTTPException(status_code=500, detail="Error al acceder a los campos del modelo Post.")
     
        
        
