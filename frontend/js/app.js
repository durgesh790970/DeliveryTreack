// API Configuration
const API_URL = 'http://localhost:5000/api';

// ======================
// AUTH STATE MANAGEMENT
// ======================

class AuthManager {
  constructor() {
    this.token = localStorage.getItem('token');
    this.user = this.getStoredUser();
  }

  // Store token in localStorage
  saveToken(token) {
    localStorage.setItem('token', token);
    this.token = token;
  }

  // Store user data in localStorage
  saveUser(user) {
    localStorage.setItem('user', JSON.stringify(user));
    this.user = user;
  }

  // Get stored user from localStorage
  getStoredUser() {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  }

  // Check if user is logged in
  isLoggedIn() {
    return !!this.token && !!this.user;
  }

  // Get current user
  getCurrentUser() {
    return this.user;
  }

  // Get token
  getToken() {
    return this.token;
  }

  // Logout - clear everything
  logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    this.token = null;
    this.user = null;
  }

  // Verify token with backend
  async verifyToken() {
    if (!this.token) return false;

    try {
      const response = await fetch(`${API_URL}/auth/verify`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${this.token}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        this.saveUser(data.user);
        return true;
      } else {
        this.logout();
        return false;
      }
    } catch (error) {
      console.error('Token verification error:', error);
      return false;
    }
  }
}

// Initialize auth manager
const auth = new AuthManager();

// ======================
// API HELPER FUNCTIONS
// ======================

// Make API calls with authentication
async function apiCall(endpoint, options = {}) {
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  // Add token if available
  if (auth.getToken()) {
    headers.Authorization = `Bearer ${auth.getToken()}`;
  }

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers,
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.message || 'API error');
  }

  return data;
}

// ======================
// SIGNUP
// ======================

async function handleSignup(event) {
  event.preventDefault();

  const name = document.getElementById('signup-name').value.trim();
  const email = document.getElementById('signup-email').value.trim();
  const password = document.getElementById('signup-password').value;
  const confirmPassword = document.getElementById('signup-confirm-password').value;

  // Validation
  if (!name || !email || !password) {
    showError('Please fill in all fields');
    return;
  }

  if (password !== confirmPassword) {
    showError('Passwords do not match');
    return;
  }

  if (password.length < 6) {
    showError('Password must be at least 6 characters');
    return;
  }

  try {
    showLoading(true);

    const response = await apiCall('/auth/signup', {
      method: 'POST',
      body: JSON.stringify({
        name,
        email,
        password,
      }),
    });

    showSuccess('Account created successfully! Redirecting to login...');

    // Redirect to login after 2 seconds
    setTimeout(() => {
      window.location.href = '/login/';
    }, 2000);
  } catch (error) {
    showError(error.message);
  } finally {
    showLoading(false);
  }
}

// ======================
// LOGIN
// ======================

async function handleLogin(event) {
  event.preventDefault();

  const email = document.getElementById('login-email').value.trim();
  const password = document.getElementById('login-password').value;

  // Validation
  if (!email || !password) {
    showError('Please fill in all fields');
    return;
  }

  try {
    showLoading(true);

    const response = await apiCall('/auth/login', {
      method: 'POST',
      body: JSON.stringify({
        email,
        password,
      }),
    });

    // Save token and user
    auth.saveToken(response.token);
    auth.saveUser(response.user);

    showSuccess('Login successful! Redirecting to home...');

    // Redirect to home after 2 seconds
    setTimeout(() => {
      window.location.href = '/';
    }, 2000);
  } catch (error) {
    showError(error.message);
  } finally {
    showLoading(false);
  }
}

// ======================
// PROFILE
// ======================

async function loadProfile() {
  try {
    // Check if user is logged in
    if (!auth.isLoggedIn()) {
      window.location.href = '/login/';
      return;
    }

    showLoading(true);

    // Fetch profile data
    const response = await apiCall('/profile', {
      method: 'GET',
    });

    const user = response.user;

    // Display user information
    document.getElementById('profile-name').textContent = user.name;
    document.getElementById('profile-email').textContent = user.email;
    document.getElementById('profile-phone').textContent = user.phone || 'Not provided';
    document.getElementById('profile-address').textContent = user.address || 'Not provided';
    document.getElementById('profile-city').textContent = user.city || 'Not provided';
    document.getElementById('profile-zipcode').textContent = user.zipCode || 'Not provided';
    document.getElementById('profile-total-orders').textContent = user.totalOrdersCount;
    document.getElementById('profile-total-spent').textContent = `$${user.totalAmountSpent.toFixed(2)}`;

    // Load order history
    loadOrderHistory();
  } catch (error) {
    showError(error.message);
  } finally {
    showLoading(false);
  }
}

// ======================
// ORDER HISTORY
// ======================

async function loadOrderHistory() {
  try {
    const response = await apiCall('/orders', {
      method: 'GET',
    });

    const orders = response.orders;
    const orderList = document.getElementById('order-history');

    if (!orders || orders.length === 0) {
      orderList.innerHTML = '<p class="no-orders">No orders yet</p>';
      return;
    }

    let html = `
      <div class="orders-table-container">
        <table class="orders-table">
          <thead>
            <tr>
              <th>Date</th>
              <th>Restaurant</th>
              <th>Amount</th>
              <th>Status</th>
              <th>Payment</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
    `;

    orders.forEach((order) => {
      const date = new Date(order.createdAt).toLocaleDateString();
      const statusClass = `status-${order.status.toLowerCase()}`;

      html += `
        <tr>
          <td>${date}</td>
          <td>${order.restaurantName}</td>
          <td>$${order.totalAmount.toFixed(2)}</td>
          <td><span class="badge ${statusClass}">${order.status}</span></td>
          <td>${order.paymentMode}</td>
          <td>
            <button onclick="viewOrderDetails('${order._id}')" class="btn-small">View</button>
            ${order.status !== 'Delivered' && order.status !== 'Cancelled' ? `<button onclick="cancelOrder('${order._id}')" class="btn-small btn-danger">Cancel</button>` : ''}
          </td>
        </tr>
      `;
    });

    html += `
          </tbody>
        </table>
      </div>
    `;

    orderList.innerHTML = html;
  } catch (error) {
    console.error('Error loading orders:', error);
  }
}

// View order details
async function viewOrderDetails(orderId) {
  try {
    const response = await apiCall(`/orders/${orderId}`, {
      method: 'GET',
    });

    const order = response.order;

    let itemsHtml = '';
    order.items.forEach((item) => {
      itemsHtml += `
        <div class="order-item">
          <span>${item.foodName} x${item.quantity}</span>
          <span>$${item.totalPrice.toFixed(2)}</span>
        </div>
      `;
    });

    const modal = `
      <div class="modal" id="orderModal">
        <div class="modal-content">
          <span class="close" onclick="closeOrderModal()">&times;</span>
          <h2>Order Details</h2>
          <div class="order-details">
            <p><strong>Order ID:</strong> ${order._id}</p>
            <p><strong>Date:</strong> ${new Date(order.createdAt).toLocaleString()}</p>
            <p><strong>Restaurant:</strong> ${order.restaurantName}</p>
            <p><strong>Status:</strong> <span class="badge status-${order.status.toLowerCase()}">${order.status}</span></p>
            <p><strong>Delivery Address:</strong> ${order.deliveryAddress}</p>
            <p><strong>Payment Mode:</strong> ${order.paymentMode}</p>
            <p><strong>Payment Status:</strong> ${order.paymentStatus}</p>
            <h3>Items:</h3>
            <div class="items-list">
              ${itemsHtml}
            </div>
            <p><strong>Total Amount:</strong> $${order.totalAmount.toFixed(2)}</p>
            ${order.estimatedDeliveryTime ? `<p><strong>Est. Delivery:</strong> ${new Date(order.estimatedDeliveryTime).toLocaleString()}</p>` : ''}
          </div>
        </div>
      </div>
    `;

    document.body.insertAdjacentHTML('beforeend', modal);
    document.getElementById('orderModal').style.display = 'block';
  } catch (error) {
    showError(error.message);
  }
}

function closeOrderModal() {
  const modal = document.getElementById('orderModal');
  if (modal) {
    modal.remove();
  }
}

// Cancel order
async function cancelOrder(orderId) {
  if (!confirm('Are you sure you want to cancel this order?')) {
    return;
  }

  try {
    showLoading(true);

    await apiCall(`/orders/${orderId}`, {
      method: 'DELETE',
    });

    showSuccess('Order cancelled successfully');
    loadOrderHistory();
  } catch (error) {
    showError(error.message);
  } finally {
    showLoading(false);
  }
}

// ======================
// UPDATE PROFILE
// ======================

async function handleProfileUpdate(event) {
  event.preventDefault();

  const name = document.getElementById('edit-name').value.trim();
  const phone = document.getElementById('edit-phone').value.trim();
  const address = document.getElementById('edit-address').value.trim();
  const city = document.getElementById('edit-city').value.trim();
  const zipCode = document.getElementById('edit-zipcode').value.trim();

  if (!name) {
    showError('Name is required');
    return;
  }

  try {
    showLoading(true);

    await apiCall('/profile', {
      method: 'PUT',
      body: JSON.stringify({
        name,
        phone,
        address,
        city,
        zipCode,
      }),
    });

    showSuccess('Profile updated successfully');
    setTimeout(() => {
      loadProfile();
    }, 1500);
  } catch (error) {
    showError(error.message);
  } finally {
    showLoading(false);
  }
}

// ======================
// PLACE NEW ORDER
// ======================

async function createOrder(items, totalAmount, paymentMode, deliveryAddress, restaurantName = '') {
  try {
    if (!auth.isLoggedIn()) {
      showError('Please login to place an order');
      setTimeout(() => {
        window.location.href = '/login/';
      }, 2000);
      return;
    }

    showLoading(true);

    const response = await apiCall('/orders', {
      method: 'POST',
      body: JSON.stringify({
        items,
        totalAmount,
        paymentMode,
        deliveryAddress,
        restaurantName,
      }),
    });

    showSuccess('Order placed successfully!');
    return response.order;
  } catch (error) {
    showError(error.message);
    throw error;
  } finally {
    showLoading(false);
  }
}

// ======================
// LOGOUT
// ======================

function handleLogout() {
  auth.logout();
  showSuccess('Logged out successfully');
  setTimeout(() => {
    window.location.href = '/';
  }, 1500);
}

// ======================
// UI HELPER FUNCTIONS
// ======================

function showError(message) {
  const errorDiv = document.createElement('div');
  errorDiv.className = 'alert alert-error';
  errorDiv.textContent = message;
  document.body.insertAdjacentElement('afterbegin', errorDiv);

  setTimeout(() => {
    errorDiv.remove();
  }, 5000);
}

function showSuccess(message) {
  const successDiv = document.createElement('div');
  successDiv.className = 'alert alert-success';
  successDiv.textContent = message;
  document.body.insertAdjacentElement('afterbegin', successDiv);

  setTimeout(() => {
    successDiv.remove();
  }, 5000);
}

function showLoading(isLoading) {
  let loader = document.getElementById('loader');
  if (isLoading) {
    if (!loader) {
      loader = document.createElement('div');
      loader.id = 'loader';
      loader.className = 'loader';
      loader.innerHTML = '<div class="spinner"></div>';
      document.body.appendChild(loader);
    }
    loader.style.display = 'block';
  } else {
    if (loader) {
      loader.style.display = 'none';
    }
  }
}

// ======================
// UPDATE UI BASED ON AUTH STATE
// ======================

function updateAuthUI() {
  const isLoggedIn = auth.isLoggedIn();

  // Hide/show profile button
  const profileBtn = document.getElementById('profile-btn');
  const logoutBtn = document.getElementById('logout-btn');
  const loginBtn = document.getElementById('login-btn');
  const signupBtn = document.getElementById('signup-btn');

  if (profileBtn) profileBtn.style.display = isLoggedIn ? 'block' : 'none';
  if (logoutBtn) logoutBtn.style.display = isLoggedIn ? 'block' : 'none';
  if (loginBtn) loginBtn.style.display = isLoggedIn ? 'none' : 'block';
  if (signupBtn) signupBtn.style.display = isLoggedIn ? 'none' : 'block';

  // Hide login/signup pages if already logged in
  const loginForm = document.getElementById('login-form');
  const signupForm = document.getElementById('signup-form');

  if (loginForm && isLoggedIn) {
    window.location.href = '/';
  }

  if (signupForm && isLoggedIn) {
    window.location.href = '/';
  }
}

// Initialize auth UI when page loads
document.addEventListener('DOMContentLoaded', () => {
  // Verify token on page load
  if (auth.getToken()) {
    auth.verifyToken();
  }

  updateAuthUI();

  // Show user name in navbar if exists
  if (auth.isLoggedIn()) {
    const user = auth.getCurrentUser();
    const userNameEl = document.getElementById('user-name');
    if (userNameEl) {
      userNameEl.textContent = user.name;
    }
  }
});

// ======================
// EXPORT FOR TESTING
// ======================
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    auth,
    handleSignup,
    handleLogin,
    handleLogout,
  };
}
