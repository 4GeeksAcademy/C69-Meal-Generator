import React, { useState, useEffect } from "react";

export const DinnerMenu = () => {

    const [dishes, setDishes] = useState([]);
    const [error, setError] = useState(null);
    const [menus, setMenus] = useState([]);

    const fetchMenus = async () => {
        const menus = await fetch(`${process.env.BACKEND_URL}/menu`)
            .then((result) => result.json())
            .catch(err => {
                setError("error fetching menu")
                console.log(err)
                return []
            })
        return menus
    }
    const fetchMenuDishes = async (menuId) => {
        const dishes = await fetch(`${process.env.BACKEND_URL}/menu/${menuId}/dish`)
            .then(res => res.json())
            .then(resData => {
                if (resData.data) {
                    return resData.data
                } else {
                    return []
                }
            })
            .catch(err => {
                setError("error fetching dishes")
                console.log(err)
                return []
            })
            return dishes
    }

    const fetchAvailableMenu = async () => {
        const menus = await fetchMenus()
        const menu = menus.find(menu => menu.type === "Dinner")
        const dishes = await fetchMenuDishes(menu.id) 
        setDishes(dishes)
    }


    useEffect(() => {

        fetchAvailableMenu()

    }, [])

    return (
        <div>
            <h1>Dinner Menu</h1>
            {error && <p>{error}</p>}
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