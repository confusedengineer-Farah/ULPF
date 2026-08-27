from typing import Any


def detect_plugin(
    parsed_data: dict[str, Any],
    log_format: str,
    plugins: list[dict[str, Any]],
) -> dict[str, Any]:

    best_plugin = None
    best_score = 0
    best_matches: list[str] = []

    parsed_fields = set(parsed_data.keys())

    for plugin in plugins:

        if plugin.get("format") != log_format:
            continue

        score = 1
        matches: list[str] = ["format"]

        # Vendor matching
        plugin_vendor = plugin.get("vendor")
        parsed_vendor = parsed_data.get("vendor")

        if plugin_vendor and parsed_vendor:

            if plugin_vendor.lower() == str(parsed_vendor).lower():
                score += 3
                matches.append("vendor")
            else:
                continue

        # Product matching
        plugin_product = plugin.get("product")
        parsed_product = parsed_data.get("product")

        if plugin_product and parsed_product:

            if plugin_product.lower() == str(parsed_product).lower():
                score += 3
                matches.append("product")
            else:
                continue

        # Required fields
        match_config = plugin.get("match", {})

        required_fields = set(
            match_config.get("required_fields", [])
        )

        if required_fields:

            matched_fields = required_fields.intersection(
                parsed_fields
            )

            if not required_fields.issubset(parsed_fields):
                continue

            score += len(matched_fields)

            matches.append(
                f"required_fields:{len(matched_fields)}"
            )

        if score > best_score:

            best_score = score
            best_plugin = plugin.get("id")
            best_matches = matches

    if best_plugin is None:

        return {
            "plugin_id": None,
            "score": 0,
            "confidence": 0.0,
            "matched_by": [],
        }

    # Simple MVP confidence calculation
    confidence = min(best_score / 10, 1.0)

    return {
        "plugin_id": best_plugin,
        "score": best_score,
        "confidence": round(confidence, 2),
        "matched_by": best_matches,
    }