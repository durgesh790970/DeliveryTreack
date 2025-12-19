const restaurants = [
  { name: "Spice Hub", category: "Indian", deliveryTime: "30 mins", offer: "20% OFF" },
  { name: "Dragon House", category: "Chinese", deliveryTime: "40 mins", offer: "Free Spring Roll" },
  { name: "Sweet Treats", category: "Desserts", deliveryTime: "20 mins", offer: "10% Cashback" },
  { name: "Global Bites", category: "All", deliveryTime: "35 mins", offer: "Flat ₹50 OFF" },
  // Add more restaurants as needed
  { name: "Pizza Palace", category: "Italian", deliveryTime: "25 mins", offer: "Buy 1 Get 1 Free" },
  { name: "Sushi World", category: "Japanese", deliveryTime: "45 mins", offer: "15% OFF" },
  { name: "Taco Fiesta", category: "Mexican", deliveryTime: "30 mins", offer: "Free Drink with Order" },
  { name: "Healthy Greens", category: "Salads", deliveryTime: "20 mins", offer: "10% OFF on First Order" },
  { name: "Spice Hub", category: "Indian", deliveryTime: "30 mins", offer: "20% OFF" },
  { name: "Dragon House", category: "Chinese", deliveryTime: "40 mins", offer: "Free Spring Roll" },
  { name: "Sweet Treats", category: "Desserts", deliveryTime: "20 mins", offer: "10% Cashback" },
  { name: "Global Bites", category: "All", deliveryTime: "35 mins", offer: "Flat ₹50 OFF" },
  { name: "Biryani Bazaar", category: "Indian", deliveryTime: "35 mins", offer: "Buy 2 Get 1 Free" },
{ name: "Dosa Express", category: "Indian", deliveryTime: "20 mins", offer: "15% OFF" },
{ name: "Tandoori Town", category: "Indian", deliveryTime: "30 mins", offer: "10% OFF" },
{ name: "Chaat Street", category: "Indian", deliveryTime: "20 mins", offer: "Buy 1 Get 1 Free" },
{ name: "Roti Ghar", category: "Indian", deliveryTime: "30 mins", offer: "20% OFF on Combos" },
{ name: "Dhaba Punjabi Tadka", category: "Indian", deliveryTime: "40 mins", offer: "Buy 1 Get 1 Free Lassi" },
{ name: "Curry Palace", category: "Indian", deliveryTime: "35 mins", offer: "15% OFF for first-timers" },
{ name: "South Indian Foods", category: "Indian", deliveryTime: "30 mins", offer: "10% OFF Dosas & Idlis" },
{ name: "North Bites", category: "Indian", deliveryTime: "25 mins", offer: "Buy 1 Get 1 Free Paratha" },
{ name: "The Royal Thali", category: "Indian", deliveryTime: "45 mins", offer: "20% OFF Thali Combos" },
{ name: "Punjabi Dhaba Express", category: "Indian", deliveryTime: "30 mins", offer: "Free Chaas with Meals" },
{ name: "Gujrati Gathiya", category: "Indian", deliveryTime: "20 mins", offer: "10% OFF Snack Combos" },
{ name: "Rajasthani Bhojanalay", category: "Indian", deliveryTime: "35 mins", offer: "15% OFF Royal Meals" },
{ name: "Bengali Sweets & Eats", category: "Indian", deliveryTime: "30 mins", offer: "Buy 2 Get 1 Free Sweet" },
{ name: "Hyderabadi Zaiqa", category: "Indian", deliveryTime: "40 mins", offer: "20% OFF Biryanis" },
{ name: "Malvani Foods", category: "Indian", deliveryTime: "30 mins", offer: "Free Papad with Thali" },
{ name: "Awadhi Cuisine Hub", category: "Indian", deliveryTime: "45 mins", offer: "15% OFF" },
{ name: "Chettinad Foods", category: "Indian", deliveryTime: "30 mins", offer: "10% OFF Curries" },
{ name: "Parathe Wale Gali", category: "Indian", deliveryTime: "20 mins", offer: "Buy 1 Get 1 Paratha Free" },
{ name: "Delhi 6 Foods", category: "Indian", deliveryTime: "30 mins", offer: "20% OFF Street Foods" },

];

let cart = []

function loadRestaurants(filter = "All") {
  const list = document.getElementById("restaurantList");
  if (!list) return;
  list.innerHTML = "";

  const filtered = filter === "All" ? restaurants : restaurants.filter(r => r.category === filter);

  filtered.forEach(r => {
    const div = document.createElement("div");
    div.className = "restaurant-card";
    div.innerHTML = `
      <h3>${r.name}</h3>
      <p>Category: ${r.category}</p>
      <p>Delivery Time: ${r.deliveryTime}</p>
      <p>Offer: <strong>${r.offer}</strong></p>
      <button onclick="addToCart('${r.name}')">Add to Cart</button>
    `;
    list.appendChild(div);
  });
}

function search() {
  const input = document.getElementById("search").value.toLowerCase();
  const list = document.getElementById("restaurantList");
  list.innerHTML = "";

  const results = restaurants.filter(r => r.name.toLowerCase().includes(input));
  results.forEach(r => {
    const div = document.createElement("div");
    div.className = "restaurant-card";
    div.innerHTML = `
      <h3>${r.name}</h3>
      <p>Category: ${r.category}</p>
      <p>Delivery Time: ${r.deliveryTime}</p>
      <p>Offer: <strong>${r.offer}</strong></p>
      <button onclick="addToCart('${r.name}')">Add to Cart</button>
    `;
    list.appendChild(div);
  });
}

function filterCategory(category) {
  loadRestaurants(category);
}

function addToCart(itemName) {
  cart.push(itemName);
  alert(`${itemName} added to cart!`);
  updateCartDisplay();
}

function updateCartDisplay() {
  // Update nav cart count
  const navCart = document.getElementById("cartCountNav");
  if (navCart) navCart.textContent = cart.length;
  // Update footer cart count
  const footerCart = document.getElementById("cartCountFooter");
  if (footerCart) footerCart.textContent = cart.length;  // Update footer order button
  const footer = document.querySelector("footer");
  if (footer) {
    footer.innerHTML = <p>Cart Items: <span id="cartCountFooter">${cart.length}</span></p>;
  }
}

function placeOrder() {
  if (cart.length === 0) {
    alert("Cart is empty!");
    return;
  }
  alert("Order placed for: " + cart.join(", "));
  cart = [];
  updateCartDisplay();
}

// Auto-load when index.html runs
if (document.getElementById("restaurantList")) {
  loadRestaurants();
}

document.addEventListener("DOMContentLoaded", function() {
  const cartBtn = document.getElementById("cartBtn");
  if (cartBtn) {
    cartBtn.addEventListener("click", function() {
      if (cart.length === 0) {
        alert("Cart is empty!");
      } else {
        alert("Order placed for: " + cart.join(", "));
        cart = [];
        updateCartDisplay();
      }
    });
  }
  updateCartDisplay();
});