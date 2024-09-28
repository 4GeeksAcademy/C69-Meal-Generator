import React, { useContext } from "react";
import { Context } from "../store/appContext";
import "../../styles/home.css";

export const Home = () => {
	const { store, actions } = useContext(Context);

	return (
		<div className="overallWebsite text-center">
			<p class="toggle-menu-buttons d-inline-flex gap">
				<a href="#"
					class="brunch-menu-btn btn btn-outline-light"
					role="button"
					id="brunchButton"
					onclick="toggleFill()">Brunch Menu</a>
				<a href="#"
					class="dinner-menu-btn btn btn-outline-light"
					role="button"
					id="dinnerButton"
					onclick="toggleFill()">Dinner Menu</a>
			</p>
			<div className="menu text-center">
				<h1 className="placeholder-for-menu">MENU</h1>
			</div>

		</div>
	);
};
