from __future__ import annotations

from fastapi import FastAPI
from starlette import status
from tinydb import TinyDB
from tinydb.table import Document
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


class BaseProjectModel(BaseModel):
    name: str = Field(..., title="Project name", example="My Project")
    description: str = Field(
        ...,
        title="Project description",
        example="This is my project",
    )


class ProjectResponse(BaseProjectModel):
    id: int = Field(..., title="Project ID", example=1)

    @classmethod
    def from_document(cls, doc: Document) -> ProjectResponse:
        return cls(id=doc.doc_id, **doc)


class CreateProject(BaseProjectModel):
    pass


class UpdateProject(BaseProjectModel):
    pass


class DeletionResponse(BaseModel):
    message: str = Field(..., title="Response message", example="Project deleted")


projects = TinyDB("projects.json")


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods="*",
    allow_headers="*",
)


@app.get("/ping")
async def root():
    return {"message": "pong"}


@app.get("/projects")
async def list_projects() -> list[ProjectResponse]:
    return [ProjectResponse.from_document(doc) for doc in projects.all()]


@app.get("/projects/{project_id}")
async def get_project(project_id: int) -> ProjectResponse:
    return ProjectResponse.from_document(projects.get(doc_id=project_id))


@app.post("/projects")
async def create_project(body: CreateProject) -> ProjectResponse:
    doc_id = projects.insert(body.dict())
    return ProjectResponse.from_document(projects.get(doc_id=doc_id))


@app.delete("/projects/{project_id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_project(project_id: int) -> DeletionResponse:
    projects.remove(doc_ids=[project_id])
    return {"message": "Project deleted"}
