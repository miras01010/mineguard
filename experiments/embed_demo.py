from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

sentences = [
    "Persons must be withdrawn if inflammable gas exceeds the permitted limit.",
    "Workers have to leave the mine when there is too much methane.",
    "The manager shall maintain a register of attendance.",
]

embeddings = model.encode(sentences)
print("Shape:", embeddings.shape)
print("First 5 numbers of sentence 1:", embeddings[0][:5])

scores = util.cos_sim(embeddings, embeddings)
print(scores)