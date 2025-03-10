# ========================================
# GraphQLAggregateSimple
# ========================================

# START-ANY
import weaviate
import weaviate.classes as wvc
import os

client = weaviate.connect_to_local()

# END-ANY


# Actual client instantiation
client = weaviate.connect_to_wcs(
    cluster_url=os.getenv("WCS_DEMO_URL"),
    auth_credentials=weaviate.AuthApiKey(os.getenv("WCS_DEMO_RO_KEY")),
    headers={"X-OpenAI-Api-Key": os.getenv("OPENAI_APIKEY")},
)


# START GraphQLAggregateSimple
collection = client.collections.get("Article")
response = collection.aggregate.over_all(
    total_count=True,
    return_metrics=wvc.Metrics("wordCount").integer(
        count=True,
        maximum=True,
        mean=True,
        median=True,
        minimum=True,
        mode=True,
        sum_=True,
    ),
)

print(response.total_count)
print(response.properties)
# END GraphQLAggregateSimple

# TEST
assert "wordCount" in response.properties.keys()
assert response.total_count > 0


# ========================================
# GraphQLMetaCount
# ========================================

# START GraphQLMetaCount
collection = client.collections.get("Article")
response = collection.aggregate.over_all(total_count=True)

print(response.total_count)
# END GraphQLMetaCount

# TEST
assert response.total_count > 0


# ========================================
# GraphQLSimpleAggregateGroupby
# ========================================

# START GraphQLSimpleAggregateGroupby
collection = client.collections.get("Article")
response = collection.aggregate_group_by.over_all(
    group_by="inPublication",
    total_count=True,
    return_metrics=wvc.Metrics("wordCount").integer(mean=True)
)

for g in response:
    print(g.total_count)
    print(g.properties)
    print(g.grouped_by)
# END GraphQLSimpleAggregateGroupby

    # TEST
    assert g.total_count > 0
    assert "wordCount" in g.properties.keys()
    assert "inPublication" == g.grouped_by.prop


# ========================================
# GraphQLnearObjectAggregate
# ========================================

# START GraphQLnearObjectAggregate
collection = client.collections.get("Article")
response = collection.aggregate.near_object(
    near_object="00037775-1432-35e5-bc59-443baaef7d80",
    distance=0.6,
    object_limit=200,
    total_count=True,
    return_metrics=[
        wvc.Metrics("wordCount").integer(
            count=True,
            maximum=True,
            mean=True,
            median=True,
            minimum=True,
            mode=True,
            sum_=True,
        ),
        wvc.Metrics("inPublication").reference(
            pointing_to=True,
        )
    ]
)

print(response.total_count)
print(response.properties)
# END GraphQLnearObjectAggregate

# TEST
assert "inPublication" in response.properties.keys()
assert "wordCount" in response.properties.keys()
assert response.total_count > 0


# ========================================
# GraphQLnearVectorAggregate
# ========================================

collection = client.collections.get("Article")
rand_obj = collection.query.fetch_objects(limit=1, include_vector=True)
some_vector = rand_obj.objects[0].vector

# START GraphQLnearVectorAggregate
collection = client.collections.get("Article")
response = collection.aggregate.near_vector(
    near_vector=some_vector,
    distance=0.7,
    object_limit=100,
    total_count=True,
    return_metrics=[
        wvc.Metrics("wordCount").integer(
            count=True,
            maximum=True,
            mean=True,
            median=True,
            minimum=True,
            mode=True,
            sum_=True,
        ),
        wvc.Metrics("inPublication").reference(
            pointing_to=True,
        )
    ]
)

print(response.total_count)
print(response.properties)
# END GraphQLnearVectorAggregate

# TEST
assert "inPublication" in response.properties.keys()
assert "wordCount" in response.properties.keys()
assert response.total_count > 0


# ========================================
# GraphQLnearTextAggregate
# ========================================

collection = client.collections.get("Article")
rand_obj = collection.query.fetch_objects(limit=1, include_vector=True)
some_vector = rand_obj.objects[0].vector

# START GraphQLnearTextAggregate
collection = client.collections.get("Article")
response = collection.aggregate.near_text(
    query="apple iphone",
    distance=0.7,
    object_limit=200,
    total_count=True,
    return_metrics=[
        wvc.Metrics("wordCount").integer(
            count=True,
            maximum=True,
            mean=True,
            median=True,
            minimum=True,
            mode=True,
            sum_=True,
        ),
        wvc.Metrics("inPublication").reference(
            pointing_to=True,
        )
    ]
)

print(response.total_count)
print(response.properties)
# END GraphQLnearTextAggregate

# TEST
assert "inPublication" in response.properties.keys()
assert "wordCount" in response.properties.keys()
assert response.total_count > 0
