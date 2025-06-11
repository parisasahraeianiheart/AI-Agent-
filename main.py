from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langgraph.graph import StateGraph
from osint_graph import osint_graph

app = FastAPI()

class OSINTQuery(BaseModel):
    query: str

@app.post("/run_osint")
async def run_osint(query_data: OSINTQuery):
    try:
        query = query_data.query
        print(f"🧠 Received OSINT query: {query}")

        # Run the LangGraph pipeline
        result = osint_graph.invoke({"input": query})
        return {"status": "success", "output": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))