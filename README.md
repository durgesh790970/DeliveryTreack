# DeliveryTreack
DeliveryTrack is a smart food delivery tracking platform that provides users with real-time order status, live location tracking, and accurate delivery updates. Its simple and fast interface gives users a smooth, reliable, and transparent experience from placing the order to delivery.
Profile feature setup

1) Apply migrations to create new models (run from project root `d:\All_Project\Food\durgesh`):

```powershell
cd d:\All_Project\Food\durgesh
python manage.py makemigrations
python manage.py migrate
```

2) (Optional) Create a superuser to view orders in admin:

```powershell
python manage.py createsuperuser
```

3) Run the development server:

```powershell
python manage.py runserver
```

4) How it works:
- The profile page is at `/profile/` and fetches data from `/api/profile/`.
- When an authenticated user completes checkout via `/api/cart/checkout/`, the order is persisted into the database (models: `Order`, `OrderItem`).
- Saved items are available at `/api/profile/saved/` (POST to add, DELETE to remove).
- Frontend uses polling (every 3s) to update purchase history and cart without a manual refresh. For true push (WebSocket) you can integrate Django Channels later.

5) Notes & next steps:
- Make sure `durgesh` is listed in `INSTALLED_APPS` (already added in settings).
- Uploaded profile pictures are stored under the `media/` folder (`MEDIA_ROOT`). Ensure your development server serves media (settings configured when `DEBUG=True`).
- If you want real-time push rather than polling, I can add Django Channels + Redis or socket.io integration next.




# 🏠 TiffinRush Home Page - Feature Summary

## ✅ **Complete Home Screen Implementation**

### 🎨 **Modern & Clean Design Features:**
- **Vibrant gradient header** - Orange to green (TiffinRush brand colors)
- **Rounded UI components** - All elements have smooth rounded corners
- **Floating animations** - Background elements with smooth floating effects
- **Clean typography** - Poppins font family throughout
- **Responsive design** - Optimized for mobile and desktop

### 🔍 **Search Bar Implementation:**
- **Prominent search bar** in header with search icon
- **Voice search integration** - Direct link to voice assistant
- **Real-time search** - Redirects to menu with search results
- **Keyboard shortcut** - Press '/' to focus search bar

### 🍽️ **Food Categories (8 Categories):**
1. **Pizza** 🍕
2. **Biryani** 🍛  
3. **Chinese** 🥡
4. **Burger** 🍔
5. **Dessert** 🍰
6. **Drinks** 🥤
7. **Indian** 🍜
8. **Healthy** 🥗

**Category Features:**
- **Hover animations** - Scale and rotate effects
- **Clickable navigation** - Direct to filtered menu
- **Visual feedback** - Shine effect on hover
- **Grid layout** - Responsive 4-column to 2-column grid

### 🔥 **Top Offers Section:**
1. **Flat ₹50 OFF** - On orders above ₹299 (Code: SAVE50)
2. **₹100 OFF** - First order special (Code: FIRST100)  
3. **Free Delivery** - On all orders today (No code needed)
4. **40% OFF** - Party orders above ₹999 (Code: PARTY40)

**Offer Features:**
- **Horizontal scrolling carousel**
- **Gradient backgrounds** with pulse animations
- **One-click copy codes** - Auto-copy to clipboard
- **Visual feedback** - Toast notifications

### 🏪 **Nearby Restaurants (4 Featured):**

#### **Restaurant 1: Domino's Pizza**
- **Rating:** ⭐ 4.3 (2.5k+ reviews)
- **Delivery:** 🚚 25-30 min  
- **Offer:** 💰 Free delivery above ₹299
- **Badge:** 30% OFF

#### **Restaurant 2: Biryani Express**
- **Rating:** ⭐ 4.5 (3.2k+ reviews)
- **Delivery:** 🚚 35-40 min
- **Offer:** 🎉 ₹100 OFF above ₹399  
- **Badge:** 40% OFF

#### **Restaurant 3: Burger King**
- **Rating:** ⭐ 4.2 (4.1k+ reviews)
- **Delivery:** 🚚 20-25 min
- **Offer:** 🔥 Free delivery + 50% OFF
- **Badge:** Buy 1 Get 1

#### **Restaurant 4: Wow! China**
- **Rating:** ⭐ 4.1 (1.8k+ reviews)
- **Delivery:** 🚚 30-35 min  
- **Offer:** 🎁 Buy 1 Get 1 on selected items
- **Badge:** 25% OFF

**Restaurant Features:**
- **Favorite system** - Heart toggle with localStorage
- **Order buttons** - Direct navigation to menu
- **Hover effects** - Lift animation on hover
- **Comprehensive info** - Rating, delivery time, offers

### 🎯 **Interactive Features:**

#### **Header Section:**
- **TiffinRush logo** - Clickable, leads to logo showcase
- **Location display** - Shows user location
- **Profile button** - Links to login/profile
- **Time-based greetings** - Good Morning/Afternoon/Evening
- **Quick actions** - Menu, Track, Cart, Top Rated buttons

#### **Navigation & UX:**
- **Bottom navigation** - 5 main sections
- **Floating Action Button** - Quick cart access
- **Pull-to-refresh** - Mobile refresh functionality
- **Keyboard shortcuts** - Enhanced accessibility
- **Toast notifications** - User feedback system

### 📱 **Responsive Design:**
- **Desktop:** 4-column category grid
- **Tablet:** 3-column category grid  
- **Mobile:** 2-column category grid
- **Adaptive layout** - All sections respond to screen size
- **Touch-friendly** - Large tap targets

### ⚡ **Performance Features:**
- **Smooth animations** - CSS transforms and transitions
- **Loading states** - Skeleton loading for better UX
- **Optimized images** - Emoji icons for fast loading
- **Entrance animations** - Staggered element appearance

### 🔗 **Integration Points:**
- **Voice Assistant** - Direct access from search bar
- **Menu System** - Category filtering integration
- **Cart System** - FAB and quick actions
- **Track Orders** - Header quick action
- **User Profile** - Header profile button

## 🚀 **Access Instructions:**

1. **Home Page**: Navigate to `/` (root URL)
2. **Logo Showcase**: Click TiffinRush logo or visit `/logo-showcase/`
3. **Voice Assistant**: Click 🎤 Voice button or visit `/voice-assistant/`
4. **Menu**: Click any category or visit `/menu/`

## 💡 **Technical Implementation:**

- **Django Views**: Complete home_view with context data
- **URL Routing**: Updated urlpatterns with home as root
- **CSS Framework**: Custom responsive CSS with modern design
- **JavaScript**: Interactive features and animations
- **LocalStorage**: Favorites and user preferences
- **Progressive Enhancement**: Works without JavaScript

## 🎨 **Color Scheme:**
- **Primary**: Orange (#ff6b35) to Green (#4caf50) gradients
- **Background**: Purple gradient (#667eea to #764ba2)
- **Accent Colors**: White, light grays for cards
- **Interactive**: Hover states with color transitions

Your TiffinRush home page is now a fully-featured, modern food delivery app interface with all requested components! 🎉
