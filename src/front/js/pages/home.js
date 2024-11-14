import React, { useContext, useState, useEffect } from "react";
import { Context } from "../store/appContext";
import "../../styles/home.css";
import { Menu } from "../component/menu";

export const Home = () => {
	const { store, actions } = useContext(Context);
	const [menuType, setMenuType] = useState("");
	const [dishes, setDishes] = useState([]);
	const [error, setError] = useState(null);
	const [menus, setMenus] = useState([]);
	const [isLoading, setIsLoading] = useState(true);

	const fetchMenus = async () => {
		try {
			const menus = await fetch(`${process.env.BACKEND_URL}/menu`)
				.then((result) => result.json());
			return menus;
		} catch (err) {
			setError("error fetching menu");
			console.log(err);
			return [];
		} finally {
			setIsLoading(false);
		}
	};

	const filterDishesByUserPreferences = (dishes) => {
		if (!store.userPreferences || !Array.isArray(dishes)) {
			console.log("No preferences or dishes:", { 
				userPreferences: store.userPreferences, 
				dishes: dishes 
			});
			return dishes;
		}
	
		console.log("User Preferences:", store.userPreferences);
		
		return dishes.filter(dish => {
			console.log("Checking dish preferences:", {
				name: dish.name,
				preferences: dish.preference
			});
	
			if (!dish.preference) {
				console.log("No preferences for dish:", dish.name);
				return true;
			}
	
			const userPreferences = {};
			Object.entries(store.userPreferences).forEach(([key, value]) => {
				const snakeKey = key.toLowerCase().replace(/ /g, '_');
				userPreferences[snakeKey] = value;
			});
	
			console.log("Converted user preferences:", userPreferences);
	
			for (const [preference, isPreferred] of Object.entries(userPreferences)) {
				console.log(`Checking ${preference}:`, {
					userHasPreference: isPreferred,
					dishHasPreference: dish.preference[preference]
				});
				
				if (isPreferred && dish.preference[preference]) {
					console.log(`Filtering out ${dish.name} due to ${preference}`);
					return false;
				}
			}
			console.log(`Keeping dish: ${dish.name}`);
			return true;
		});
	};

	const filterDishesByUserRestrictions = (dishes) => {
		if (!store.userRestrictions || !Array.isArray(dishes)) {
			console.log("No restrictions or dishes:", { 
				userRestrictions: store.userRestrictions, 
				dishes: dishes 
			});
			return dishes;
		}
	
		console.log("User Restrictions:", store.userRestrictions);
		
		return dishes.filter(dish => {
			console.log("Checking dish:", {
				name: dish.name,
				restrictions: dish.restriction
			});
	
			if (!dish.restriction) {
				console.log("No restrictions for dish:", dish.name);
				return true;
			}
	
			const userRestrictions = {};
			Object.entries(store.userRestrictions).forEach(([key, value]) => {
				const snakeKey = key.toLowerCase().replace(/ /g, '_');
				userRestrictions[snakeKey] = value;
			});
	
			console.log("Converted user restrictions:", userRestrictions);
	
			for (const [restriction, isRestricted] of Object.entries(userRestrictions)) {
				if (isRestricted && dish.restriction[restriction]) {
					console.log(`Filtering out ${dish.name} due to ${restriction}`);
					return false;
				}
			}
			console.log(`Keeping dish: ${dish.name}`);
			return true;
		});
	};

	const fetchMenuDishes = async (menuId) => {
		try {
			const response = await fetch(`${process.env.BACKEND_URL}/menu/${menuId}/dish`);
			const resData = await response.json();
			
			if (resData.data) {
				// Apply both filters in sequence
				const restrictionFilteredDishes = filterDishesByUserRestrictions(resData.data);
				const finalFilteredDishes = filterDishesByUserPreferences(restrictionFilteredDishes);
				return finalFilteredDishes;
			}
			return [];
		} catch (err) {
			setError("error fetching dishes");
			console.log(err);
			return [];
		} finally {
			setIsLoading(false);
		}
	};

	const stringTimeToNumber = (stringTime) => {
		return Number(stringTime.split(":").join(""));
	};

	const determineActiveMenu = (menus) => {
		const now = new Date();
		const currentDay = now.toLocaleDateString('en-US', { weekday: 'long' });
		const currentStringTime = now.toLocaleTimeString('en-US', { hour12: false });
		const currentTime = stringTimeToNumber(currentStringTime);

		for (const menu of menus) {
			const availability = menu.availability.find(a => {
				const menuStartTime = stringTimeToNumber(a.start_time);
				const menuEndTime = stringTimeToNumber(a.end_time);

				return a.day.toLowerCase() === currentDay.toLowerCase() &&
					menuStartTime <= currentTime &&
					menuEndTime >= currentTime;
			});

			if (availability) {
				return menu.type;
			}
		}
		return "Dinner";
	};

	const fetchAvailableMenu = async (menus, menuType) => {
		setIsLoading(true);
		const menu = menus.find(menu => menu.type === menuType);
		if (menu) {
			const dishes = await fetchMenuDishes(menu.id);
			setDishes(dishes);
		}
	};

	const fetchCurrentlyAvailableMenu = async () => {
		const menus = await fetchMenus();
		const currentlyActiveMenuType = determineActiveMenu(menus);
		await fetchAvailableMenu(menus, currentlyActiveMenuType);
		setMenus(menus);
		setMenuType(currentlyActiveMenuType);
	};

	useEffect(() => {
		fetchCurrentlyAvailableMenu();
	}, []);

	useEffect(() => {
		if (menus.length > 0 && menuType) {
			fetchAvailableMenu(menus, menuType);
		}
	}, [store.userRestrictions, store.userPreferences]); // Added userPreferences dependency

	const populateMenu = (menus, menuType) => {
		setMenuType(menuType);
		fetchAvailableMenu(menus, menuType);
	};

	return (
		<div className="overallWebsite text-center">
			<p className="toggle-menu-buttons d-inline-flex gap">
				<button
					type="button"
					className={`btn btn-outline-light ${menuType === "Brunch" ? "active" : ""}`}
					data-bs-toggle="button"
					autoComplete="off"
					aria-pressed="true"
					onClick={() => populateMenu(menus, "Brunch")}
				>
					Brunch Menu
				</button>
				<button
					type="button"
					className={`btn btn-outline-light ${menuType === "Dinner" ? "active" : ""}`}
					data-bs-toggle="button"
					autoComplete="off"
					aria-pressed="true"
					onClick={() => populateMenu(menus, "Dinner")}
				>
					Dinner Menu
				</button>
			</p>
			<div className="menu text-center">
				<h1 className="placeholder-for-menu">MENU</h1>
				{error && <p className="text-danger">{error}</p>}
				{isLoading ? (
					<div className="spinner-border text-light" role="status">
						<span className="visually-hidden">Loading...</span>
					</div>
				) : dishes.length === 0 ? (
					<div className="alert alert-info mx-5" role="alert">
						There are no dishes left that meet your preferences & restrictions. 
						Please ask your server for help in picking the right menu items.
					</div>
				) : (
					<Menu
						menuType={menuType}
						dishes={dishes}
					/>
				)}
			</div>
		</div>
	);
};