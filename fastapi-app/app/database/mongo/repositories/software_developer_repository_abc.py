from abc import ABC, abstractmethod
from app.models.software_developer import (
    CreateSoftwareDeveloperModel, 
    SoftwareDeveloperModel, 
    UpdateSoftwareDeveloperModel
)


class SoftwareDeveloperRepositoryABC(ABC):

    @abstractmethod
    async def create(self, software_developer: CreateSoftwareDeveloperModel) -> SoftwareDeveloperModel:
        pass
    
    @abstractmethod
    async def delete(self, software_developer_id: str) -> bool:
        pass
    
    @abstractmethod
    async def get(self, software_developer_id: str) -> SoftwareDeveloperModel:
        pass
        
    @abstractmethod
    async def update(self, software_developer_id: str, update_software_developer: UpdateSoftwareDeveloperModel) -> SoftwareDeveloperModel:
        pass
