import React, { useState, useEffect } from "react";

export const Menu = (props) => {

    const { menuType, dishes } = props;

    return (
        <div>
            <h1>{menuType} Menu</h1>
            <ul>
                {dishes.map(dish => (
                    <li key={dish.id}>
                        <h2>{dish.name}</h2>
                        <div>
                            {dish.ingredients.map(ingredient => ingredient.name).join(', ')}
                        </div>
                    </li>
                ))}
            </ul>
        </div>

    )
};