const mongoose = require('mongoose');

const orderSchema = new mongoose.Schema(
  {
    userId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'User',
      required: true,
    },
    items: [
      {
        foodName: {
          type: String,
          required: true,
        },
        quantity: {
          type: Number,
          required: true,
        },
        price: {
          type: Number,
          required: true,
        },
        totalPrice: {
          type: Number,
          required: true,
        },
      },
    ],
    totalAmount: {
      type: Number,
      required: true,
    },
    status: {
      type: String,
      enum: ['Pending', 'Confirmed', 'Preparing', 'Ready', 'Delivered', 'Cancelled'],
      default: 'Pending',
    },
    paymentMode: {
      type: String,
      enum: ['Cash', 'Online', 'Card'],
      default: 'Cash',
      required: true,
    },
    paymentStatus: {
      type: String,
      enum: ['Pending', 'Completed', 'Failed'],
      default: 'Pending',
    },
    deliveryAddress: {
      type: String,
      required: true,
    },
    restaurantName: {
      type: String,
      default: '',
    },
    estimatedDeliveryTime: {
      type: Date,
      default: () => new Date(Date.now() + 30 * 60000), // 30 minutes from now
    },
    deliveredAt: {
      type: Date,
      default: null,
    },
    cancelledAt: {
      type: Date,
      default: null,
    },
    notes: {
      type: String,
      default: '',
    },
  },
  {
    timestamps: true, // Creates createdAt and updatedAt fields
  }
);

// Index for faster queries
orderSchema.index({ userId: 1, createdAt: -1 });

module.exports = mongoose.model('Order', orderSchema);
