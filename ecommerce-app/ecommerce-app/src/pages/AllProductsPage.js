import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ProductList from '../components/ProductList';

const AllProductsPage = () => {
    const [products, setProducts] = useState([]);

    useEffect(() => {
        axios.get('http://20.244.56.144/test/products')
            .then(response => {
                const productsWithId = response.data.map(product => ({
                    ...product,
                    id: `${product.company}-${product.category}-${product.name}`.replace(/\s+/g, '-').toLowerCase(),
                }));
                setProducts(productsWithId);
            })
            .catch(error => {
                console.error('There was an error fetching the products!', error);
            });
    }, []);

    return (
        <div>
            <h1>All Products</h1>
            <ProductList products={products} />
        </div>
    );
};

export default AllProductsPage;
