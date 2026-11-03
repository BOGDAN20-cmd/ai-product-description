from fastapi import FastAPI, HTTPException

from app.llm import generate_product_card
from app.schemas import ProductInput, ProductOutput

app = FastAPI(title="AI Product Card Generator")


@app.post("/generate", response_model=ProductOutput)
async def generate(product: ProductInput):
    try:
        result = await generate_product_card(product.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return ProductOutput(**result)


@app.get("/")
async def root():
    return {"status": "ok", "service": "AI Product Card Generator"}
