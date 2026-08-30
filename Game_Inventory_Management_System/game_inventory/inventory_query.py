from .config import inventory_db

def query_inventory(search_query="", rarity=None, limit=50, offset=0):
    results = []
    search_query = search_query.lower()
    
    for sku, item in inventory_db.items():
        matches_query = search_query in item["name"].lower() or search_query in sku.lower()
        matches_rarity = (rarity is None) or (item["rarity"] == rarity)
        
        if matches_query and matches_rarity:
            # Output matching rows representation structure
            results.append((sku, item["name"], item["category"], item["rarity"], item["quantity"], item["threshold"], item["price"]))
            
    paginated_results = results[offset : offset + limit]
    return paginated_results
