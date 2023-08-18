from transformers import BartForConditionalGeneration, BartTokenizer


def get_summary(pretrained_model, prompt, max_length):
    """
    generate summary using model.
    :param pretrained_model: str
    :param prompt: str
    :param max_length: int
    :return: Summary : str
    """
    model = BartForConditionalGeneration.from_pretrained(pretrained_model)
    tokenizer = BartTokenizer.from_pretrained(pretrained_model)
    inputs = tokenizer(prompt, max_length=max_length, return_tensors="pt", truncation=True)
    summary_ids = model.generate(inputs["input_ids"], max_length=max_length, min_length=50, num_beams=4,
                                 length_penalty=2.0, early_stopping=True)

    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return summary
