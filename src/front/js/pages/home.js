import React, { useContext, useState, useEffect } from "react";
import { Context } from "../store/appContext";
import "../../styles/home.css";
import { Menu, } from "../component/menu";


export const Home = () => {
	const { store, actions } = useContext(Context);
	const [menuType, setMenuType] = useState("");

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

	const stringTimeToNumber = (stringTime) => {
		return Number(stringTime.split(":").join(""))
	}

	const determineActiveMenu = (menus) => {
		const now = new Date();
		const currentDay = now.toLocaleDateString('en-US', { weekday: 'long'});
		const currentStringTime = now.toLocaleTimeString('en-US', { hour12: false});
		const currentTime = stringTimeToNumber(currentStringTime)

		console.log({currentDay, currentTime, menus})

		for (const menu of menus) {
			const availability = menu.availability.find(a => {
				const menuStartTime = stringTimeToNumber(a.start_time)
				const menuEndTime = stringTimeToNumber(a.end_time)

				return a.day.toLowerCase() === currentDay.toLocaleLowerCase() &&
				menuStartTime <= currentTime &&
				menuEndTime >= currentTime

			});
			
			if (availability) {
				return menu.type;
			}
		}
		return "Dinner"; 
	}

	const fetchAvailableMenu = async (menus ,menuType) => {
		const menu = menus.find(menu => menu.type === menuType)
		const dishes = await fetchMenuDishes(menu.id)
		setDishes(dishes)
	}

	const fetchCurrentlyAvailableMenu = async () => {
		const menus = await fetchMenus()
		const currentlyActiveMenuType = determineActiveMenu(menus)
		fetchAvailableMenu(menus ,currentlyActiveMenuType)
		setMenus(menus)
		setMenuType(currentlyActiveMenuType)
	}

	useEffect(() => {
		fetchCurrentlyAvailableMenu()

	}, [])

	const populateMenu = (menus,menuType) => {
		setMenuType(menuType)
		fetchAvailableMenu(menus, menuType)
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
					onClick={() => populateMenu(menus, "Brunch")}
				>
						Brunch Menu
				</button>
				<button 
					type="button"
					className={`btn btn-outline-light ${menuType === "Dinner" ? "active" : ""}`}
					data-bs-toggle="button"
					autocomplete="off"
					aria-pressed="true"
					onClick={() => populateMenu(menus, "Dinner")}
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
