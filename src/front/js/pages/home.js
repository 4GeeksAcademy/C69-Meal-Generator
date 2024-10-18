import React, { useContext, useState, useEffect } from "react";
import { Context } from "../store/appContext";
import "../../styles/home.css";
import { Menu, } from "../component/menu";


export const Home = () => {
	const { store, actions } = useContext(Context);
	const [menuType, setMenuType] = useState("Dinner");

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

	const fetchAvailableMenu = async (menuType) => {
		const menus = await fetchMenus()
		console.log({ menus })
		const menu = menus.find(menu => menu.type === menuType)
		const dishes = await fetchMenuDishes(menu.id)
		setDishes(dishes)
	}

	useEffect(() => {

		fetchAvailableMenu(menuType)

	}, [])

	const populateMenu = (menuType) => {
		setMenuType(menuType)
		fetchAvailableMenu(menuType)
	}

	return (
		<div className="overallWebsite text-center">
			<p class="toggle-menu-buttons d-inline-flex gap">
				<button 
					type="button"
					className={`btn btn-outline-light ${menuType === "Brunch" ? "active" : ""}`}
					data-bs-toggle="button"
					autocomplete="off"
					aria-pressed="true"
					onClick={() => populateMenu("Brunch")}
				>
						Brunch Menu
				</button>
				<button 
					type="button"
					className={`btn btn-outline-light ${menuType === "Dinner" ? "active" : ""}`}
					data-bs-toggle="button"
					autocomplete="off"
					aria-pressed="true"
					onClick={() => populateMenu("Dinner")}
				>
						Dinner Menu
				</button>
			</p>
			<div className="menu text-center">
				<h1 className="placeholder-for-menu">MENU</h1>
				{error && <p>{error}</p>}
				<Menu
					menuType={menuType}
					dishes={dishes}
				/>
			</div>

		</div>
	);
};
