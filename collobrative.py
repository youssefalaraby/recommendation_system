import pandas as pd
import numpy as np
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

# Collaborative Filtering for Item-Based Recommendations
# This code provides a collaborative filtering approach to recommend companies to investors based on their interaction history.
# It uses cosine similarity to find similar items based on user interactions.
# The code includes functions to load interaction data, calculate item similarity, and generate recommendations for a given investor.
def calculate_item_similarity(ratings_matrix, metric='cosine'):
    if metric == 'cosine':
        item_similarity = cosine_similarity(ratings_matrix.T)
    else:
        raise ValueError("Unsupported similarity metric.")
    return item_similarity

# Function to recommend items for a given investor based on item similarity
def recommend_items(investor_id, ratings_matrix, item_similarity, k=9):
    investor_scores = ratings_matrix.loc[investor_id]
    interacted_companies = investor_scores[investor_scores > 0].index

    if investor_id not in ratings_matrix.index or len(interacted_companies) < 10:
        return cold_start_recommendations()
    
    recommendation_scores = {}
    for company_id in interacted_companies:
        similar_items = item_similarity[ratings_matrix.columns.get_loc(company_id)]
        weight = investor_scores[company_id]
        for other_idx, sim_score in enumerate(similar_items):
            other_company_id = ratings_matrix.columns[other_idx]
            if other_company_id not in interacted_companies:
                recommendation_scores[other_company_id] = recommendation_scores.get(other_company_id, 0) + sim_score * weight
    recommendations = pd.DataFrame({
        'company_id': list(recommendation_scores.keys()),
        'score': list(recommendation_scores.values())
    })
    recommendations = recommendations.sort_values(by='score', ascending=False)
    return recommendations[['company_id']].head(k)

# Function to load interaction data and calculate item similarity
def load_data_item_similarity(retrain=False):
    if retrain:
        df_interactions = pd.read_csv('interactions_table.csv')
        df_new = df_interactions.groupby(['investor_id', 'company_id']).agg({
            'view': 'sum',
            'save_for_later': 'sum',
            'comment': 'sum',
            'ratings': 'sum',
            'services': 'sum',
            'fund': 'sum',
            'timestamp': 'first'
        }).reset_index()
        df_new['interaction_score'] = (
            df_new['view']*0.1 + df_new['save_for_later']*0.3 + df_new['comment']*0.4 +
            df_new['ratings']*0.5 + df_new['services']*0.7 + df_new['fund']*0.9
        )
        data = df_new[['investor_id', 'company_id', 'interaction_score']]
        user_item_matrix = data.pivot(index='investor_id', columns='company_id', values='interaction_score').fillna(0)
        item_similarity = calculate_item_similarity(user_item_matrix)
        with open('sim_matrix_CF.pkl', 'wb') as f:
            pickle.dump(item_similarity, f)
        with open('user_item_matrix.pkl', 'wb') as f:
            pickle.dump(user_item_matrix, f)
        return user_item_matrix, item_similarity
    else:
        with open('user_item_matrix.pkl', 'rb') as f:
            user_item_matrix = pickle.load(f)
        with open('sim_matrix_CF.pkl', 'rb') as f:
            item_similarity = pickle.load(f)
        return user_item_matrix, item_similarity
    
def cold_start_recommendations():
     df_interactions = pd.read_csv('interactions_table.csv')
     df_new = df_interactions.groupby('company_id').agg({
            'fund': 'sum',
        }).reset_index()
     df_new.sort_values(by='fund', ascending=True, inplace=True)
     return df_new[['company_id']].head(9).values.flatten().tolist()

# Function to get recommendations for a specific investor
def get_recommendations_for_investor(investor_id, k=9):
    user_item_matrix, item_similarity = load_data_item_similarity(retrain=False)
    if investor_id not in user_item_matrix.index:
        return {'investor_id': investor_id, 'recommendations': cold_start_recommendations()}
    recommendations = recommend_items(investor_id, user_item_matrix, item_similarity, k)
    return {'investor_id': investor_id, 'recommendations': recommendations.values.flatten().tolist()}


print(get_recommendations_for_investor(100))  # Example call to test the function
# FastAPI application to serve recommendations
app = FastAPI()

@app.get("/recommendations/{investor_id}")
def get_recommendations(investor_id: int):
    try:
        recommendations = get_recommendations_for_investor(investor_id)
        return recommendations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))