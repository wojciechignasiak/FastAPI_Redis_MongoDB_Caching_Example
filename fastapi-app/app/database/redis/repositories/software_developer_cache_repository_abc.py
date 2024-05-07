from abc import ABC, abstractmethod
from app.models.software_developer import SoftwareDeveloperModel

class SoftwareDeveloperCacheRepositoryABC(ABC):

    @abstractmethod
    async def create_or_update(self, created_or_updated_software_developer: SoftwareDeveloperModel) -> bool:
        pass
    
    @abstractmethod
    async def get(self, software_developer_id: str):
        pass

    @abstractmethod
    async def delete(self, software_developer_id: str):
        pass