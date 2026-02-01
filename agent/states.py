from pydantic import BaseModel, Field, ConfigDict

class File(BaseModel):
    path: str = Field(description="The file path where the file will be created e.g 'src/components/Calculator.js'")
    purpose: str = Field(description="The purpose of the file e.g 'This file contains the main calculator component'")

class Plan(BaseModel):
    name: str = Field(description="The name of the app of to be built")
    description: str = Field(description="A oneline description of the app to be built e.g 'A social media app for sharing photos'")
    technologies: list[str] = Field(description="A list of technologies to be used to build the app e.g ['React', 'Node.js']")
    features: list[str] = Field(description="A list of features to be included in the app e.g ['User authentication', 'Real-time chat']")
    files: list[File] = Field(description="A list of files to be created for the app each with a 'path' and 'purpose'.")

class Task(BaseModel):
    filepath : str = Field(description="The file path where this task will be implemented e.g 'src/components/Calculator.js'")
    title: str = Field(description="The title of the task e.g 'Implement user authentication'")
    description: str = Field(description="A detailed description of the task including what needs to be implemented.")
    integration_details: str = Field(description="Details on how this task integrates with other parts of the project e.g imports, function signatures, data flow.")

class TaskPlan(BaseModel):
    tasks: list[Task] = Field(description="A list of steps to be taken to implement the task")
    model_config = ConfigDict(extra="allow")
