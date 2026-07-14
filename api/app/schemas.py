from pydantic import BaseModel


class CustomerFeatures(BaseModel):

    frequency: float

    monetary: float

    recency: float

    avg_order_value: float
