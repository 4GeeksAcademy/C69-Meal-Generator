import React from "react";
import { Link } from "react-router-dom";
import "../../styles/navbar.css"
import towaLogo from "../../img/towa-logo.png"

export const Navbar = () => {
	return (
		<nav className="navbar navbar-light d-flex">
			<div className="logo px-3 col-8 d-flex">
				<Link to="/">
					<img className="towaLogo" src={towaLogo} />
				</Link>
			</div>
			<div className="login ml-3 col-3 px-5">
				<Link to="/login">Log-In</Link>
			</div>
			<div className="signup ml-3 col-1">
				<Link to="/signup">Sign up</Link>
			</div>
		</nav>
	);
};
