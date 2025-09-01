from abc import ABC, abstractmethod
from typing import List, Optional, TypeVar, Generic
from schemas.jsonPlaceHolderApi.PostDtoRequest import Post

T = TypeVar('T')

# La interfaz JsonPlaceHolderUseCase define los métodos que cualquier clase que implemente esta interfaz debe tener.
class GenericUseCase(ABC, Generic[T]):
    @abstractmethod
    async def get_items(self) -> List[T]:
        """Método para obtener todos los item"""
        pass

    @abstractmethod
    async def get_item_by_id(self, postId:int) -> Optional[T]:
        """Método para obtener items por ID"""
        pass

    