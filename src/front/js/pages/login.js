import React, { useContext, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "../../styles/login.css";
import { Context } from "../store/appContext";

export const Login = () => {
	const { actions } = useContext(Context);
	const [email, setEmail] = useState(''); //default value of the variable goes in the quotes. In this case, an empty string.
	const [password, setPassword] = useState('');

	const navigate = useNavigate()

	const handleSubmit = async (event) => {
		event.preventDefault();

		if (!email || !password) {
			alert('Email or password cannot be empty');
			return;
		}

		const response = await actions.login(email, password);

		if (response) {
			alert('Welcome back');
			navigate('/');
		} else {
			alert("We weren't able to log you in at this time. Please try again later.");
		}
	}


	return (
		<div className="container mt-5">
			<form className="login-container d-flex row justify-content-center" onSubmit={handleSubmit}>
				<h1 className="login-header text-center">Log-In</h1>
				<div className="mb-3 col-7">
					<label for="exampleInputEmail1" className="form-label">Email address</label>
					<input
						onChange={(e) => setEmail(e.target.value)}
						value={email}
						type="email"
						name='emailInput'
						className="form-control"
						id="exampleInputEmail1"
						aria-describedby="emailHelp"
						required />
					<div id="emailHelp" className="form-text">We'll never share your email with anyone else.</div>
				</div>
				<div className="mb-3 col-7">
					<label for="exampleInputPassword1" className="form-label">Password</label>
					<input
						onChange={(e) => setPassword(e.target.value)}
						value={password}
						type="password"
						name='passwordInput'
						className="form-control"
						id="exampleInputPassword1" />
				</div>
				<div className="mb-3 form-check col-7">
					<input type="checkbox" className="form-check-input" id="exampleCheck1" />
					<label className="form-check-label" for="exampleCheck1">Remember Me</label>
					<a href="/forgot-password" className="forgotPassword">Forgot Password</a>
				</div>
				<div className="submit-btn d-flex">
					<button
						type="submit"
						className="btn btn-outline-light"
					>
						Submit
					</button>
				</div>

			</form>
		</div>
	);
};
