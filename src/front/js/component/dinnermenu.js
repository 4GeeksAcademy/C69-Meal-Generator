import React, { Component } from "react";
import { useEffect, useState } from "react/cjs/react.production.min";

export const DinnerMenu = () => {

    const [dishes, setDishes] = useState([]);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetch("/menu")
            .then((response) => response.json())
            .then((data) => {
                const dinnerMenu = data.find(menu => menu.type === "Dinner");
                if (dinnerMenu) {
                    fetch(`/menu/${dinnerMenu.id}/dish`)
                        .then(res => res.json())
                        .then(resData => {
                            if (resData.data) {
                                setDishes(resData.data)
                            } else {
                                setError("Dishes not found")
                            }
                        })
                        .catch(err => setError("error fetching dishes"))
                } else {
                    setError("dinner menu not found")
                }
            })
            .catch(err => setError("error fetching menu"))
    }, [])

    return (
        <div>
            <h1>Dinner Menu</h1>
            {error && <p>{error}</p>}
            <ul>
                {dishes.map(dish => (
                    <li key={dish.id}>
                        <h2>{dish.name}</h2>
                        <p>{dish.ingredients}</p>
                    </li>
                ))}
            </ul>
        </div>

    )
};