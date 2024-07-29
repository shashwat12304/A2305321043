import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import ProductDetails from '../components/ProductDetails';

const ProductPage = () => {
    const { id } = useParams();
    const [product, setProduct] = useState(null);

    useEffect(() => {
        axios.get(`http://20.244.56.144/test/product/${id}`)
            .then(response => {
                setProduct(response.data);
            })
            .catch(error => {
                console.error('There was an error fetching the product details!', error);
            });
    }, [id]);

    return (
        <div>
            {product ? <ProductDetails product={product} /> : <p>Loading...</p>}
        </div>
    );
};

export default ProductPage;
