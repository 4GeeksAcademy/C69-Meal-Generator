import React, {useContext} from "react";
import { Context } from "../store/appContext";
import { Link, useNavigate } from "react-router-dom";
import "../../styles/navbar.css"
import towaLogo from "../../img/towa-logo.png"

export const Navbar = () => {
	const {store, actions} = useContext(Context);
	const isLoggedIn = !!localStorage.getItem("token");
	const navigate= useNavigate();

	const handleLogout= () => {
		actions.logout();
		navigate("/");
		window.location.reload()
	}
	return (
		<nav className="navbar navbar-light d-flex">
			<div className="logo px-3 col-8 d-flex">
				<Link to="/">
					<img className="towaLogo" src={towaLogo} />
				</Link>
			</div>
			{isLoggedIn ? (

				<div className="dropdown signup ms-auto me-3">
						<button className="btn btn-outline-light dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
							<i className="fa-regular fa-user"></i>
						</button>
						<ul className="dropdown-menu dropdown-menu-dark dropdown-menu-end">
							<li><Link className="dropdown-item" to="/profile">Profile</Link></li>
							<li><button className="dropdown-item" onClick={handleLogout}>Sign-Out</button></li>
						</ul>

				</div>

			) : (
				<>
					<div className="login ml-3 col-3 px-5">
						<Link to="/login">Log-In</Link>
					</div>
					<div className="signup ml-3 col-1">
						<Link to="/signup">Sign up</Link>
					</div>
				</>
			)}



		</nav>
	);
};
