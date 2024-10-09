import React, { useState, useEffect } from "react";

export const DinnerMenu = () => {

    const [dishes, setDishes] = useState([]);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetch(`${process.env.BACKEND_URL}/menu`)
            .then((response) => response.json())
            .then((data) => {
                console.log({data})
                const dinnerMenu = data.find(menu => menu.type === "Dinner");
                if (dinnerMenu) {
                    fetch(`${process.env.BACKEND_URL}/menu/${dinnerMenu.id}/dish`)
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