"""
API for generating summary using BART-Large-CNN model
"""
from fastapi import FastAPI, HTTPException
from models.bart_summarization import get_summary
from evaluation.rogue_metrics import get_accuracy
import time
from utils import calculate_llm_inference_cost
from pydantic import BaseModel

app = FastAPI()


class Info(BaseModel):
    article_id: str
    prompt: str
    max_length: int
    model_name: str
    ground_truth: str


@app.post("/generate/")
async def generate_text(info: Info):
    """
    API endpoint to generate summary for the
    article and returns a json response.
    :param info:
    :return: response :JSON
    {Article Id, Summary, Accuracy, Prompt length,
    Summary length, Inference cost, Inference Time}
    """
    try:

        if info.model_name == 'BART':
            pretrained_model = "facebook/bart-large-cnn"
            start_time = time.time()
            summary = get_summary(pretrained_model, info.prompt, info.max_length)
            end_time = time.time()
            elapsed_time = end_time - start_time
            scores = get_accuracy(info.ground_truth, summary)
            cost = calculate_llm_inference_cost(len(info.prompt), cost_per_token=0.00001)
            response = {"Article Id": info.article_id,
                        "Summary": summary,
                        "Accuracy": scores,
                        "Prompt length": len(info.prompt),
                        "Summary length": len(summary),
                        "Inference Cost": cost,
                        "Inference time": elapsed_time}
        else:
            response = {"Model not implemented."}

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error generating text")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
