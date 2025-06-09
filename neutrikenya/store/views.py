from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Avg, Count, Min, Max
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import Category, Product, Cart, CartItem, Order, OrderItem
from .forms import SignUpForm, UserProfileForm
import uuid
from django.core.paginator import Paginator

def get_or_create_cart(request):
    """Create or retrieve a cart for the user."""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_id = request.session.get('session_id')
        if not session_id:
            session_id = str(uuid.uuid4())
            request.session['session_id'] = session_id
        
        cart, created = Cart.objects.get_or_create(session_id=session_id)
    
    return cart

def home(request):
    """Home page view showing featured products and collections."""
    # Get featured and bestselling products
    featured_products = Product.objects.filter(
        featured=True, 
        is_available=True
    ).order_by('-created_at')[:8]
    
    # Get Vitamin C products
    vitamin_c_products = Product.objects.filter(
        product_line='Vitamin C',
        is_available=True
    ).order_by('-created_at')[:4]
    
    # Get Retinol products
    retinol_products = Product.objects.filter(
        product_line='Retinol',
        is_available=True
    ).order_by('-created_at')[:4]
    
    # Get main categories
    main_categories = Category.objects.filter(parent=None)
    
    context = {
        'featured_products': featured_products,
        'vitamin_c_products': vitamin_c_products,
        'retinol_products': retinol_products,
        'main_categories': main_categories,
        'meta_title': 'NeutriherbsKenya - Natural Skincare Products',
        'meta_description': 'Discover our range of natural skincare products for all your beauty needs. Shop Vitamin C, Retinol, and more.',
    }
    return render(request, 'store/home.html', context)

def shop(request):
    """Shop page showing all available products with advanced filtering and sorting."""
    # Start with all available products
    products = Product.objects.filter(is_available=True)
    
    # Filter by category
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(
            Q(category=category) | Q(category__parent=category)
        )
    
    # Filter by product line
    product_line = request.GET.get('line')
    if product_line:
        products = products.filter(product_line=product_line)
    
    # Filter by price range
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        try:
            products = products.filter(price__gte=float(min_price))
        except ValueError:
            pass
    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except ValueError:
            pass
    
    # Search functionality with improved relevance
    search_query = request.GET.get('q')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__name__icontains=search_query) |
            Q(product_line__icontains=search_query)
        ).distinct()
    
    # Advanced sorting
    sort = request.GET.get('sort', 'default')
    if sort == 'price_low':
        products = products.order_by('price')
    elif sort == 'price_high':
        products = products.order_by('-price')
    elif sort == 'newest':
        products = products.order_by('-created_at')
    elif sort == 'bestseller':
        products = products.filter(is_bestseller=True)
    elif sort == 'featured':
        products = products.filter(featured=True)
    elif sort == 'name_asc':
        products = products.order_by('name')
    elif sort == 'name_desc':
        products = products.order_by('-name')
    
    categories = Category.objects.filter(parent=None)
    
    # Get unique product lines for filtering
    product_lines = [
        'Beauty Tool',
        'Collagen',
        'Deeply Cleansing',
        'Feminine Care',
        'Hyaluronic Acid',
        'PRO Retinol',
        'Salicylic Acid',
        'Skin Whitening',
        'Snail',
        'Sun Care',
        'Turmeric',
        'Vitamin C',
        'Vitamin E',
        'Weight Loss',
        '24K Luxury Gold'
    ]
    
    # Get price range for the filter
    price_range = products.aggregate(min_price=Min('price'), max_price=Max('price'))
    
    # Pagination
    page = request.GET.get('page', 1)
    items_per_page = request.GET.get('items_per_page', 12)
    paginator = Paginator(products, items_per_page)
    products_page = paginator.get_page(page)
    
    context = {
        'products': products_page,
        'categories': categories,
        'product_lines': product_lines,
        'current_category': request.GET.get('category'),
        'current_line': request.GET.get('line'),
        'search_query': request.GET.get('q'),
        'current_sort': request.GET.get('sort', 'default'),
        'price_range': price_range,
        'min_price_filter': min_price,
        'max_price_filter': max_price,
        'items_per_page': items_per_page,
        'sort_options': [
            {'value': 'default', 'label': 'Default'},
            {'value': 'price_low', 'label': 'Price: Low to High'},
            {'value': 'price_high', 'label': 'Price: High to Low'},
            {'value': 'newest', 'label': 'Newest First'},
            {'value': 'bestseller', 'label': 'Bestsellers'},
            {'value': 'featured', 'label': 'Featured'},
            {'value': 'name_asc', 'label': 'Name: A to Z'},
            {'value': 'name_desc', 'label': 'Name: Z to A'},
        ],
        'items_per_page_options': [12, 24, 36, 48]
    }
    
    return render(request, 'store/shop.html', context)

def category_detail(request, slug):
    """Category page showing all products in a category."""
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(
        Q(category=category) | Q(category__parent=category),
        is_available=True
    )
    subcategories = category.subcategories.all()
    
    context = {
        'category': category,
        'products': products,
        'subcategories': subcategories,
    }
    return render(request, 'store/category_detail.html', context)

def product_detail(request, slug):
    """Product detail page."""
    product = get_object_or_404(Product, slug=slug, is_available=True)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'store/product_detail.html', context)

def add_to_cart(request, product_id):
    """Add a product to the cart."""
    product = get_object_or_404(Product, id=product_id, is_available=True)
    cart = get_or_create_cart(request)
    
    quantity = int(request.POST.get('quantity', 1))
    
    # Check if product is already in cart
    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.quantity += quantity
        cart_item.save()
    except CartItem.DoesNotExist:
        CartItem.objects.create(cart=cart, product=product, quantity=quantity)
    
    messages.success(request, f"{product.name} added to your cart.")
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'item_count': cart.item_count,
            'total_price': cart.total_price,
        })
    
    return redirect('store:product_detail', slug=product.slug)

def update_cart_item(request, item_id):
    """Update quantity of a cart item."""
    cart_item = get_object_or_404(CartItem, id=item_id)
    
    # Ensure the cart belongs to the user
    cart = get_or_create_cart(request)
    if cart_item.cart.id != cart.id:
        messages.error(request, "You don't have permission to update this item.")
        return redirect('store:cart')
    
    quantity = int(request.POST.get('quantity', 1))
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
    else:
        cart_item.delete()
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'item_count': cart.item_count,
            'total_price': cart.total_price,
        })
    
    return redirect('store:cart')

def remove_from_cart(request, item_id):
    """Remove an item from the cart."""
    cart_item = get_object_or_404(CartItem, id=item_id)
    
    # Ensure the cart belongs to the user
    cart = get_or_create_cart(request)
    if cart_item.cart.id != cart.id:
        messages.error(request, "You don't have permission to remove this item.")
        return redirect('store:cart')
    
    cart_item.delete()
    messages.success(request, "Item removed from your cart.")
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'item_count': cart.item_count,
            'total_price': cart.total_price,
        })
    
    return redirect('store:cart')

def cart_view(request):
    """View cart contents."""
    cart = get_or_create_cart(request)
    context = {'cart': cart}
    return render(request, 'store/cart.html', context)

def checkout(request):
    """Checkout page."""
    cart = get_or_create_cart(request)
    
    if cart.item_count == 0:
        messages.warning(request, "Your cart is empty.")
        return redirect('store:cart')
    
    context = {'cart': cart}
    return render(request, 'store/checkout.html', context)

def place_order(request):
    """Process order placement."""
    if request.method != 'POST':
        return redirect('store:checkout')
    
    cart = get_or_create_cart(request)
    
    if cart.item_count == 0:
        messages.warning(request, "Your cart is empty.")
        return redirect('store:cart')
    
    # Get form data
    payment_method = request.POST.get('payment_method', 'mpesa')
    
    # Create order
    order = Order(
        user=request.user if request.user.is_authenticated else None,
        first_name=request.POST.get('first_name'),
        last_name=request.POST.get('last_name'),
        email=request.POST.get('email'),
        phone=request.POST.get('phone'),
        address=request.POST.get('address'),
        city=request.POST.get('city'),
        payment_method=payment_method,
        status='pending',
        delivery_instructions=request.POST.get('delivery_instructions', '')
    )
    order.save()
    
    # Create order items
    for cart_item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            price=cart_item.product.price,
            quantity=cart_item.quantity
        )
    
    # Store payment info if needed
    if payment_method == 'mpesa':
        # Store M-Pesa phone number
        mpesa_phone = request.POST.get('mpesa_phone')
        if mpesa_phone and request.user.is_authenticated:
            profile = request.user.profile
            profile.mpesa_phone = mpesa_phone
            profile.default_payment_method = 'mpesa'
            profile.save()
    elif payment_method == 'card':
        # Store last 4 digits of card for reference
        card_number = request.POST.get('card_number', '')
        if card_number and request.user.is_authenticated:
            # Only store last 4 digits for security
            last_four = card_number[-4:] if len(card_number) >= 4 else ''
            profile = request.user.profile
            profile.card_last_four = last_four
            profile.card_expiry = request.POST.get('card_expiry', '')
            profile.default_payment_method = 'card'
            profile.save()
    
    # Clear cart
    cart.items.all().delete()
    
    # Send order confirmation email (can be implemented later)
    
    messages.success(request, "Your order has been placed successfully!")
    return redirect('store:order_confirmation', order_id=order.id)

def order_confirmation(request, order_id):
    """Order confirmation page."""
    order = get_object_or_404(Order, id=order_id)
    
    # Security check to ensure order belongs to user or is accessible via session
    if request.user.is_authenticated:
        if order.user and order.user != request.user:
            messages.error(request, "You don't have permission to view this order.")
            return redirect('store:home')
    
    context = {'order': order}
    return render(request, 'store/order_confirmation.html', context)

def about(request):
    """About page."""
    return render(request, 'store/about.html', {})

def contact(request):
    """Contact page."""
    return render(request, 'store/contact.html')

def haircare(request):
    """Hair care products page."""
    # Find products in hair care category if it exists
    haircare_featured = []
    try:
        haircare_category = Category.objects.get(name__icontains='hair')
        haircare_featured = Product.objects.filter(
            Q(category=haircare_category) | 
            Q(category__parent=haircare_category) |
            Q(name__icontains='hair') |
            Q(description__icontains='hair')
        ).distinct()[:4]
    except Category.DoesNotExist:
        # If no hair category exists, just show products with 'hair' in the name
        haircare_featured = Product.objects.filter(
            Q(name__icontains='hair') | 
            Q(description__icontains='hair')
        ).distinct()[:4]
    
    context = {
        'haircare_featured': haircare_featured,
    }
    return render(request, 'store/haircare.html', context)

def signup(request):
    """Handle user registration."""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in after registration
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Registration successful! Welcome to NeutriKenya.")
            return redirect('store:home')
    else:
        form = SignUpForm()
    
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def profile(request):
    """Display user profile and order history."""
    # Handle form submission
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('store:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    # Get user's orders
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    # Determine if user has all required info for checkout
    profile_complete = False
    payment_complete = False
    if hasattr(request.user, 'profile'):
        profile = request.user.profile
        profile_complete = profile.has_complete_shipping_info()
        payment_complete = profile.has_complete_payment_info()
    
    context = {
        'user': request.user,
        'form': form,
        'orders': orders,
        'profile_complete': profile_complete,
        'payment_complete': payment_complete,
        'active_tab': request.GET.get('tab', 'profile')  # Default to profile tab
    }
    return render(request, 'store/profile.html', context)

@login_required
def order_detail(request, order_id):
    """Display details of a specific order."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    context = {
        'order': order
    }
    return render(request, 'store/order_detail.html', context)

@receiver(user_logged_in)
def merge_carts_on_login(sender, user, request, **kwargs):
    """
    When a user logs in, if they have items in a session-based cart,
    transfer those items to their user account cart.
    """
    session_id = request.session.get('session_id')
    if not session_id:
        return
    
    try:
        # Get the session cart
        session_cart = Cart.objects.get(session_id=session_id)
        
        # Check if the user already has a cart
        try:
            user_cart = Cart.objects.get(user=user)
            
            # Transfer items from session cart to user cart
            for session_item in session_cart.items.all():
                try:
                    # Check if the product already exists in the user's cart
                    user_item = CartItem.objects.get(cart=user_cart, product=session_item.product)
                    # If it exists, update the quantity
                    user_item.quantity += session_item.quantity
                    user_item.save()
                except CartItem.DoesNotExist:
                    # If it doesn't exist, create a new cart item in the user's cart
                    session_item.cart = user_cart
                    session_item.save()
            
            # Delete the session cart after transferring items
            session_cart.delete()
            
        except Cart.DoesNotExist:
            # If the user doesn't have a cart, simply assign the session cart to the user
            session_cart.user = user
            session_cart.save()
            
        # Clear the session ID
        del request.session['session_id']
        
    except Cart.DoesNotExist:
        # No session cart exists
        pass

# Product Line Views
def vitamin_c_line(request):
    """Vitamin C product line page"""
    products = Product.objects.filter(product_line='Vitamin C', is_available=True)
    categories = Category.objects.filter(parent=None)
    
    context = {
        'products': products,
        'categories': categories,
        'current_line': 'Vitamin C',
        'page_title': 'Vitamin C Products',
        'page_description': 'Explore our range of Vitamin C products for brightening, anti-aging, and antioxidant protection.',
        'line_benefits': [
            'Brightens skin and reduces hyperpigmentation',
            'Protects against environmental damage with antioxidants',
            'Boosts collagen production for firmer skin',
            'Reduces signs of aging and fine lines'
        ],
        'recommended_concerns': ['Brightening Skin', 'Aging Skin', 'Dehydrated Skin']
    }
    return render(request, 'store/product_line.html', context)

def retinol_line(request):
    """Retinol product line page"""
    products = Product.objects.filter(product_line='Retinol', is_available=True)
    categories = Category.objects.filter(parent=None)
    
    context = {
        'products': products,
        'categories': categories,
        'current_line': 'Retinol',
        'page_title': 'Retinol Products',
        'page_description': 'Discover our powerful Retinol products for anti-aging, skin renewal, and acne control.',
        'line_benefits': [
            'Reduces appearance of fine lines and wrinkles',
            'Accelerates cell turnover for smoother skin',
            'Helps clear and prevent acne breakouts',
            'Improves skin texture and tone'
        ],
        'recommended_concerns': ['Aging Skin', 'Acne Skin', 'Blackhead Removal']
    }
    return render(request, 'store/product_line.html', context)

def hyaluronic_acid_line(request):
    """Hyaluronic Acid product line page"""
    products = Product.objects.filter(product_line='Hyaluronic Acid', is_available=True)
    categories = Category.objects.filter(parent=None)
    
    context = {
        'products': products,
        'categories': categories,
        'current_line': 'Hyaluronic Acid',
        'page_title': 'Hyaluronic Acid Products',
        'page_description': 'Hydrate and plump your skin with our range of Hyaluronic Acid products for intense moisture.',
        'line_benefits': [
            'Provides deep hydration and moisture retention',
            'Plumps skin and reduces the appearance of fine lines',
            'Suitable for all skin types, even sensitive skin',
            'Helps repair skin barrier function'
        ],
        'recommended_concerns': ['Dehydrated Skin', 'Dry Skin', 'Aging Skin']
    }
    return render(request, 'store/product_line.html', context)

def skin_whitening_line(request):
    """Skin Whitening product line page"""
    products = Product.objects.filter(product_line='Skin Whitening', is_available=True)
    categories = Category.objects.filter(parent=None)
    
    context = {
        'products': products,
        'categories': categories,
        'current_line': 'Skin Whitening',
        'page_title': 'Skin Whitening Products',
        'page_description': 'Achieve a more even skin tone with our gentle skin whitening range for reducing dark spots and pigmentation.',
        'line_benefits': [
            'Reduces the appearance of dark spots and hyperpigmentation',
            'Evens out skin tone for a brighter complexion',
            'Contains gentle ingredients that work without harsh chemicals',
            'Helps prevent future pigmentation with antioxidant protection'
        ],
        'recommended_concerns': ['Brightening Skin', 'Aging Skin', 'Acne Skin']
    }
    return render(request, 'store/product_line.html', context)

def snail_line(request):
    """Snail product line page"""
    products = Product.objects.filter(product_line='Snail', is_available=True)
    categories = Category.objects.filter(parent=None)
    
    context = {
        'products': products,
        'categories': categories,
        'current_line': 'Snail',
        'page_title': 'Snail Mucin Products',
        'page_description': 'Experience the healing and regenerative properties of snail mucin for multiple skin concerns.',
        'line_benefits': [
            'Promotes skin healing and regeneration',
            'Provides intense hydration and moisture',
            'Reduces acne scarring and hyperpigmentation',
            'Improves skin elasticity and texture'
        ],
        'recommended_concerns': ['Acne Skin', 'Dehydrated Skin', 'Aging Skin', 'Soothing Skin']
    }
    return render(request, 'store/product_line.html', context)

def turmeric_line(request):
    """Turmeric product line page"""
    products = Product.objects.filter(product_line='Turmeric', is_available=True)
    categories = Category.objects.filter(parent=None)
    
    context = {
        'products': products,
        'categories': categories,
        'current_line': 'Turmeric',
        'page_title': 'Turmeric Products',
        'page_description': 'Harness the anti-inflammatory and brightening benefits of turmeric in our specialized skincare line.',
        'line_benefits': [
            'Reduces inflammation and soothes irritated skin',
            'Brightens skin tone and helps fade dark spots',
            'Contains antioxidants to fight free radical damage',
            'Helps control excess oil and prevent breakouts'
        ],
        'recommended_concerns': ['Acne Skin', 'Brightening Skin', 'Oily Skin', 'Soothing Skin']
    }
    return render(request, 'store/product_line.html', context)

# Product Type Category Views
def cleanser_category(request):
    """Cleanser category page"""
    try:
        category = Category.objects.get(name__icontains='cleanser')
        products = Product.objects.filter(
            Q(category=category) | 
            Q(category__parent=category) |
            Q(name__icontains='cleanser'),
            is_available=True
        ).distinct()
    except Category.DoesNotExist:
        # If no category exists, just show products with 'cleanser' in the name
        products = Product.objects.filter(
            Q(name__icontains='cleanser') | 
            Q(description__icontains='cleanser'),
            is_available=True
        ).distinct()
    
    categories = Category.objects.filter(parent=None)
    
    context = {
        'products': products,
        'categories': categories,
        'current_category': 'Cleanser',
        'page_title': 'Facial Cleansers',
        'page_description': 'Start your skincare routine right with our range of gentle yet effective facial cleansers.',
        'category_benefits': [
            'Removes dirt, oil, and makeup without stripping skin',
            'Cleanses pores to prevent breakouts',
            'Prepares skin for the rest of your skincare routine',
            'Available for all skin types and concerns'
        ]
    }
    return render(request, 'store/product_type.html', context)

def toner_category(request):
    """Toner category page"""
    try:
        category = Category.objects.get(name='Toners')
        products = Product.objects.filter(
            Q(category=category) | 
            Q(category__parent=category) |
            Q(name__icontains='toner'),
            is_available=True
        ).distinct()
    except Category.DoesNotExist:
        # If no category exists, just show products with 'toner' in the name
        products = Product.objects.filter(
            Q(name__icontains='toner') | 
            Q(description__icontains='toner'),
            is_available=True
        ).distinct()
    
    categories = Category.objects.filter(parent=None)
    
    context = {
        'products': products,
        'categories': categories,
        'current_category': 'Toner',
        'page_title': 'Facial Toners',
        'page_description': 'Balance, soothe and prep your skin with our range of facial toners for enhanced skincare absorption.',
        'category_benefits': [
            'Balances skin pH after cleansing',
            'Removes remaining impurities and tightens pores',
            'Hydrates and prepares skin for serums and moisturizers',
            'Soothes and refreshes the skin'
        ]
    }
    return render(request, 'store/product_type.html', context)

def serum_category(request):
    """Serum category page"""
    try:
        category = Category.objects.get(name__icontains='serum')
        products = Product.objects.filter(
            Q(category=category) | 
            Q(category__parent=category) |
            Q(name__icontains='serum'),
            is_available=True
        ).distinct()
    except Category.DoesNotExist:
        # If no category exists, just show products with 'serum' in the name
        products = Product.objects.filter(
            Q(name__icontains='serum') | 
            Q(description__icontains='serum'),
            is_available=True
        ).distinct()
    
    categories = Category.objects.filter(parent=None)
    
    context = {
        'products': products,
        'categories': categories,
        'current_category': 'Serum',
        'page_title': 'Facial Serums',
        'page_description': 'Target specific skin concerns with our concentrated facial serums for maximum effectiveness.',
        'category_benefits': [
            'Delivers concentrated active ingredients deep into skin',
            'Targets specific skin concerns with powerful formulations',
            'Lightweight texture absorbs quickly without residue',
            'Provides visible results with consistent use'
        ]
    }
    return render(request, 'store/product_type.html', context)

def face_cream_category(request):
    """Face Cream category page"""
    try:
        category = Category.objects.get(Q(name__icontains='face cream') | Q(name__icontains='facial cream'))
        products = Product.objects.filter(
            Q(category=category) | 
            Q(category__parent=category) |
            Q(name__icontains='face cream') |
            Q(name__icontains='facial cream'),
            is_available=True
        ).distinct()
    except Category.DoesNotExist:
        # If no category exists, just show products with 'face cream' in the name
        products = Product.objects.filter(
            Q(name__icontains='face cream') | 
            Q(name__icontains='facial cream') |
            Q(description__icontains='face cream'),
            is_available=True
        ).distinct()
    
    categories = Category.objects.filter(parent=None)
    
    context = {
        'products': products,
        'categories': categories,
        'current_category': 'Face Cream',
        'page_title': 'Face Creams & Moisturizers',
        'page_description': 'Lock in hydration and nourish your skin with our range of face creams for all skin types.',
        'category_benefits': [
            'Provides deep hydration and locks in moisture',
            'Strengthens skin barrier function',
            'Nourishes skin with essential vitamins and nutrients',
            'Prevents moisture loss and protects against environmental damage'
        ]
    }
    return render(request, 'store/product_type.html', context)

def facial_mask_category(request):
    """Facial Mask category page"""
    try:
        category = Category.objects.get(Q(name__icontains='mask') | Q(name__icontains='facial mask'))
        products = Product.objects.filter(
            Q(category=category) | 
            Q(category__parent=category) |
            Q(name__icontains='mask') |
            Q(name__icontains='facial mask'),
            is_available=True
        ).distinct()
    except Category.DoesNotExist:
        # If no category exists, just show products with 'mask' in the name
        products = Product.objects.filter(
            Q(name__icontains='mask') | 
            Q(name__icontains='facial mask') |
            Q(description__icontains='mask'),
            is_available=True
        ).distinct()
    
    categories = Category.objects.filter(parent=None)
    
    context = {
        'products': products,
        'categories': categories,
        'current_category': 'Facial Mask',
        'page_title': 'Facial Masks',
        'page_description': 'Give your skin an intensive treatment with our range of facial masks for various skin concerns.',
        'category_benefits': [
            'Provides intensive treatment for specific skin concerns',
            'Delivers high concentration of active ingredients',
            'Creates a relaxing self-care ritual',
            'Gives immediate visible results'
        ]
    }
    return render(request, 'store/product_type.html', context)

def soap_category(request):
    """Soap category page"""
    try:
        category = Category.objects.get(name__icontains='soap')
        products = Product.objects.filter(
            Q(category=category) | 
            Q(category__parent=category) |
            Q(name__icontains='soap'),
            is_available=True
        ).distinct()
    except Category.DoesNotExist:
        # If no category exists, just show products with 'soap' in the name
        products = Product.objects.filter(
            Q(name__icontains='soap') | 
            Q(description__icontains='soap'),
            is_available=True
        ).distinct()
    
    categories = Category.objects.filter(parent=None)
    
    context = {
        'products': products,
        'categories': categories,
        'current_category': 'Soap',
        'page_title': 'Natural Soaps',
        'page_description': 'Cleanse and nourish your skin with our range of natural handmade soaps.',
        'category_benefits': [
            'Made with natural ingredients with no harsh chemicals',
            'Cleanses without stripping skin\'s natural oils',
            'Packed with nourishing botanicals and essential oils',
            'Suitable for face and body'
        ]
    }
    return render(request, 'store/product_type.html', context)

def body_wash_category(request):
    """Body Wash category page"""
    try:
        category = Category.objects.get(name__icontains='body wash')
        products = Product.objects.filter(
            Q(category=category) | 
            Q(category__parent=category) |
            Q(name__icontains='body wash'),
            is_available=True
        ).distinct()
    except Category.DoesNotExist:
        # If no category exists, just show products with 'body wash' in the name
        products = Product.objects.filter(
            Q(name__icontains='body wash') | 
            Q(description__icontains='body wash'),
            is_available=True
        ).distinct()
    
    categories = Category.objects.filter(parent=None)
    
    context = {
        'products': products,
        'categories': categories,
        'current_category': 'Body Wash',
        'page_title': 'Body Washes',
        'page_description': 'Indulge in a luxurious bathing experience with our natural and nourishing body washes.',
        'category_benefits': [
            'Gently cleanses without drying the skin',
            'Contains moisturizing ingredients for soft skin',
            'Infused with aromatic natural scents for a spa-like experience',
            'Suitable for all skin types, including sensitive skin'
        ]
    }
    return render(request, 'store/product_type.html', context)

def body_lotion_category(request):
    """Body Lotion category page"""
    try:
        category = Category.objects.get(name__icontains='body lotion')
        products = Product.objects.filter(
            Q(category=category) | 
            Q(category__parent=category) |
            Q(name__icontains='body lotion'),
            is_available=True
        ).distinct()
    except Category.DoesNotExist:
        # If no category exists, just show products with 'body lotion' in the name
        products = Product.objects.filter(
            Q(name__icontains='body lotion') | 
            Q(description__icontains='body lotion'),
            is_available=True
        ).distinct()
    
    categories = Category.objects.filter(parent=None)
    
    context = {
        'products': products,
        'categories': categories,
        'current_category': 'Body Lotion',
        'page_title': 'Body Lotions',
        'page_description': 'Nourish and hydrate your skin with our range of moisturizing body lotions.',
        'category_benefits': [
            'Provides long-lasting hydration for dry skin',
            'Absorbs quickly without greasy residue',
            'Improves skin texture and elasticity',
            'Protects and repairs skin barrier'
        ]
    }
    return render(request, 'store/product_type.html', context)

# Skin Concern Views
def acne_skin_concern(request):
    """Acne Skin concern page"""
    products = Product.objects.filter(skin_concern='Acne Skin', is_available=True)
    categories = Category.objects.filter(parent=None)
    
    context = {
        'products': products,
        'categories': categories,
        'current_concern': 'Acne Skin',
        'page_title': 'Acne Skincare Solutions',
        'page_description': 'Combat acne and prevent breakouts with our specially formulated products for acne-prone skin.',
        'concern_description': 'Acne occurs when hair follicles become clogged with oil and dead skin cells. Our acne-fighting products help clear existing breakouts and prevent new ones from forming, while balancing oil production and reducing inflammation.',
        'recommended_products': ['Cleansers with Salicylic Acid', 'Oil-Free Moisturizers', 'Spot Treatments', 'Clay Masks']
    }
    return render(request, 'store/skin_concern.html', context)

def aging_skin_concern(request):
    """Aging Skin concern page"""
    products = Product.objects.filter(skin_concern='Aging Skin', is_available=True)
    categories = Category.objects.filter(parent=None)
    
    context = {
        'products': products,
        'categories': categories,
        'current_concern': 'Aging Skin',
        'page_title': 'Anti-Aging Skincare',
        'page_description': 'Target signs of aging with our effective anti-aging products for a more youthful complexion.',
        'concern_description': 'As we age, our skin produces less collagen and elastin, leading to wrinkles, fine lines, and loss of firmness. Our anti-aging products help boost collagen production, protect against environmental damage, and visibly reduce signs of aging.',
        'recommended_products': ['Retinol Serums', 'Peptide Creams', 'Vitamin C Products', 'Eye Creams']
    }
    return render(request, 'store/skin_concern.html', context)

def blackhead_removal_concern(request):
    """Blackhead Removal concern page"""
    products = Product.objects.filter(skin_concern='Blackhead Removal', is_available=True)
    categories = Category.objects.filter(parent=None)
    
    context = {
        'products': products,
        'categories': categories,
        'current_concern': 'Blackhead Removal',
        'page_title': 'Blackhead Removal Solutions',
        'page_description': 'Clear clogged pores and eliminate blackheads with our targeted skincare products.',
        'concern_description': 'Blackheads are a mild form of acne that appear as small, dark lesions on the skin, typically on the face and nose. They occur when hair follicles become clogged with oil and dead skin cells. Our products help unclog pores, dissolve excess sebum, and prevent new blackheads from forming.',
        'recommended_products': ['Pore Strips', 'BHA Exfoliants', 'Clay Masks', 'Oil-Control Cleansers']
    }
    return render(request, 'store/skin_concern.html', context)

def brightening_skin_concern(request):
    """Brightening Skin concern page"""
    products = Product.objects.filter(skin_concern='Brightening Skin', is_available=True)
    categories = Category.objects.filter(parent=None)
    
    context = {
        'products': products,
        'categories': categories,
        'current_concern': 'Brightening Skin',
        'page_title': 'Skin Brightening Solutions',
        'page_description': 'Achieve a radiant, even skin tone with our brightening products for a luminous complexion.',
        'concern_description': 'Dull skin and uneven skin tone can be caused by factors such as sun damage, pollution, and aging. Our brightening products help fade dark spots, even out skin tone, and restore natural radiance for a more luminous complexion.',
        'recommended_products': ['Vitamin C Serums', 'Alpha Arbutin Products', 'Exfoliating Treatments', 'Brightening Masks']
    }
    return render(request, 'store/skin_concern.html', context)

def dehydrated_skin_concern(request):
    """Dehydrated Skin concern page"""
    products = Product.objects.filter(skin_concern='Dehydrated Skin', is_available=True)
    categories = Category.objects.filter(parent=None)
    
    context = {
        'products': products,
        'categories': categories,
        'current_concern': 'Dehydrated Skin',
        'page_title': 'Solutions for Dehydrated Skin',
        'page_description': 'Restore moisture and plumpness to dehydrated skin with our hydrating skincare solutions.',
        'concern_description': 'Dehydrated skin lacks water and can affect any skin type - even oily skin. Signs include dullness, itchiness, and fine lines. Our products help replenish lost moisture, strengthen the skin barrier, and prevent water loss for plump, healthy skin.',
        'recommended_products': ['Hyaluronic Acid Serums', 'Hydrating Toners', 'Moisturizing Masks', 'Ceramide Creams']
    }
    return render(request, 'store/skin_concern.html', context)

def dry_skin_concern(request):
    """Dry Skin concern page"""
    products = Product.objects.filter(skin_concern='Dry Skin', is_available=True)
    categories = Category.objects.filter(parent=None)
    
    context = {
        'products': products,
        'categories': categories,
        'current_concern': 'Dry Skin',
        'page_title': 'Dry Skin Relief',
        'page_description': 'Nourish and replenish dry skin with our deeply moisturizing products for lasting comfort.',
        'concern_description': 'Dry skin lacks oil and can feel tight, rough, and flaky. It may be caused by genetics, harsh weather, hot showers, or aging. Our products help replenish oils, provide deep hydration, and strengthen the skin barrier to prevent moisture loss.',
        'recommended_products': ['Rich Creams', 'Cleansing Oils', 'Hydrating Serums', 'Nourishing Masks']
    }
    return render(request, 'store/skin_concern.html', context)

def oily_skin_concern(request):
    """Oily Skin concern page"""
    products = Product.objects.filter(skin_concern='Oily Skin', is_available=True)
    categories = Category.objects.filter(parent=None)
    
    context = {
        'products': products,
        'categories': categories,
        'current_concern': 'Oily Skin',
        'page_title': 'Oily Skin Solutions',
        'page_description': 'Control shine and balance oil production with our specialized products for oily skin.',
        'concern_description': 'Oily skin occurs when sebaceous glands produce excess sebum, leading to a shiny appearance and potential breakouts. Our products help regulate oil production, minimize the appearance of pores, and provide oil-free hydration for balanced skin.',
        'recommended_products': ['Oil-Control Cleansers', 'Mattifying Toners', 'Lightweight Gel Moisturizers', 'Clay Masks']
    }
    return render(request, 'store/skin_concern.html', context)

def soothing_skin_concern(request):
    """Soothing Skin concern page"""
    products = Product.objects.filter(skin_concern='Soothing Skin', is_available=True)
    categories = Category.objects.filter(parent=None)
    
    context = {
        'products': products,
        'categories': categories,
        'current_concern': 'Soothing Skin',
        'page_title': 'Soothing Solutions for Sensitive Skin',
        'page_description': 'Calm irritation and reduce redness with our gentle, soothing products for sensitive skin.',
        'concern_description': 'Sensitive skin can be easily irritated, leading to redness, itching, and discomfort. Our gentle, soothing products help calm inflammation, strengthen the skin barrier, and provide relief from irritation without harsh ingredients.',
        'recommended_products': ['Centella Asiatica Products', 'Fragrance-Free Cleansers', 'Calming Serums', 'Barrier Repair Creams']
    }
    return render(request, 'store/skin_concern.html', context)

def collagen_line(request):
    """Collagen product line page"""
    products = Product.objects.filter(product_line='Collagen', is_available=True)
    categories = Category.objects.filter(parent=None)
    
    context = {
        'products': products,
        'categories': categories,
        'current_line': 'Collagen',
        'page_title': 'Collagen Products',
        'page_description': 'Boost skin elasticity and firmness with our collagen-enriched skincare products.',
        'line_benefits': [
            'Improves skin elasticity and firmness',
            'Reduces appearance of fine lines and wrinkles',
            'Promotes skin repair and regeneration',
            'Enhances skin hydration and plumpness'
        ],
        'recommended_concerns': ['Aging Skin', 'Dehydrated Skin', 'Dry Skin']
    }
    return render(request, 'store/product_line.html', context)

def deeply_cleansing_line(request):
    """Deeply Cleansing product line page"""
    products = Product.objects.filter(product_line='Deeply Cleansing', is_available=True)
    categories = Category.objects.filter(parent=None)
    
    context = {
        'products': products,
        'categories': categories,
        'current_line': 'Deeply Cleansing',
        'page_title': 'Deeply Cleansing Products',
        'page_description': 'Achieve a deep clean with our powerful yet gentle cleansing products.',
        'line_benefits': [
            'Removes deep-seated impurities and excess oil',
            'Unclogs pores and prevents breakouts',
            'Maintains skin\'s natural moisture balance',
            'Leaves skin fresh and thoroughly cleansed'
        ],
        'recommended_concerns': ['Oily Skin', 'Acne Skin', 'Blackhead Removal']
    }
    return render(request, 'store/product_line.html', context)

def beauty_tools_line(request):
    """Beauty Tools product line page"""
    products = Product.objects.filter(product_line='Beauty Tool', is_available=True)
    categories = Category.objects.filter(parent=None)
    
    context = {
        'products': products,
        'categories': categories,
        'current_line': 'Beauty Tool',
        'page_title': 'Beauty Tools',
        'page_description': 'Enhance your skincare routine with our professional beauty tools.',
        'line_benefits': [
            'Improves product absorption and effectiveness',
            'Promotes blood circulation for healthier skin',
            'Helps reduce puffiness and tone facial muscles',
            'Professional-grade tools for at-home use'
        ],
        'recommended_concerns': ['All Skin Types']
    }
    return render(request, 'store/product_line.html', context)

def luxury_gold_line(request):
    """24K Luxury Gold product line page"""
    products = Product.objects.filter(product_line='24K Luxury Gold', is_available=True)
    categories = Category.objects.filter(parent=None)
    
    context = {
        'products': products,
        'categories': categories,
        'current_line': '24K Luxury Gold',
        'page_title': '24K Luxury Gold Products',
        'page_description': 'Experience luxury skincare with our 24K gold-infused products.',
        'line_benefits': [
            'Promotes collagen production and skin renewal',
            'Provides antioxidant protection',
            'Reduces signs of aging and improves skin texture',
            'Adds a luxurious glow to your skincare routine'
        ],
        'recommended_concerns': ['Aging Skin', 'Brightening Skin', 'Dehydrated Skin']
    }
    return render(request, 'store/product_line.html', context)

def feminine_care_line(request):
    """Feminine Care product line page"""
    products = Product.objects.filter(product_line='Feminine Care', is_available=True)
    categories = Category.objects.filter(parent=None)
    
    context = {
        'products': products,
        'categories': categories,
        'current_line': 'Feminine Care',
        'page_title': 'Feminine Care Products',
        'page_description': 'Gentle and effective feminine care products for your intimate wellness.',
        'line_benefits': [
            'pH-balanced formulations for intimate areas',
            'Gentle cleansing and moisturizing',
            'Promotes feminine hygiene and comfort',
            'Made with natural, soothing ingredients'
        ],
        'recommended_concerns': ['Sensitive Skin', 'Personal Care']
    }
    return render(request, 'store/product_line.html', context)

def salicylic_acid_line(request):
    """Salicylic Acid product line page"""
    products = Product.objects.filter(product_line='Salicylic Acid', is_available=True)
    categories = Category.objects.filter(parent=None)
    
    context = {
        'products': products,
        'categories': categories,
        'current_line': 'Salicylic Acid',
        'page_title': 'Salicylic Acid Products',
        'page_description': 'Combat acne and unclog pores with our salicylic acid treatments.',
        'line_benefits': [
            'Unclogs pores and prevents breakouts',
            'Exfoliates dead skin cells',
            'Reduces excess oil production',
            'Improves skin texture and clarity'
        ],
        'recommended_concerns': ['Acne Skin', 'Oily Skin', 'Blackhead Removal']
    }
    return render(request, 'store/product_line.html', context)

def sun_care_line(request):
    """Sun Care product line page"""
    products = Product.objects.filter(product_line='Sun Care', is_available=True)
    categories = Category.objects.filter(parent=None)
    
    context = {
        'products': products,
        'categories': categories,
        'current_line': 'Sun Care',
        'page_title': 'Sun Care Products',
        'page_description': 'Protect your skin from harmful UV rays with our advanced sun care products.',
        'line_benefits': [
            'Broad-spectrum UV protection',
            'Lightweight, non-greasy formulas',
            'Prevents premature aging and dark spots',
            'Suitable for daily use'
        ],
        'recommended_concerns': ['Sun Protection', 'Aging Skin', 'Brightening Skin']
    }
    return render(request, 'store/product_line.html', context)

def vitamin_e_line(request):
    """Vitamin E product line page"""
    products = Product.objects.filter(product_line='Vitamin E', is_available=True)
    categories = Category.objects.filter(parent=None)
    
    context = {
        'products': products,
        'categories': categories,
        'current_line': 'Vitamin E',
        'page_title': 'Vitamin E Products',
        'page_description': 'Nourish and protect your skin with our vitamin E-enriched products.',
        'line_benefits': [
            'Provides powerful antioxidant protection',
            'Moisturizes and nourishes skin',
            'Helps heal and repair skin damage',
            'Supports skin barrier function'
        ],
        'recommended_concerns': ['Dry Skin', 'Aging Skin', 'Dehydrated Skin']
    }
    return render(request, 'store/product_line.html', context)

def weight_loss_line(request):
    """Weight Loss product line page"""
    products = Product.objects.filter(product_line='Weight Loss', is_available=True)
    categories = Category.objects.filter(parent=None)
    
    context = {
        'products': products,
        'categories': categories,
        'current_line': 'Weight Loss',
        'page_title': 'Weight Loss Products',
        'page_description': 'Support your weight management goals with our specialized products.',
        'line_benefits': [
            'Supports healthy weight management',
            'Promotes fat reduction',
            'Enhances body contouring',
            'Natural and safe formulations'
        ],
        'recommended_concerns': ['Body Care', 'Weight Management']
    }
    return render(request, 'store/product_line.html', context)

def beauty_tools(request):
    """Beauty Tools page using the custom beauty tools template"""
    products = Product.objects.filter(product_line='Beauty Tool', is_available=True)
    
    # Sort options
    sort = request.GET.get('sort', 'default')
    if sort == 'price_low':
        products = products.order_by('price')
    elif sort == 'price_high':
        products = products.order_by('-price')
    elif sort == 'newest':
        products = products.order_by('-created_at')
    elif sort == 'name_asc':
        products = products.order_by('name')
    elif sort == 'name_desc':
        products = products.order_by('-name')
    else:  # Default sorting - featured first
        products = products.order_by('-featured', 'name')
    
    # Calculate discount percentages for display
    for product in products:
        if product.original_price and product.original_price > product.price:
            discount = product.original_price - product.price
            product.discount_percentage = int((discount / product.original_price) * 100)
    
    context = {
        'products': products,
        'page_title': 'Facial Beauty Tool',
    }
    
    return render(request, 'store/beauty_tools.html', context)
