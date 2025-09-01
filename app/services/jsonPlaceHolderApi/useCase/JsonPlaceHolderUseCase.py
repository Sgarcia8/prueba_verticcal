from abc import ABC, abstractmethod
from typing import List, Optional
from schemas.jsonPlaceHolderApi.PostDtoRequest import Post

# La interfaz JsonPlaceHolderUseCase define los métodos que cualquier clase que implemente esta interfaz debe tener.
class JsonPlaceHolderUseCase(ABC):
    @abstractmethod
    async def get_items_by_key_word(self, field:str, key_word:str) -> Optional[List[Post]]:
        """Método para obtener posts desde la API externa."""
        pass


    