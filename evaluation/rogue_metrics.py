from rouge_score import rouge_scorer


def get_accuracy(ground_truth, model_summary):
    """
    function to get rogue score as a accuracy metrics.
    :param ground_truth: str
    :param model_summary: str
    :return: scores: list
    """
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)
    scores = scorer.score(ground_truth,model_summary)

    return scores
