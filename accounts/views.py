import json
import random
import time 
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_http_methods
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from kavenegar import *
from decouple import config
from menu.models import MenuItem
from menu.utils import merge_cart_on_login
from .models import Profile, Favorite
from .forms import RegisterForm


@login_required
@require_POST
def toggle_favorite(request):
    try:
        data = json.loads(request.body)
        item_id = data.get('item_id')
        item = get_object_or_404(MenuItem, id=item_id)
        
        # Check if it exists
        favorite, created = Favorite.objects.get_or_create(user=request.user, item=item)
        
        if not created:
            # If it already existed, the user clicked again to REMOVE it
            favorite.delete()
            is_favorited = False 
            msg = "از علاقه مندی ها حذف شد"
        else:
            # It was created
            is_favorited = True 
            msg = "به علاقه مندی ها اضافه شد"
            
        return JsonResponse({'success': True, 'is_favorited': is_favorited, 'message': msg})
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
    
    
# def register_view(request):
#     if request.user.is_authenticated:
#         return redirect('menu:menu_view')

#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('menu:menu_view')
#     else:
#         form = RegisterForm()
    
#     return render(request, 'register.html', {'form': form})

#------------------------------------------------------------------------


def login_view(request):
    MY_KAVENEGAR_API_KEY=config('MY_KAVENEGAR_API_KEY', default=None)
    
    if request.user.is_authenticated:
        return redirect('menu:menu_view')

    if request.method == 'POST':
        phone = request.POST.get('phone')
        
        if phone and phone.startswith('09') and len(phone) == 11:
            otp = random.randint(1000, 9999)
            
            expiry_time = int(time.time()) + 120
            
            request.session['otp'] = otp
            request.session['phone'] = phone
            request.session['otp_expiry'] = expiry_time 
            
            # --- SMS LOGIC (Real + Console Fallback) ---
            '''
            With Kavenegar's free service (basic sign-up), you can only use sms_send with the specified params.
            For example, the receptor can only be the phone number you registered with, so be cautious about how you use it.
            For more details, thoroughly read your Kavenegar homepage and their GitHub page.
            '''
            try:
                api = KavenegarAPI(MY_KAVENEGAR_API_KEY)
                # params = {
                #     'receptor': phone,
                #     'template': 'verify', 
                #     'token': str(otp),
                #     'type': 'sms'
                # }
                # api.verify_lookup(params)
                params = {
                    'sender': '2000660110',
                    'receptor': phone,
                    'message':f'Here is your OTP code for ROYAL TEHRAN Restaurant: \n {str(str)}'
                }
                api.sms_send(params)
                print(f"✅ SMS SENT VIA API TO {phone}")
            except Exception as e:
                # Fallback for testing
                print(f"\n📩 ==================================")
                print(f"📩 ROYAL TEHRAN OTP: {otp}")
                print(f"📩 (Valid for 2 minutes)")
                print(f"📩 ==================================\n")
            
            return redirect('accounts:verify_otp')
        else:
            return render(request, 'accounts/login_otp.html', {'error': 'شماره موبایل نامعتبر است'})

    return render(request, 'accounts/login_otp.html')


def verify_otp_view(request):
    phone = request.session.get('phone')
    generated_otp = request.session.get('otp')
    expiry_time = request.session.get('otp_expiry')

    # 1. Security Check: If no session data, kick them out
    if not phone or not generated_otp or not expiry_time:
        return redirect('accounts:login')

    # 2. Calculate Time Remaining
    current_time = int(time.time())
    time_remaining = expiry_time - current_time

    # 3. Handle Expiration
    if time_remaining <= 0:
        del request.session['otp']
        del request.session['otp_expiry']
        return render(request, 'accounts/login_otp.html', {'error': 'کد تایید منقضی شده است. لطفا مجددا تلاش کنید.'})

    if request.method == 'POST':
        entered_code = request.POST.get('code')
        
        if entered_code == str(generated_otp):
            # Code is Correct! Login/Create User
            try:
                profile = Profile.objects.get(phone_number=phone)
                user = profile.user
            except Profile.DoesNotExist:
                user = User.objects.create_user(username=phone)
                Profile.objects.create(user=user, phone_number=phone)
            
            login(request, user)
            merge_cart_on_login(request, user)
            
            # Clean session
            if 'otp' in request.session: del request.session['otp']
            if 'phone' in request.session: del request.session['phone']
            if 'otp_expiry' in request.session: del request.session['otp_expiry']
            
            return redirect('menu:menu_view')
        else:
            return render(request, 'accounts/verify_otp.html', {
                'phone': phone, 
                'error': 'کد وارد شده اشتباه است',
                'time_remaining': time_remaining # Pass time back so timer doesn't reset visually
            })

    return render(request, 'accounts/verify_otp.html', {
        'phone': phone,
        'time_remaining': time_remaining
    })

# --- 3. PROFILE VIEW (Task 2) ---
def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
        
    favorites = Favorite.objects.filter(user=request.user).select_related('item')
    
    context = {
        'profile': request.user.profile,
        'favorites': favorites
    }
    return render(request, 'accounts/profile.html', context)