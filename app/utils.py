PRICES = {
    "black_white": 2.00,
    "colored": 5.00,
    "photo": 20.00,
}


def compute_cost(pages: int, paper_type: str) -> float:
    price = PRICES.get(paper_type)
    if price is None:
        raise ValueError(f"Unknown paper type: {paper_type}")
    return round(pages * price, 2)


def get_pricing() -> dict[str, float]:
    return dict(PRICES)
