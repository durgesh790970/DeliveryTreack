from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.contrib.auth import login, authenticate, logout

from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from .models import UserProfile, Order, OrderItem, SavedItem, CartItem

import json
import logging
import time
def add_address_view(request):
    return render(request, 'add_address.html')

logger = logging.getLogger(__name__)

def home_view(request):
    # Home page with featured content
    featured_restaurants = [
        {
            'id': 1,
            'name': "Domino's Pizza",
            'cuisine': 'Italian, Pizza, Fast Food',
            'rating': 4.3,
            'reviews': '2.5k+',
            'delivery_time': '25-30 min',
            'offer': 'Free delivery above ₹299',
            'discount': '30% OFF',
            'image': '🍕'
        },
        {
            'id': 2,
            'name': 'Biryani Express',
            'cuisine': 'North Indian, Biryani, Mughlai',
            'rating': 4.5,
            'reviews': '3.2k+',
            'delivery_time': '35-40 min',
            'offer': '₹100 OFF above ₹399',
            'discount': '40% OFF',
            'image': '🍛'
        },
        {
            'id': 3,
            'name': 'Burger King',
            'cuisine': 'American, Burgers, Fast Food',
            'rating': 4.2,
            'reviews': '4.1k+',
            'delivery_time': '20-25 min',
            'offer': 'Free delivery + 50% OFF',
            'discount': 'Buy 1 Get 1',
            'image': '🍔'
        },
        {
            'id': 4,
            'name': 'Wow! China',
            'cuisine': 'Chinese, Thai, Pan-Asian',
            'rating': 4.1,
            'reviews': '1.8k+',
            'delivery_time': '30-35 min',
            'offer': 'Buy 1 Get 1 on selected items',
            'discount': '25% OFF',
            'image': '🥡'
        }
    ]
    
    top_offers = [
        {
            'title': 'Flat ₹50 OFF',
            'subtitle': 'On orders above ₹299',
            'code': 'SAVE50'
        },
        {
            'title': '₹100 OFF',
            'subtitle': 'First order special',
            'code': 'FIRST100'
        },
        {
            'title': 'Free Delivery',
            'subtitle': 'On all orders today',
            'code': 'No Code Needed'
        },
        {
            'title': '40% OFF',
            'subtitle': 'Party orders above ₹999',
            'code': 'PARTY40'
        }
    ]
    
    food_categories = [
        {'name': 'Pizza', 'icon': '🍕', 'slug': 'pizza'},
        {'name': 'Biryani', 'icon': '🍛', 'slug': 'biryani'},
        {'name': 'Chinese', 'icon': '🥡', 'slug': 'chinese'},
        {'name': 'Burger', 'icon': '🍔', 'slug': 'burger'},
        {'name': 'Dessert', 'icon': '🍰', 'slug': 'dessert'},
        {'name': 'Drinks', 'icon': '🥤', 'slug': 'drinks'},
        {'name': 'Indian', 'icon': '🍜', 'slug': 'indian'},
        {'name': 'Healthy', 'icon': '🥗', 'slug': 'healthy'}
    ]
    
    context = {
        'featured_restaurants': featured_restaurants,
        'top_offers': top_offers,
        'food_categories': food_categories,
        'user_name': 'Food Lover'  # In real app, get from user session
    }
    
    return render(request, "home.html", context)

def index(request):
    restaurants = [
        {"name": "Spicy Indian Palace", "category": "Indian", "rating": "4.2", "delivery_time": "25-30", "offer": "30% OFF"},
        {"name": "Dragon Wok Express", "category": "Chinese", "rating": "4.5", "delivery_time": "20-25", "offer": "40% OFF"},
        {"name": "Sweet Treats Cafe", "category": "Desserts", "rating": "4.3", "delivery_time": "15-20", "offer": "25% OFF"},
        {"name": "Pizza Corner", "category": "Italian", "rating": "4.1", "delivery_time": "30-35", "offer": "50% OFF"},
        {"name": "Burger Junction", "category": "Fast Food", "rating": "4.4", "delivery_time": "20-25", "offer": "Buy 1 Get 1"},
        {"name": "Healthy Bites", "category": "Healthy", "rating": "4.0", "delivery_time": "25-30", "offer": "20% OFF"},
    ]
    return render(request, "index.html", {"restaurants": restaurants})

def index_page(request):
    return render(request, "index.html")

def login_view(request):
    return render(request, "login.html")

def restaurants_view(request):
    return render(request, "restaurants.html")

def cart_view(request):
    return render(request, "cart_enhanced.html")

def checkout_view(request):
    return render(request, "checkout.html")

def singup_view(request):
    return render(request, "singup.html")

def track_view(request):
    return render(request, "track.html")

def order_view(request):
    return render(request, "order_status.html")

@ensure_csrf_cookie
def menu_view(request):
    menu_items = get_menu_items()
    return render(request, "menu.html", {"menu_items": menu_items})


def get_menu_items():
    """Return a full list of menu items used across multiple views."""
    return [
        {"id": 1, "name": "Margherita Pizza", "category": "pizza", "price": 299, "image": "🍕", "image_url": "/static/images/pizza.jpg", "description": "Fresh tomatoes, mozzarella, basil"},
        {"id": 2, "name": "Pepperoni Pizza", "category": "pizza", "price": 399, "image": "🍕", "image_url": "/static/images/pizza.jpg", "description": "Pepperoni, cheese, tomato sauce"},
        {"id": 3, "name": "Veggie Supreme", "category": "pizza", "price": 349, "image": "🍕", "image_url": "/static/images/pizza.jpg", "description": "Bell peppers, onions, mushrooms, olives"},
        {"id": 4, "name": "Chicken BBQ Pizza", "category": "pizza", "price": 449, "image": "🍕", "image_url": "/static/images/pizza.jpg", "description": "BBQ chicken, red onions, cilantro"},
        {"id": 5, "name": "Hawaiian Pizza", "category": "pizza", "price": 379, "image": "🍕", "image_url": "/static/images/pizza.jpg", "description": "Ham, pineapple, cheese"},
        {"id": 6, "name": "Four Cheese Pizza", "category": "pizza", "price": 429, "image": "🍕", "image_url": "/static/images/pizza.jpg", "description": "Mozzarella, cheddar, parmesan, gouda"},
        {"id": 7, "name": "Meat Lovers Pizza", "category": "pizza", "price": 499, "image": "🍕", "image_url": "/static/images/pizza.jpg", "description": "Pepperoni, sausage, ham, bacon"},
        {"id": 8, "name": "Mushroom Delight", "category": "pizza", "price": 329, "image": "🍕", "image_url": "/static/images/pizza.jpg", "description": "Mixed mushrooms, garlic, herbs"},
        {"id": 9, "name": "Spicy Jalapeño", "category": "pizza", "price": 359, "image": "🍕", "image_url": "/static/images/pizza.jpg", "description": "Jalapeños, pepperoni, spicy sauce"},
        {"id": 10, "name": "Classic Italian", "category": "pizza", "price": 389, "image": "🍕", "image_url": "/static/images/pizza.jpg", "description": "Italian sausage, peppers, onions"},
        {"id": 11, "name": "Classic Burger", "category": "burger", "price": 199, "image": "🍔", "description": "Beef patty, lettuce, tomato, onion"},
        {"id": 12, "name": "Cheese Burger", "category": "burger", "price": 229, "image": "🍔", "description": "Beef patty, cheese, lettuce, tomato"},
        {"id": 13, "name": "Chicken Burger", "category": "burger", "price": 249, "image": "🍔", "description": "Grilled chicken, mayo, lettuce"},
        {"id": 14, "name": "Fish Burger", "category": "burger", "price": 269, "image": "🍔", "description": "Fish fillet, tartar sauce, lettuce"},
        {"id": 15, "name": "Veggie Burger", "category": "burger", "price": 179, "image": "🍔", "description": "Veggie patty, avocado, sprouts"},
        {"id": 16, "name": "BBQ Bacon Burger", "category": "burger", "price": 299, "image": "🍔", "description": "Beef patty, bacon, BBQ sauce"},
        {"id": 17, "name": "Mushroom Swiss", "category": "burger", "price": 279, "image": "🍔", "description": "Beef patty, mushrooms, swiss cheese"},
        {"id": 18, "name": "Spicy Chicken", "category": "burger", "price": 259, "image": "🍔", "description": "Spicy chicken, jalapeños, pepper jack"},
        {"id": 19, "name": "Double Cheese", "category": "burger", "price": 319, "image": "🍔", "description": "Two patties, double cheese"},
        {"id": 20, "name": "Turkey Burger", "category": "burger", "price": 239, "image": "🍔", "description": "Turkey patty, cranberry sauce"},
        {"id": 21, "name": "Black Bean Burger", "category": "burger", "price": 189, "image": "🍔", "description": "Black bean patty, salsa, avocado"},
        {"id": 22, "name": "Lamb Burger", "category": "burger", "price": 349, "image": "🍔", "description": "Lamb patty, mint sauce, feta"},
        {"id": 23, "name": "Breakfast Burger", "category": "burger", "price": 289, "image": "🍔", "description": "Beef patty, egg, bacon, cheese"},
        {"id": 24, "name": "Hawaiian Burger", "category": "burger", "price": 259, "image": "🍔", "description": "Chicken, pineapple, teriyaki"},
        {"id": 25, "name": "Buffalo Chicken", "category": "burger", "price": 269, "image": "🍔", "description": "Buffalo chicken, blue cheese, celery"},
        {"id": 26, "name": "Butter Chicken", "category": "indian", "price": 329, "image": "🍛", "description": "Creamy tomato curry with chicken"},
        {"id": 27, "name": "Chicken Biryani", "category": "indian", "price": 299, "image": "🍛", "description": "Fragrant rice with spiced chicken"},
        {"id": 28, "name": "Palak Paneer", "category": "indian", "price": 249, "image": "🍛", "description": "Spinach curry with cottage cheese"},
        {"id": 29, "name": "Dal Makhani", "category": "indian", "price": 199, "image": "🍛", "description": "Creamy black lentil curry"},
        {"id": 30, "name": "Tandoori Chicken", "category": "indian", "price": 349, "image": "🍛", "description": "Clay oven roasted chicken"},
        {"id": 31, "name": "Naan Bread", "category": "indian", "price": 49, "image": "🍛", "description": "Fresh baked Indian bread"},
        {"id": 32, "name": "Chicken Tikka", "category": "indian", "price": 279, "image": "🍛", "description": "Grilled marinated chicken pieces"},
        {"id": 33, "name": "Mutton Curry", "category": "indian", "price": 399, "image": "🍛", "description": "Spicy goat meat curry"},
        {"id": 34, "name": "Vegetable Biryani", "category": "indian", "price": 249, "image": "🍛", "description": "Aromatic rice with mixed vegetables"},
        {"id": 35, "name": "Chole Bhature", "category": "indian", "price": 189, "image": "🍛", "description": "Chickpea curry with fried bread"},
        {"id": 36, "name": "Fish Curry", "category": "indian", "price": 319, "image": "🍛", "description": "Coconut based fish curry"},
        {"id": 37, "name": "Paneer Makhani", "category": "indian", "price": 269, "image": "🍛", "description": "Cottage cheese in tomato gravy"},
        {"id": 38, "name": "Rajma Rice", "category": "indian", "price": 179, "image": "🍛", "description": "Kidney beans curry with rice"},
        {"id": 39, "name": "Samosa", "category": "indian", "price": 29, "image": "🍛", "description": "Crispy pastry with spiced filling"},
        {"id": 40, "name": "Masala Dosa", "category": "indian", "price": 149, "image": "🍛", "description": "Crispy crepe with potato filling"},
        {"id": 41, "name": "Aloo Gobi", "category": "indian", "price": 199, "image": "🍛", "description": "Potato and cauliflower curry"},
        {"id": 42, "name": "Chicken Korma", "category": "indian", "price": 309, "image": "🍛", "description": "Mild creamy chicken curry"},
        {"id": 43, "name": "Pav Bhaji", "category": "indian", "price": 139, "image": "🍛", "description": "Spiced vegetable mash with bread"},
        {"id": 44, "name": "Lamb Vindaloo", "category": "indian", "price": 379, "image": "🍛", "description": "Spicy Goan lamb curry"},
        {"id": 45, "name": "Idli Sambar", "category": "indian", "price": 99, "image": "🍛", "description": "Steamed rice cakes with lentil soup"},
        {"id": 46, "name": "Chicken Fried Rice", "category": "chinese", "price": 199, "image": "🥡", "description": "Wok-fried rice with chicken"},
        {"id": 47, "name": "Sweet & Sour Pork", "category": "chinese", "price": 249, "image": "🥡", "description": "Pork in tangy sweet sauce"},
        {"id": 48, "name": "Kung Pao Chicken", "category": "chinese", "price": 229, "image": "🥡", "description": "Spicy chicken with peanuts"},
        {"id": 49, "name": "Beef Black Bean", "category": "chinese", "price": 269, "image": "🥡", "description": "Beef stir-fry in black bean sauce"},
        {"id": 50, "name": "Vegetable Spring Rolls", "category": "chinese", "price": 149, "image": "🥡", "description": "Crispy rolls with fresh vegetables"},
        {"id": 51, "name": "Chow Mein", "category": "chinese", "price": 179, "image": "🥡", "description": "Stir-fried noodles with vegetables"},
        {"id": 52, "name": "General Tso's Chicken", "category": "chinese", "price": 259, "image": "🥡", "description": "Crispy chicken in sweet sauce"},
        {"id": 53, "name": "Mapo Tofu", "category": "chinese", "price": 189, "image": "🥡", "description": "Silky tofu in spicy sauce"},
        {"id": 54, "name": "Peking Duck", "category": "chinese", "price": 399, "image": "🥡", "description": "Roasted duck with pancakes"},
        {"id": 55, "name": "Hot Pot", "category": "chinese", "price": 449, "image": "🥡", "description": "Spicy broth with mixed ingredients"},
        {"id": 56, "name": "Dim Sum Platter", "category": "chinese", "price": 299, "image": "🥡", "description": "Assorted steamed dumplings"},
        {"id": 57, "name": "Orange Chicken", "category": "chinese", "price": 239, "image": "🥡", "description": "Battered chicken in orange glaze"},
        {"id": 58, "name": "Wonton Soup", "category": "chinese", "price": 169, "image": "🥡", "description": "Pork dumplings in clear broth"},
        {"id": 59, "name": "Cashew Chicken", "category": "chinese", "price": 249, "image": "🥡", "description": "Chicken stir-fry with cashews"},
        {"id": 60, "name": "Salt & Pepper Prawns", "category": "chinese", "price": 319, "image": "🥡", "description": "Crispy prawns with spices"},
        {"id": 61, "name": "Chocolate Cake", "category": "dessert", "price": 149, "image": "🍰", "description": "Rich chocolate layer cake"},
        {"id": 62, "name": "Cheesecake", "category": "dessert", "price": 179, "image": "🍰", "description": "Creamy New York style cheesecake"},
        {"id": 63, "name": "Tiramisu", "category": "dessert", "price": 199, "image": "🍰", "description": "Italian coffee-flavored dessert"},
        {"id": 64, "name": "Ice Cream Sundae", "category": "dessert", "price": 129, "image": "🍰", "description": "Vanilla ice cream with toppings"},
        {"id": 65, "name": "Apple Pie", "category": "dessert", "price": 159, "image": "🍰", "description": "Classic American apple pie"},
        {"id": 66, "name": "Brownie", "category": "dessert", "price": 99, "image": "🍰", "description": "Fudgy chocolate brownie"},
        {"id": 67, "name": "Crème Brûlée", "category": "dessert", "price": 189, "image": "🍰", "description": "Vanilla custard with caramelized sugar"},
        {"id": 68, "name": "Panna Cotta", "category": "dessert", "price": 169, "image": "🍰", "description": "Italian cream dessert"},
        {"id": 69, "name": "Fruit Tart", "category": "dessert", "price": 139, "image": "🍰", "description": "Pastry shell with fresh fruits"},
        {"id": 70, "name": "Chocolate Mousse", "category": "dessert", "price": 149, "image": "🍰", "description": "Light and airy chocolate dessert"},
        {"id": 71, "name": "Carrot Cake", "category": "dessert", "price": 159, "image": "🍰", "description": "Spiced cake with cream cheese frosting"},
        {"id": 72, "name": "Lemon Meringue Pie", "category": "dessert", "price": 169, "image": "🍰", "description": "Tangy lemon filling with meringue"},
        {"id": 73, "name": "Red Velvet Cake", "category": "dessert", "price": 179, "image": "🍰", "description": "Velvety red cake with cream cheese"},
        {"id": 74, "name": "Banana Split", "category": "dessert", "price": 199, "image": "🍰", "description": "Banana with ice cream and toppings"},
        {"id": 75, "name": "Chocolate Soufflé", "category": "dessert", "price": 229, "image": "🍰", "description": "Warm chocolate soufflé"},
        {"id": 76, "name": "Strawberry Shortcake", "category": "dessert", "price": 149, "image": "🍰", "description": "Sponge cake with strawberries"},
        {"id": 77, "name": "Gelato", "category": "dessert", "price": 119, "image": "🍰", "description": "Italian style ice cream"},
        {"id": 78, "name": "Macarons", "category": "dessert", "price": 89, "image": "🍰", "description": "French almond cookies"},
        {"id": 79, "name": "Peach Cobbler", "category": "dessert", "price": 139, "image": "🍰", "description": "Warm peach dessert with crust"},
        {"id": 80, "name": "Chocolate Tart", "category": "dessert", "price": 159, "image": "🍰", "description": "Rich chocolate tart"},
        {"id": 81, "name": "Fresh Orange Juice", "category": "drinks", "price": 79, "image": "🥤", "description": "Freshly squeezed orange juice"},
        {"id": 82, "name": "Mango Smoothie", "category": "drinks", "price": 99, "image": "🥤", "description": "Creamy mango smoothie"},
        {"id": 83, "name": "Iced Coffee", "category": "drinks", "price": 89, "image": "🥤", "description": "Cold brew coffee with ice"},
        {"id": 84, "name": "Green Tea", "category": "drinks", "price": 59, "image": "🥤", "description": "Antioxidant rich green tea"},
        {"id": 85, "name": "Chocolate Milkshake", "category": "drinks", "price": 119, "image": "🥤", "description": "Rich chocolate milkshake"},
        {"id": 86, "name": "Lemonade", "category": "drinks", "price": 69, "image": "🥤", "description": "Fresh lemon drink"},
        {"id": 87, "name": "Cappuccino", "category": "drinks", "price": 109, "image": "🥤", "description": "Espresso with steamed milk foam"},
        {"id": 88, "name": "Fruit Punch", "category": "drinks", "price": 79, "image": "🥤", "description": "Mixed fruit refreshing drink"},
        {"id": 89, "name": "Matcha Latte", "category": "drinks", "price": 129, "image": "🥤", "description": "Green tea powder with milk"},
        {"id": 90, "name": "Virgin Mojito", "category": "drinks", "price": 99, "image": "🥤", "description": "Mint and lime refresher"},
        {"id": 91, "name": "Berry Smoothie", "category": "drinks", "price": 109, "image": "🥤", "description": "Mixed berries smoothie"},
        {"id": 92, "name": "Hot Chocolate", "category": "drinks", "price": 89, "image": "🥤", "description": "Warm chocolate drink"},
        {"id": 93, "name": "Iced Tea", "category": "drinks", "price": 69, "image": "🥤", "description": "Refreshing iced tea"},
        {"id": 94, "name": "Coconut Water", "category": "drinks", "price": 59, "image": "🥤", "description": "Natural coconut water"},
        {"id": 95, "name": "Protein Shake", "category": "drinks", "price": 149, "image": "🥤", "description": "Healthy protein smoothie"},
        {"id": 96, "name": "Espresso", "category": "drinks", "price": 79, "image": "🥤", "description": "Strong Italian coffee"},
        {"id": 97, "name": "Strawberry Juice", "category": "drinks", "price": 89, "image": "🥤", "description": "Fresh strawberry juice"},
        {"id": 98, "name": "Energy Drink", "category": "drinks", "price": 99, "image": "🥤", "description": "Caffeine energy booster"},
        {"id": 99, "name": "Watermelon Juice", "category": "drinks", "price": 79, "image": "🥤", "description": "Refreshing watermelon juice"},
        {"id": 100, "name": "Masala Chai", "category": "drinks", "price": 49, "image": "🥤", "description": "Spiced Indian tea"},
    ]


def manu_view(request):
    menu_items = get_menu_items()
    return render(request, 'manu.html', {'menu_items': menu_items})

def restaurants_view(request):
    # You can pass real restaurant data here if needed
    return render(request, "restaurants.html")

def food_detail_view(request):
    # You can pass specific food item data here if needed
    food_item = {
        'name': 'Margherita Pizza',
        'category': 'Italian • Pizza • Vegetarian',
        'price': 299,
        'original_price': 399,
        'discount': 25,
        'rating': 4.5,
        'reviews_count': 1247,
        'description': 'A classic Italian pizza topped with fresh mozzarella cheese, ripe tomatoes, and aromatic basil leaves. Made with hand-tossed dough and baked to perfection in our wood-fired oven.',
        'image': 'pizza.jpg',
        'is_veg': True,
        'is_bestseller': True,
        'spice_level': 'Mild',
        'sizes': [
            {'name': 'Small', 'price': 199},
            {'name': 'Medium', 'price': 299},
            {'name': 'Large', 'price': 399}
        ],
        'addons': [
            {'name': 'Extra Cheese', 'description': 'Double the cheese for extra richness', 'price': 50},
            {'name': 'Mushrooms', 'description': 'Fresh button mushrooms', 'price': 30},
            {'name': 'Black Olives', 'description': 'Premium black olives', 'price': 25},
            {'name': 'Bell Peppers', 'description': 'Colorful bell peppers', 'price': 20}
        ],
        'nutrition': {
            'calories': 420,
            'protein': '18g',
            'carbs': '45g',
            'fat': '15g',
            'fiber': '2.5g',
            'sodium': '890mg'
        }
    }
    return render(request, "food_detail.html", {'food_item': food_item})

def logo_showcase_view(request):
    # Logo showcase page
    return render(request, "logo_showcase.html")

def voice_assistant_view(request):
    # Voice assistant page
    return render(request, "voice_assistant.html")

@csrf_exempt
@require_http_methods(["POST"])
def social_login_view(request):
    """
    Handle social authentication (Google, Facebook, etc.)
    """
    try:
        data = json.loads(request.body)
        provider = data.get('provider')
        user_data = data.get('user_data')
        
        if not provider or not user_data:
            return JsonResponse({
                'success': False,
                'message': 'Invalid request data'
            }, status=400)
        
        if provider == 'google':
            return handle_google_login(request, user_data)
        elif provider == 'facebook':
            return handle_facebook_login(request, user_data)
        else:
            return JsonResponse({
                'success': False,
                'message': 'Unsupported authentication provider'
            }, status=400)
            
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        logger.error(f"Social login error: {str(e)}")
        return JsonResponse({
            'success': False,
            'message': 'Authentication failed'
        }, status=500)

def handle_google_login(request, user_data):
    """
    Handle Google OAuth login
    """
    try:
        google_id = user_data.get('googleId')
        email = user_data.get('email')
        name = user_data.get('name')
        picture = user_data.get('picture')
        email_verified = user_data.get('emailVerified', False)
        
        if not email or not email_verified:
            return JsonResponse({
                'success': False,
                'message': 'Email verification required'
            }, status=400)
        
        # Check if user exists
        user = None
        try:
            user = User.objects.get(email=email)
            # Update user info if needed
            if user.first_name != name:
                user.first_name = name
                user.save()
        except User.DoesNotExist:
            # Create new user
            username = email.split('@')[0]
            # Ensure username is unique
            counter = 1
            original_username = username
            while User.objects.filter(username=username).exists():
                username = f"{original_username}{counter}"
                counter += 1
            
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=name,
                is_active=True
            )
            
            # You can store additional Google-specific data here
            # Example: Create a UserProfile model to store google_id, picture, etc.
        
        # Log the user in
        login(request, user)
        
        return JsonResponse({
            'success': True,
            'message': 'Google authentication successful',
            'redirect_url': '/',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'name': user.first_name,
            }
        })
        
    except Exception as e:
        logger.error(f"Google login error: {str(e)}")
        return JsonResponse({
            'success': False,
            'message': 'Google authentication failed'
        }, status=500)

def handle_facebook_login(request, user_data):
    """
    Handle Facebook OAuth login (similar to Google)
    """
    try:
        facebook_id = user_data.get('facebookId')
        email = user_data.get('email')
        name = user_data.get('name')
        
        if not email:
            return JsonResponse({
                'success': False,
                'message': 'Email is required for Facebook login'
            }, status=400)
        
        # Similar logic to Google login
        user = None
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            username = email.split('@')[0]
            counter = 1
            original_username = username
            while User.objects.filter(username=username).exists():
                username = f"{original_username}{counter}"
                counter += 1
            
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=name,
                is_active=True
            )
        
        login(request, user)
        
        return JsonResponse({
            'success': True,
            'message': 'Facebook authentication successful',
            'redirect_url': '/',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'name': user.first_name,
            }
        })
        
    except Exception as e:
        logger.error(f"Facebook login error: {str(e)}")
        return JsonResponse({
            'success': False,
            'message': 'Facebook authentication failed'
        }, status=500)


def _get_session_cart(request):
    """Helper to return the cart stored in session."""
    try:
        return request.session.get('cart', [])
    except Exception:
        return []


def _save_session_cart(request, cart):
    request.session['cart'] = cart
    request.session.modified = True


def _cart_totals(cart):
    total_qty = sum((item.get('qty', 1) for item in cart))
    total_price = sum((item.get('price', 0) * item.get('qty', 1) for item in cart))
    return total_qty, total_price


@require_http_methods(["GET", "POST", "PATCH", "DELETE"])
def api_cart(request):
    """Simple session-backed cart API.

    GET -> returns cart
    POST -> add item or perform action (add/remove/update/clear)
    PATCH -> update specific item qty
    DELETE -> clear cart
    """
    try:
        if request.method == 'GET':
            cart = _get_session_cart(request)
            qty, total = _cart_totals(cart)
            return JsonResponse({'success': True, 'cart': cart, 'total_qty': qty, 'total_price': total})

        # For POST/PATCH, read JSON body
        try:
            data = json.loads(request.body.decode('utf-8') or '{}')
        except Exception:
            data = {}

        cart = _get_session_cart(request)
        action = data.get('action', 'add')

        if request.method == 'DELETE' or action == 'clear':
            cart = []
            _save_session_cart(request, cart)
            return JsonResponse({'success': True, 'cart': cart, 'message': 'Cart cleared'})

        if action == 'add':
            name = data.get('name')
            price = int(data.get('price', 0) or 0)
            image = data.get('image', '')
            qty = int(data.get('qty', 1) or 1)
            if not name:
                return JsonResponse({'success': False, 'message': 'Missing item name'}, status=400)

            existing = next((i for i in cart if i.get('name') == name and i.get('price') == price), None)
            if existing:
                existing['qty'] = existing.get('qty', 1) + qty
            else:
                cart.append({'name': name, 'price': price, 'image': image, 'qty': qty})

            _save_session_cart(request, cart)
            qty, total = _cart_totals(cart)
            return JsonResponse({'success': True, 'cart': cart, 'total_qty': qty, 'total_price': total})

        if action == 'remove':
            name = data.get('name')
            price = int(data.get('price', 0) or 0)
            if not name:
                return JsonResponse({'success': False, 'message': 'Missing item name'}, status=400)
            existing = next((i for i in cart if i.get('name') == name and i.get('price') == price), None)
            if existing:
                existing['qty'] = existing.get('qty', 1) - 1
                if existing['qty'] <= 0:
                    cart = [i for i in cart if not (i.get('name') == name and i.get('price') == price)]
                _save_session_cart(request, cart)
                qty, total = _cart_totals(cart)
                return JsonResponse({'success': True, 'cart': cart, 'total_qty': qty, 'total_price': total})
            else:
                return JsonResponse({'success': False, 'message': 'Item not in cart'}, status=404)

        if action == 'update' or request.method == 'PATCH':
            name = data.get('name')
            price = int(data.get('price', 0) or 0)
            qty_val = int(data.get('qty', 0) or 0)
            if not name:
                return JsonResponse({'success': False, 'message': 'Missing item name'}, status=400)
            new_cart = []
            found = False
            for i in cart:
                if i.get('name') == name and i.get('price') == price:
                    found = True
                    if qty_val > 0:
                        i['qty'] = qty_val
                        new_cart.append(i)
                    # if qty_val <=0 we remove the item
                else:
                    new_cart.append(i)
            if not found:
                return JsonResponse({'success': False, 'message': 'Item not in cart'}, status=404)
            cart = new_cart
            _save_session_cart(request, cart)
            qty, total = _cart_totals(cart)
            return JsonResponse({'success': True, 'cart': cart, 'total_qty': qty, 'total_price': total})

        return JsonResponse({'success': False, 'message': 'Unsupported action/method'}, status=400)

    except Exception as e:
        logger.error(f"Cart API error: {str(e)}")
        return JsonResponse({'success': False, 'message': 'Internal server error'}, status=500)


@require_http_methods(["POST"])
def api_cart_checkout(request):
    """Place an order using current session cart. This is a simple simulated order placement
    that stores the order in session under 'orders' and clears the cart.
    """
    try:
        cart = _get_session_cart(request)
        if not cart:
            return JsonResponse({'success': False, 'message': 'Cart is empty'}, status=400)

        # compute subtotal and fees on server-side to avoid client tampering
        _, subtotal = _cart_totals(cart)
        delivery_fee = 40
        taxes = int(round(subtotal * 0.08))
        total_with_fees = subtotal + delivery_fee + taxes

        order = {
            'id': int(time.time()),
            'items': cart,
            'subtotal': subtotal,
            'delivery_fee': delivery_fee,
            'taxes': taxes,
            'total': total_with_fees,
            'status': 'placed'
        }

        # Persist the order to DB for authenticated users
        if request.user.is_authenticated:
            try:
                db_order = Order.objects.create(
                    user=request.user,
                    subtotal=subtotal,
                    delivery_fee=delivery_fee,
                    taxes=taxes,
                    total=total_with_fees,
                    status='placed',
                )
                for item in cart:
                    OrderItem.objects.create(
                        order=db_order,
                        name=item.get('name', ''),
                        price=int(item.get('price', 0) or 0),
                        qty=int(item.get('qty', 1) or 1),
                        image=item.get('image', '')
                    )
            except Exception as e:
                logger.exception(f"Failed to persist order for user {request.user}: {e}")

        # keep a lightweight copy in session for compatibility
        orders = request.session.get('orders', [])
        orders.append(order)
        request.session['orders'] = orders
        # clear cart
        request.session['cart'] = []
        request.session.modified = True

        return JsonResponse({'success': True, 'order': order, 'message': 'Order placed successfully'})
    except Exception as e:
        logger.error(f"Checkout error: {str(e)}")
        return JsonResponse({'success': False, 'message': 'Checkout failed'}, status=500)


def profile_view(request):
    """Render user profile page."""
    if not request.user.is_authenticated:
        # Redirect to login in a real app; for now show a simple message
        return render(request, 'login.html', {})
    return render(request, 'profile.html')


@require_http_methods(["GET"])
def api_profile(request):
    """Return profile JSON including orders, saved items and cart."""
    try:
        user = request.user
        if not user.is_authenticated:
            # return limited info for anonymous users
            orders = request.session.get('orders', [])
            cart = request.session.get('cart', [])
            return JsonResponse({'success': True, 'user': None, 'orders': orders, 'cart': cart, 'saved': []})

        # Authenticated user: load from DB
        profile = getattr(user, 'profile', None)
        saved_qs = SavedItem.objects.filter(user=user).order_by('-created_at')
        saved = [{'name': s.name, 'price': s.price, 'image': s.image, 'id': s.id} for s in saved_qs]

        orders_qs = Order.objects.filter(user=user).order_by('-created_at')[:50]
        orders = []
        for o in orders_qs:
            items = [{'name': it.name, 'price': it.price, 'qty': it.qty, 'image': it.image} for it in o.items.all()]
            orders.append({'id': o.id, 'created_at': o.created_at.isoformat(), 'subtotal': o.subtotal, 'delivery_fee': o.delivery_fee, 'taxes': o.taxes, 'total': o.total, 'status': o.status, 'items': items})

        cart_items = CartItem.objects.filter(user=user)
        cart = [{'name': c.name, 'price': c.price, 'qty': c.qty, 'image': c.image} for c in cart_items]

        user_info = {'id': user.id, 'username': user.username, 'email': user.email, 'name': user.first_name}
        return JsonResponse({'success': True, 'user': user_info, 'orders': orders, 'cart': cart, 'saved': saved})
    except Exception as e:
        logger.exception(f"api_profile error: {e}")
        return JsonResponse({'success': False, 'message': 'Failed to load profile'}, status=500)


@csrf_exempt
@require_http_methods(["POST", "DELETE"])
def api_profile_saved(request):
    """Add or remove a saved item for the authenticated user.

    POST body: { name, price, image }
    DELETE body: { id } or { name }
    """
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'Authentication required'}, status=401)
    try:
        data = json.loads(request.body.decode('utf-8') or '{}')
    except Exception:
        data = {}

    if request.method == 'POST':
        name = data.get('name')
        price = int(data.get('price', 0) or 0)
        image = data.get('image', '')
        if not name:
            return JsonResponse({'success': False, 'message': 'Missing name'}, status=400)
        s = SavedItem.objects.create(user=request.user, name=name, price=price, image=image)
        return JsonResponse({'success': True, 'saved': {'id': s.id, 'name': s.name, 'price': s.price, 'image': s.image}})

    # DELETE
    if request.method == 'DELETE':
        item_id = data.get('id')
        name = data.get('name')
        qs = SavedItem.objects.filter(user=request.user)
        if item_id:
            qs = qs.filter(id=item_id)
        elif name:
            qs = qs.filter(name=name)
        deleted = qs.delete()
        return JsonResponse({'success': True, 'deleted': deleted[0]})


def logout_view(request):
    """Log out the user and redirect to home page."""
    logout(request)
    return redirect('/')
