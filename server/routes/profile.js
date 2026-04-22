const express = require('express');
const { body, validationResult } = require('express-validator');
const User = require('../models/User');
const Order = require('../models/Order');
const protect = require('../middleware/auth');

const router = express.Router();

// @route   GET /api/profile
// @desc    Get user profile
// @access  Private
router.get('/', protect, async (req, res) => {
  try {
    const user = await User.findById(req.user.id);

    if (!user) {
      return res.status(404).json({
        success: false,
        message: 'User not found',
      });
    }

    res.status(200).json({
      success: true,
      user: {
        id: user._id,
        name: user.name,
        email: user.email,
        phone: user.phone,
        address: user.address,
        city: user.city,
        zipCode: user.zipCode,
        totalOrdersCount: user.totalOrdersCount,
        totalAmountSpent: user.totalAmountSpent,
      },
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

// @route   PUT /api/profile
// @desc    Update user profile
// @access  Private
router.put(
  '/',
  protect,
  [
    body('name', 'Name is required').trim().notEmpty(),
    body('phone', 'Phone must be a valid number').optional().isMobilePhone(),
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
      const { name, phone, address, city, zipCode } = req.body;

      // Find and update user
      let user = await User.findById(req.user.id);

      if (!user) {
        return res.status(404).json({
          success: false,
          message: 'User not found',
        });
      }

      // Update fields
      if (name) user.name = name;
      if (phone) user.phone = phone;
      if (address) user.address = address;
      if (city) user.city = city;
      if (zipCode) user.zipCode = zipCode;

      await user.save();

      res.status(200).json({
        success: true,
        message: 'Profile updated successfully',
        user: {
          id: user._id,
          name: user.name,
          email: user.email,
          phone: user.phone,
          address: user.address,
          city: user.city,
          zipCode: user.zipCode,
        },
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

module.exports = router;
