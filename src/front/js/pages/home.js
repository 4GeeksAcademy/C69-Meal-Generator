import React, { useContext } from "react";
import { Context } from "../store/appContext";
import "../../styles/home.css";
import { DinnerMenu } from "../component/dinnermenu";


export const Home = () => {
	const { store, actions } = useContext(Context);

	return (
		<div className="overallWebsite text-center">
			<p className="toggle-menu-buttons d-inline-flex gap">
				<a href="#"
					className="brunch-menu-btn btn btn-outline-light"
					role="button"
					id="brunchButton"
					onClick="toggleFill()">Brunch Menu</a>
				<a href="#"
					className="dinner-menu-btn btn btn-outline-light"
					role="button"
					id="dinnerButton"
					onClick="toggleFill()">Dinner Menu</a>
			</p>
			<div className="menu text-center">
				<h1 className="placeholder-for-menu">MENU</h1>
				<DinnerMenu/>
			</div>

		</div>
	);
};
