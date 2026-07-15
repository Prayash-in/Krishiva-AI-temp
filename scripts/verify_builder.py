from engine.retrieval.formatting.builder import TextBuilder

builder = TextBuilder()

builder.field("Crop", "Rice")
builder.field("Problem", "Rice Blast")

builder.section("Symptoms")

builder.bullets(
    [
        "Yellow spot",
        "Gray lesion",
        "Brown border",
    ]
)

builder.section("Visual Description")

builder.text(
    "Diamond-shaped lesions with gray centre."
)

print(builder.build())