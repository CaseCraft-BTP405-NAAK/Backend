import { api } from '@/lib/api';

export interface RecentOrder {
  id: string;
  customer: string;
  total: number;
  status: 'processing' | 'shipped' | 'completed' | 'cancelled';
  date: string;
}

export interface ProductStat {
  totalProducts: number;
  topSelling: Array<{
    name: string;
    sold: number;
  }>;
  lowStock: Array<{
    name: string;
    stock: number;
  }>;
}

export interface UserStat {
  totalUsers: number;
  newUsers: number;
  activeUsers: number;
}

export interface SalesData {
  total: number;
  change: number;
  direction: 'up' | 'down';
}

/**
 * Get recent orders for admin dashboard
 */
export const getRecentOrders = async (): Promise<RecentOrder[]> => {
  try {
    const response = await api.get('/admin/orders/recent');
    return response.data;
  } catch (error) {
    console.error('Error fetching recent orders:', error);
    // Return mock data for development
    return [
      { id: "ORD001", customer: "John Doe", total: 129.99, status: "completed", date: "2023-05-15" },
      { id: "ORD002", customer: "Jane Smith", total: 79.50, status: "processing", date: "2023-05-14" },
      { id: "ORD003", customer: "Robert Johnson", total: 199.99, status: "completed", date: "2023-05-13" },
      { id: "ORD004", customer: "Emily Davis", total: 149.95, status: "shipped", date: "2023-05-12" },
      { id: "ORD005", customer: "Michael Brown", total: 89.99, status: "processing", date: "2023-05-11" }
    ];
  }
};

/**
 * Get product statistics for admin dashboard
 */
export const getProductStats = async (): Promise<ProductStat> => {
  try {
    const response = await api.get('/admin/products/stats');
    return response.data;
  } catch (error) {
    console.error('Error fetching product stats:', error);
    // Return mock data for development
    return {
      totalProducts: 128,
      topSelling: [
        { name: "Premium Phone Case", sold: 245 },
        { name: "Screen Protector Ultra", sold: 189 },
        { name: "Wireless Charger", sold: 156 }
      ],
      lowStock: [
        { name: "Designer Phone Case", stock: 5 },
        { name: "Fast Charging Cable", stock: 8 },
        { name: "Bluetooth Earbuds", stock: 10 }
      ]
    };
  }
};

/**
 * Get user statistics for admin dashboard
 */
export const getUserStats = async (): Promise<UserStat> => {
  try {
    const response = await api.get('/admin/users/stats');
    return response.data;
  } catch (error) {
    console.error('Error fetching user stats:', error);
    // Return mock data for development
    return {
      totalUsers: 1247,
      newUsers: 28,
      activeUsers: 632
    };
  }
};

/**
 * Get sales data for admin dashboard
 */
export const getSalesData = async (): Promise<SalesData> => {
  try {
    const response = await api.get('/admin/sales/data');
    return response.data;
  } catch (error) {
    console.error('Error fetching sales data:', error);
    // Return mock data for development
    return {
      total: 12689.50,
      change: 10.1,
      direction: "up"
    };
  }
}; 