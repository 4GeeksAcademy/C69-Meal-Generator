import React from "react";
import { Link } from "react-router-dom";
import "../../styles/navbar.css"

export const Navbar = () => {
	return (
		<nav className="navbar navbar-light bg-light d-flex">
				<div className="logo px-5 col-8">
					<Link to="/">
						<p className="navbar-brand mb-0 h1">TOWA</p>
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
