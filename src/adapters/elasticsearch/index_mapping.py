index_mapping = {
    'properties': {
        'source': {'type': 'keyword'},
        'sku': {'type': 'integer'},
        'title': {'type': 'text'},
        'price': {'type': 'scaled_float', 'scaling_factor': 100},
        'link': {'type': 'text'},
        'photo_link': {'type': 'keyword'},
        'characteristics': {'type': 'text'},
        'description': {'type': 'text'},
        'rating': {'type': 'scaled_float', 'scaling_factor': 100},
        'number_of_reviews': {'type': 'integer'},
        'updated_at': {'type': 'date'},
        'created_at': {'type': 'date'},
        'characteristics_vector': {'type': 'dense_vector', 'dims': 768, 'index': True, 'similarity': 'cosine'},
        'description_vector': {'type': 'dense_vector', 'dims': 768, 'index': True, 'similarity': 'cosine'},
    }
}
