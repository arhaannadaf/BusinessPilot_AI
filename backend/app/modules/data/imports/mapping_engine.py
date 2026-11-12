import re
from typing import Any


# This is the platform vocabulary, not a list of source-column mappings.
# Source headers are scored against field names, meaning, and data type.
CANONICAL_FIELDS: tuple[dict[str, Any], ...] = (
    {
        "id": "customer_identifier",
        "label": "Customer Identifier",
        "description": "A stable code or key used to identify a customer or account.",
        "type": "text",
        "terms": ("customer", "client", "account", "identifier", "id", "code", "key"),
    },
    {
        "id": "customer_name",
        "label": "Customer Name",
        "description": "The displayed name of a customer, client, or account.",
        "type": "text",
        "terms": ("customer", "client", "account", "name", "title"),
    },
    {
        "id": "annual_value",
        "label": "Annual Value",
        "description": "A yearly business value; its exact meaning may require confirmation.",
        "type": "decimal",
        "terms": ("annual", "yearly", "value", "amount"),
    },
    {
        "id": "creation_date",
        "label": "Creation Date",
        "description": "The date a customer, record, or business object was created.",
        "type": "date",
        "terms": ("created", "creation", "entry", "added", "date"),
    },
    {
        "id": "status",
        "label": "Status",
        "description": "A lifecycle state or current standing.",
        "type": "text",
        "terms": ("status", "state", "stage", "lifecycle"),
    },
)


def _tokens(value: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", value.casefold()))


def _type_compatibility(source_type: str, target_type: str) -> float:
    if source_type in {"unknown", "mixed"}:
        return 0.5
    if source_type == target_type:
        return 1.0
    if source_type == "integer" and target_type == "decimal":
        return 0.8
    return 0.0


def suggest_mappings(schema: dict[str, Any]) -> list[dict[str, Any]]:
    results = []
    for column in schema.get("columns", []):
        source_tokens = _tokens(column.get("source_name", ""))
        candidates = []
        for field in CANONICAL_FIELDS:
            field_tokens = _tokens(f"{field['label']} {field['description']}") | set(field["terms"])
            overlap = source_tokens & field_tokens
            lexical_score = len(overlap) / max(len(source_tokens), 1)
            type_score = _type_compatibility(
                column.get("inferred_type", "unknown"), field["type"]
            )
            if not overlap or type_score == 0:
                continue
            score = round(0.75 * lexical_score + 0.25 * type_score, 2)
            candidates.append({
                "field_id": field["id"],
                "label": field["label"],
                "description": field["description"],
                "confidence": score,
                "evidence": {
                    "matching_terms": sorted(overlap),
                    "source_type": column.get("inferred_type", "unknown"),
                    "type_compatible": type_score > 0,
                },
                "requires_review": True,
            })
        candidates.sort(key=lambda candidate: candidate["confidence"], reverse=True)
        results.append({
            **column,
            "mapping_status": "pending",
            "canonical_field_id": None,
            "requires_human_review": True,
            "suggestions": candidates[:3],
        })
    return results
