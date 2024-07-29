import axios from 'axios';

const API_BASE_URL = 'http://20.244.56.144/test';

export const fetchProducts = async () => {
    const response = await axios.get(`${API_BASE_URL}/products`);
    return response.data;
};

export const fetchProductDetails = async (id) => {
    const response = await axios.get(`${API_BASE_URL}/product/${id}`);
    return response.data;
};
