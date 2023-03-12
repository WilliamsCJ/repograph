from datasets import load_dataset
from transformers import T5ForConditionalGeneration, RobertaTokenizer
from sentence_transformers import SentenceTransformer, util

import pandas as pd

dataset = load_dataset("code_x_glue_ct_code_to_text", "python")

df = pd.DataFrame(dataset['test'])

tokenizer = RobertaTokenizer.from_pretrained("Salesforce/codet5-base")
model = T5ForConditionalGeneration.from_pretrained("Salesforce/codet5-base-multi-sum")
cosine_model = SentenceTransformer("sentence-transformers/multi-qa-distilbert-cos-v1")
finetuned_model = T5ForConditionalGeneration.from_pretrained(
    "stmnk/codet5-small-code-summarization-python")


counter = 1
counter_fine = 1


def summarize(code_tokens):
    global counter
    counter += 1
    input_ids = tokenizer(' '.join(code_tokens), return_tensors='pt').input_ids
    generated_ids = model.generate(input_ids, max_length=200)
    return tokenizer.decode(generated_ids[0], skip_special_tokens=True)


def summarize_finetuned(code_tokens):
    global counter_fine
    counter_fine += 1
    input_ids = tokenizer(' '.join(code_tokens), return_tensors='pt').input_ids
    generated_ids = finetuned_model.generate(input_ids, max_length=200)
    return tokenizer.decode(generated_ids[0], skip_special_tokens=True)

df['summarization'] = df['code_tokens'].apply(summarize)
df['summarization_finetuned'] = df['code_tokens'].apply(summarize_finetuned)


def compare(summarization, docstring):
    embedding_1 = cosine_model.encode(summarization)
    embedding_2 = cosine_model.encode([docstring, ""])
    score = util.dot_score(embedding_1, embedding_2)[0].cpu().tolist()[0]
    return abs(score)


df['score'] = df.apply(lambda x: compare(x.summarization, ' '.join(x.docstring_tokens)), axis=1)
df['finetuned_score'] = df.apply(
    lambda x: compare(x.summarization_finetuned, ' '.join(x.docstring_tokens)), axis=1)

df['score'].mean()
df['finetuned_score'].mean()
