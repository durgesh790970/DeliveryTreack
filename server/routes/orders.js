const express = require('express');
const { body, validationResult } = require('express-validator');
const Order = require('../models/Order');
const User = require('../models/User');
const protect = require('../middleware/auth');

const router = express.Router();

// @route   GET /api/orders
// @desc    Get all orders for logged-in user
// @access  Private
router.get('/', protect, async (req, res) => {
  try {
    const orders = await Order.find({ userId: req.user.id }).sort({
      createdAt: -1,
    });

    res.status(200).json({
      success: true,
      count: orders.length,
      orders,
    });
  } catch (error) {
    console.error(error);
    res.status(500).json({
      success: false,
      message: 'Server error',
      error: error.message,
    });
  }
});

// @route   GET /api/orders/:id
// @desc    Get single order by ID
// @access  Private
router.get('/:id', protect, async (req, res) => {
  try {
    const order = await Order.findById(req.params.id);

    if (!order) {
      return res.status(404).json({
        success: false,
        message: 'Order not found',
      });
    }

    // Check if order belongs to user
    if (order.userId.toString() !== req.user.id) {
      return res.status(403).json({
        success: false,
        message: 'Not authorized to access this order',
      });
    }

    res.status(200).json({
      success: true,
      order,
    });
  } catch (error) {
    console.error(error);
    res.status(500).json({
      success: false,
      message: 'Server error',
      error: error.message,
    });
  }
});

// @route   POST /api/orders
// @desc    Create new order
// @access  Private
router.post(
  '/',
  protect,
  [
    body('items', 'Items array is required').isArray({ min: 1 }),
    body('totalAmount', 'Total amount is required').isFloat({ min: 0 }),
    body('paymentMode', 'Payment mode is required').isIn(['Cash', 'Online', 'Card']),
    body('deliveryAddress', 'Delivery address is required').trim().notEmpty(),
  ],
  async (req, res) => {
    // Check for validation errors
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        errors: errors.array(),
      });
    }

    try {
      const { items, totalAmount, paymentMode, deliveryAddress, restaurantName, notes } =
        req.body;

      // Create new order
      const order = new Order({
        userId: req.user.id,
        items,
        totalAmount,
        paymentMode,
        deliveryAddress,
        restaurantName: restaurantName || 'Food Delivery',
        notes,
      });

      // Save order
      await order.save();

      // Update user stats
      await User.findByIdAndUpdate(
        req.user.id,
        {
          $inc: {
            totalOrdersCount: 1,
            totalAmountSpent: totalAmount,
          },
        },
        { new: true }
      );

      res.status(201).json({
        success: true,
        message: 'Order created successfully',
        order,
      });
    } catch (error) {
      console.error(error);
      res.status(500).json({
        success: false,
        message: 'Server error',
        error: error.message,
      });
    }
  }
);

// @route   PUT /api/orders/:id
// @desc    Update order status
// @access  Private
router.put('/:id', protect, async (req, res) => {
  try {
    const { status, paymentStatus } = req.body;

    let order = await Order.findById(req.params.id);

    if (!order) {
      return res.status(404).json({
        success: false,
        message: 'Order not found',
      });
    }

    // Check if order belongs to user
    if (order.userId.toString() !== req.user.id) {
      return res.status(403).json({
        success: false,
        message: 'Not authorized to update this order',
      });
    }

    // Update status
    if (status) {
      order.status = status;

      // Set delivered or cancelled timestamp
      if (status === 'Delivered') {
        order.deliveredAt = new Date();
      } else if (status === 'Cancelled') {
        order.cancelledAt = new Date();
      }
    }

    // Update payment status
    if (paymentStatus) {
      order.paymentStatus = paymentStatus;
    }

    await order.save();

    res.status(200).json({
      success: true,
      message: 'Order updated successfully',
      order,
    });
  } catch (error) {
    console.error(error);
    res.status(500).json({
      success: false,
      message: 'Server error',
      error: error.message,
    });
  }
});

// @route   DELETE /api/orders/:id
// @desc    Cancel order
// @access  Private
router.delete('/:id', protect, async (req, res) => {
  try {
    const order = await Order.findById(req.params.id);

    if (!order) {
      return res.status(404).json({
        success: false,
        message: 'Order not found',
      });
    }

    // Check if order belongs to user
    if (order.userId.toString() !== req.user.id) {
      return res.status(403).json({
        success: false,
        message: 'Not authorized to cancel this order',
      });
    }

    // Only allow cancelling if not delivered
    if (order.status === 'Delivered' || order.status === 'Cancelled') {
      return res.status(400).json({
        success: false,
        message: `Cannot cancel order with status: ${order.status}`,
      });
    }

    order.status = 'Cancelled';
    order.cancelledAt = new Date();
    await order.save();

    res.status(200).json({
      success: true,
      message: 'Order cancelled successfully',
      order,
    });
  } catch (error) {
    console.error(error);
    res.status(500).json({
      success: false,
      message: 'Server error',
      error: error.message,
    });
  }
});

module.exports = router;
