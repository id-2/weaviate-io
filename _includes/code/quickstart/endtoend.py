# DockerInstantiationExample
import weaviate
import weaviate.classes as wvc
import os

client = weaviate.connect_to_local(
    port=8080,
    grpc_port=50051,
    headers={
        "X-OpenAI-Api-Key": os.environ["OPENAI_APIKEY"]  # Replace with your inference API key
    }
)
# END DockerInstantiationExample

assert client.is_ready()

# EndToEndExample  # InstantiationExample  # NearTextExample
import weaviate
import weaviate.classes as wvc
# END EndToEndExample  # END InstantiationExample  # END NearTextExample
# ===== import data =====  # EndToEndExample
import requests
import json
import os

# END EndToEndExample  # Test import

# TODO -> Replace this with WCS example when sandbox ready
# EndToEndExample  # InstantiationExample  # NearTextExample

# As of November 2023, we are working towards making all WCS instances compatible with the new API introduced in the v4 Python client.
# Accordingly, we show you how to connect to a local instance of Weaviate.
# Here, authentication is switched off, which is why you do not need to provide the Weaviate API key.
client = weaviate.connect_to_local(
    port=8080,
    grpc_port=50051,
    headers={
        "X-OpenAI-Api-Key": os.environ["OPENAI_APIKEY"]  # Replace with your inference API key
    }
)

# END EndToEndExample  # END InstantiationExample  # END NearTextExample

assert client.is_ready()

client.collections.delete("Question")

# EndToEndExample
# ===== define collection =====
questions = client.collections.create(
    name="Question",
    vectorizer_config=wvc.Configure.Vectorizer.text2vec_openai(),  # If set to "none" you must always provide vectors yourself. Could be any other "text2vec-*" also.
    generative_config=wvc.Configure.Generative.openai()  # Ensure the `generative-openai` module is used for generative queries
)

# ===== import data =====
resp = requests.get('https://raw.githubusercontent.com/weaviate-tutorials/quickstart/main/data/jeopardy_tiny.json')
data = json.loads(resp.text)  # Load data

question_objs = list()
for i, d in enumerate(data):
    question_objs.append({
        "answer": d["Answer"],
        "question": d["Question"],
        "category": d["Category"],
    })

questions = client.collections.get("Question")
questions.data.insert_many(question_objs)  # This uses batching under the hood

# END EndToEndExample    # Test import
questions_definition = questions.config.get()
obj_count = questions.aggregate.over_all(total_count=True)

assert questions_definition.name == "Question"
assert obj_count.total_count == 10

# NearTextExample
questions = client.collections.get("Question")

response = questions.query.near_text(
    query="biology",
    limit=2
)

print(response.objects[0].properties)  # Inspect the first object
# END NearTextExample

# ===== Test query responses =====
assert len(response.objects) == 2
assert response.objects[0].properties["answer"] == "DNA"

# NearTextWhereExample
questions = client.collections.get("Question")

response = questions.query.near_text(
    query="biology",
    limit=2,
    filters=wvc.Filter(path="category").equal("ANIMALS")
)

print(response.objects[0].properties)  # Inspect the first object
# END NearTextWhereExample

# ===== Test query responses =====
assert len(response.objects) == 2
assert response.objects[0].properties["category"] == "ANIMALS"


# GenerativeSearchExample
questions = client.collections.get("Question")

response = questions.generate.near_text(
    query="biology",
    limit=2,
    single_prompt="Explain {answer} as you might to a five-year-old."
)

print(response.objects[0].generated)  # Inspect the generated text
# END GenerativeSearchExample

# ===== Test query responses =====
assert len(response.objects) == 2
assert len(response.objects[0].generated) > 0

# GenerativeSearchGroupedTaskExample
questions = client.collections.get("Question")

response = questions.generate.near_text(
    query="biology",
    limit=2,
    grouped_task="Write a tweet with emojis about these facts."
)

print(response.generated)  # Inspect the generated text
# END GenerativeSearchGroupedTaskExample

# ===== Test query responses =====
assert len(response.objects) == 2
assert len(response.generated) > 0

# Cleanup

client.collections.delete("Question")  # Cleanup after


# ===== import with custom vectors =====
import requests

# highlight-start
fname = "jeopardy_tiny_with_vectors_all-OpenAI-ada-002.json"  # This file includes pre-generated vectors
# highlight-end
url = f"https://raw.githubusercontent.com/weaviate-tutorials/quickstart/main/data/{fname}"
resp = requests.get(url)
data = json.loads(resp.text)  # Load data

question_objs = list()
for i, d in enumerate(data):
    question_objs.append(wvc.DataObject(
        properties={
            "answer": d["Answer"],
            "question": d["Question"],
            "category": d["Category"],
        },
        vector=d["vector"]
    ))

questions = client.collections.get("Question")
questions.data.insert_many(question_objs)    # This uses batching under the hood
# ===== END import with custom vectors =====

questions_definition = questions.config.get()
obj_count = questions.aggregate.over_all(total_count=True)

assert questions_definition.name == "Question"
assert obj_count.total_count == 10

client.collections.delete("Question")  # Cleanup after
