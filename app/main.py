from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import os
from app.rule_converter import RuleConverter

app = FastAPI()

# Init RuleConverter
converter = RuleConverter()

# Request and Response models
class RuleRequest(BaseModel):
    xml_rule: str

class RuleResponse(BaseModel):
    json_rule: str

@app.post("/convert_rule", response_model=RuleResponse)
async def convert_rule(request: RuleRequest):
    """
    Endpoint to convert XML rules to JSON using the preloaded RuleConverter.
    """
    try:
        converted_rule = converter.convert_rule(request.xml_rule)
        return RuleResponse(json_rule=converted_rule)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Conversion failed: {str(e)}")

@app.post("/train_model")
async def train_model():
    """
    Endpoint to trigger training by executing train_model.py.
    """
    try:
        script_path = os.path.join(os.path.dirname(__file__), "train_model.py")
        result = subprocess.run(
            ["python", script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=f"Training failed: {result.stderr}")
        
        # Reload the updated model after training
        converter.reload_model()
        return {"message": "Training completed successfully!", "log": result.stdout}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error starting training: {str(e)}")

@app.get("/")
async def root():
    """
    Root endpoint to check service health.
    """
    return {"message": "Rule Migration Service is running!"}