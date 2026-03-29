# AI Prompting Rules

* **Always return structured JSON**: The output format must be exclusively valid JSON that conforms to the requested schema. Do not include markdown formatting or additional explanation text around the JSON object.
* **Do not hallucinate fields**: Only include the fields requested. Avoid making up new attributes or changing the expected structure.
* **Follow schema strictly**: The output must exactly match the data types, enumerations, and requirements of the specified schema (e.g. priorities must be one of LOW, MEDIUM, or HIGH).
