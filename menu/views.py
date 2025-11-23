import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.humanize.templatetags.humanize import intcomma
from django.db.models import Prefetch
from .models import Category, MenuItem, CartItem
from accounts.models import Favorite 

# --- 🛠️ HELPER: Safe Cart Counter ---
def get_cart_count(session):
    """
    Safely counts total quantity of items in the session basket.
    Ignores non-numeric keys (like '_auth_user_id') to prevent errors.
    """
    basket = session.get('basket', {})
    if not isinstance(basket, dict):
        return 0
        
    count = 0
    for key, quantity in basket.items():
        # Only count if the key represents a MenuItem ID (digits)
        if str(key).isdigit():
            count += int(quantity)
            
    return count

# --- 🍽️ VIEW: Main Menu ---
def menu_view(request):
    """
    Renders the single-page menu with categories and items ordered by priority.
    """
    # 1. Efficiently fetch Categories + Items (Ordered by 'priority')
    items_prefetch = Prefetch(
        'items', 
        queryset=MenuItem.objects.order_by('priority'),
        to_attr='menu_items'
    )
    categories = Category.objects.order_by('priority').prefetch_related(items_prefetch)
    
    # 2. Get Cart Count for the Badge
    cart_count = get_cart_count(request.session)

    # 3. Get User Favorites (List of IDs) for the Red Hearts
    user_favorites = []
    if request.user.is_authenticated:
        user_favorites = request.user.favorites.values_list('item_id', flat=True)

    context = {
        'categories': categories,
        'cart_count': cart_count,
        'user_favorites': user_favorites,
    }
    return render(request, "index.html", context)

# --- 🛒 API: Add Item to Basket (AJAX) ---
@require_POST
def add_to_basket_api(request):
    try:
        data = json.loads(request.body)
        item_id = data.get('id')
        
        # Verify item exists
        item = get_object_or_404(MenuItem, id=item_id)
        
        # Get & Update Basket
        basket = request.session.get('basket', {})
        basket_key = str(item_id)
        
        # Simple logic: Add 1
        basket[basket_key] = basket.get(basket_key, 0) + 1
        
        # Save Session
        request.session['basket'] = basket
        request.session.modified = True 
        
        if request.user.is_authenticated:
            cart_item, created = CartItem.objects.get_or_create(
                user=request.user, 
                menu_item=item
            )
            cart_item.quantity = basket[str(item.id)] # Sync quantity
            cart_item.save()
        
        # Calculate new total
        new_total = get_cart_count(request.session)
        
        return JsonResponse({
            'success': True,
            'cart_total': new_total,
            'item_name': item.name
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

# --- 🔄 API: Update/Remove Item in Basket Page (AJAX) ---
@require_POST
def update_basket_api(request):
    try:
        data = json.loads(request.body)
        item_id = str(data.get('id'))
        action = data.get('action') # 'increase' or 'decrease'
        
        basket = request.session.get('basket', {})
        
        if item_id in basket:
            if action == 'increase':
                basket[item_id] += 1
            elif action == 'decrease':
                basket[item_id] -= 1
                if basket[item_id] < 1:
                    del basket[item_id] # Remove if 0
            
            request.session['basket'] = basket
            request.session.modified = True
            
            if request.user.is_authenticated:
                if item_id in basket:
                    current_qty = basket[item_id]
                    cart_item, created = CartItem.objects.get_or_create(
                        user=request.user,
                        menu_item_id=int(item_id)
                    )
                    cart_item.quantity = current_qty
                    cart_item.save()
                else:
                    CartItem.objects.filter(
                        user=request.user, 
                        menu_item_id=int(item_id)
                    ).delete()
            
            cart_count = get_cart_count(request.session)
            
            total_price = 0
            for k, v in basket.items():
                if k.isdigit():
                    i = MenuItem.objects.get(id=k)
                    total_price += i.price * v
            
            discount_amount = 0
            final_total = total_price
            if request.user.is_authenticated:
                discount_amount = int(total_price * 0.05)
                final_total = total_price - discount_amount

            item_total = 0
            new_qty = 0
            if item_id in basket:
                item = MenuItem.objects.get(id=item_id)
                new_qty = basket[item_id]
                item_total = item.price * new_qty

            return JsonResponse({
                'success': True,
                'new_quantity': new_qty,
                'item_total': intcomma(item_total),
                'cart_total': intcomma(total_price),
                'discount_amount': intcomma(discount_amount),
                'final_total': intcomma(final_total),
                'total_items': cart_count
            })
            
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'success': False}, status=400)


# --- ❤️ API: Toggle Favorite (AJAX) ---
@login_required
@require_POST
def toggle_favorite(request):
    try:
        data = json.loads(request.body)
        item_id = data.get('item_id')
        item = get_object_or_404(MenuItem, id=item_id)
        
        favorite, created = Favorite.objects.get_or_create(user=request.user, item=item)
        
        if not created:
            favorite.delete()
            is_favorited = False
            msg = "از علاقه مندی ها حذف شد"
        else:
            is_favorited = True
            msg = "به علاقه مندی ها اضافه شد"
            
        # Note the key: 'is_favorited' (with a 'd')
        return JsonResponse({'success': True, 'is_favorited': is_favorited, 'message': msg})
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


# --- 🛒 VIEW: Basket Page ---
def view_basket(request):
    basket = request.session.get('basket', {})
    items_data = []
    total = 0

    for item_id, quantity in basket.items():
        if not item_id.isdigit(): continue
        try:
            item = MenuItem.objects.get(id=item_id)
            item_total = item.price * quantity
            total += item_total
            items_data.append({'item': item, 'quantity': quantity, 'total_price': item_total})
        except MenuItem.DoesNotExist:
            continue

    discount_amount = 0
    final_total = total
    
    if request.user.is_authenticated and total > 0:
        discount_amount = int(total * 0.05)
        final_total = total - discount_amount
        
    context = {
        'items_data': items_data,
        'total': total,
        'discount_amount': discount_amount,
        'final_total': final_total,
        'cart_count': get_cart_count(request.session),
    }
    return render(request, 'basket.html', context)

def clear_basket(request):
    if 'basket' in request.session:
        del request.session['basket']
    return redirect('menu:basket')