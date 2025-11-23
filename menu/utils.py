from .models import MenuItem, CartItem

def merge_cart_on_login(request, user):
    """
    1. Get items from the anonymous session.
    2. Get items from the user's database cart.
    3. Merge them (Session items overwrite DB items if duplicates exist).
    4. Save everything back to DB and Session.
    """
    session_basket = request.session.get('basket', {})
    
    # 1. Loop through Session Basket and save/update to DB
    for item_id, quantity in session_basket.items():
        if item_id.isdigit():
            # Get or Create in DB
            cart_item, created = CartItem.objects.get_or_create(
                user=user, 
                menu_item_id=int(item_id),
                defaults={'quantity': int(quantity)}
            )
            if not created:
                # If it existed in DB, update with the session quantity (fresh data)
                cart_item.quantity = int(quantity)
                cart_item.save()

    # 2. Now, load the FULL database cart back into the Session
    # (This pulls in items they might have saved on a different device)
    db_cart = CartItem.objects.filter(user=user)
    new_session_basket = {}
    
    for db_item in db_cart:
        new_session_basket[str(db_item.menu_item.id)] = db_item.quantity
        
    # 3. Update the request session
    request.session['basket'] = new_session_basket
    request.session.modified = True