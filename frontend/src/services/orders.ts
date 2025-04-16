import { api } from '@/lib/api';
import { Order, CartItem } from '@/types';

// Local storage key for orders
const ORDERS_STORAGE_KEY = 'user_orders';

/**
 * Save an order to local storage
 */
export const saveOrder = (items: CartItem[], total: number): Order => {
  // Get existing orders
  const existingOrdersStr = localStorage.getItem(ORDERS_STORAGE_KEY);
  const existingOrders: Order[] = existingOrdersStr ? JSON.parse(existingOrdersStr) : [];
  
  // Create a new order
  const newOrder: Order = {
    id: `ORD-${Date.now().toString().slice(-6)}`,
    userId: getUserId(),
    items: items,
    total: total,
    status: 'processing',
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
  };
  
  // Add the new order to existing orders
  const updatedOrders = [newOrder, ...existingOrders];
  
  // Save to local storage
  localStorage.setItem(ORDERS_STORAGE_KEY, JSON.stringify(updatedOrders));
  
  return newOrder;
};

/**
 * Get all orders for the current user
 */
export const getUserOrders = (): Order[] => {
  const userId = getUserId();
  const ordersStr = localStorage.getItem(ORDERS_STORAGE_KEY);
  
  if (!ordersStr) return [];
  
  const allOrders: Order[] = JSON.parse(ordersStr);
  return allOrders.filter(order => order.userId === userId);
};

/**
 * Get a single order by ID
 */
export const getOrderById = (orderId: string): Order | null => {
  const orders = getUserOrders();
  return orders.find(order => order.id === orderId) || null;
};

/**
 * Update order status (e.g., from 'processing' to 'shipped')
 */
export const updateOrderStatus = (orderId: string, status: Order['status']): Order | null => {
  const ordersStr = localStorage.getItem(ORDERS_STORAGE_KEY);
  
  if (!ordersStr) return null;
  
  const allOrders: Order[] = JSON.parse(ordersStr);
  const orderIndex = allOrders.findIndex(order => order.id === orderId);
  
  if (orderIndex === -1) return null;
  
  // Update status and updatedAt timestamp
  allOrders[orderIndex].status = status;
  allOrders[orderIndex].updatedAt = new Date().toISOString();
  
  // Save back to storage
  localStorage.setItem(ORDERS_STORAGE_KEY, JSON.stringify(allOrders));
  
  return allOrders[orderIndex];
};

/**
 * Helper to get current user ID
 */
function getUserId(): string {
  const userStr = localStorage.getItem('user');
  if (!userStr) return 'guest-user';
  
  try {
    const user = JSON.parse(userStr);
    return user.id || user.username || 'unknown-user';
  } catch (error) {
    console.error('Error parsing user data:', error);
    return 'unknown-user';
  }
} 