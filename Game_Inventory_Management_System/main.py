import game_inventory

def main():
    game_inventory.init_inventory()
    
    print("Adding items...")
    game_inventory.add_item(
        name="Epic Sword of Fire",
        sku="SW-FIRE-001",
        category="Weapons",
        rarity="Epic",
        quantity=10,
        threshold=3,
        price=150.0
    )
    
    game_inventory.add_item(
        name="Health Potion",
        sku="POT-HEAL-002",
        category="Consumables",
        rarity="Common",
        quantity=2,
        threshold=5,
        price=10.0
    )
    
    print("\nChecking inventory stock alerts:")
    game_inventory.check_item_alert(sku="POT-HEAL-002")
    
    print("\nUpdating stock (using Health Potion)...")
    game_inventory.update_stock(sku="POT-HEAL-002", quantity_delta=5)
    
    print("\nQuerying weapons in inventory:")
    items = game_inventory.query_inventory(search_query="Sword", rarity="Epic")
    for item in items:
        print(item)

if __name__ == "__main__":
    main()
