import React, { useState, useEffect, useContext } from "react";
import { Context } from "../store/appContext";

export const Menu = (props) => {
    const {store, actions} = useContext(Context)
    const { menuType, dishes } = props;

    const handleFavorites = async(dishId) => {
        if (!store.token) {
            alert("please log in to save favorites");
            return 
        }
        await actions.toggleFavorite(dishId);
    }

    const isFavorite = (dishId) => {
        return store.favorites.some(fav => fav.dish_id === dishId)
    }

    return (
        <div>
            {(!menuType || !dishes.length) && (<div class="spinner-border" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>)}
            {(!!menuType && !!dishes.length) && (
                <>
                    <h1>{menuType} Menu</h1>
                    <ul>
                        {dishes.map(dish => (
                            <li key={dish.id}>
                                <button 
                                    className="btn btn-light"
                                    onClick={() => handleFavorites(dish.id)}
                                >
                                    <i className={`fa-${isFavorite(dish.id) ? 'solid' : 'regular'} fa-star`} />
                                </button>
                                <h2>{dish.name}</h2>
                                <div>
                                    {dish.ingredients.map(ingredient => ingredient.name).join(', ')}
                                </div>
                            </li>
                        ))}
                    </ul>
                </>
            )}
        </div>
    )
};
