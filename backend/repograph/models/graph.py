from pydantic import BaseModel


class GraphSummary(BaseModel):
    is_empty: bool = True
    classes: int = 0
    functions: int = 0
