import React, { useContext, useState } from "react";
import PropTypes from "prop-types";
import { Link, useNavigate } from "react-router-dom";
import { Context } from "../store/appContext";
import "../../styles/signup.css";


export const SignUp = () => {
	const { actions } = useContext(Context);
	const [email, setEmail] = useState('');
	const [firstName, setFirstName] = useState('');
	const [lastName, setLastName] = useState('');
	const [password, setPassword] = useState('');
	const [confirmPassword, setConfirmPassword] = useState('');
	const navigate = useNavigate()

	// instead of this, use useState:
	// let email = event.target.emailInput.value; 
	// let password = event.target.passwordInput.value;
	// let confirmPassword = event.target.confirmPasswordInput.value;

	const handleSubmit = async (event) => {
		event.preventDefault();

		// First validate inputs
		if (!email || !password || !confirmPassword) {
			alert('Please fill out all fields.');
			return;
		}

		if (password !== confirmPassword) {
			alert('Passwords do not match. Please try again.');
			return;
		}

		// Proceed with signUp after validation
		const response = await actions.signup(email, password, firstName, lastName);

		if (response) {
			alert('Account has been created');
			navigate('/login');
		} else {
			alert("We weren't able to sign you up at this time. Please try again later.");
		}
	};

	return (
		<div className="container d-flex flex-wrap mt-5 ">
			<h1 className="text-center">Create an Account</h1>
			<form onSubmit={handleSubmit} className="signInForm w-100 row g-4">
				<div className="col-md-8">
					<label for="inputEmail4" className="form-label">Email</label>
					<input
						value={email}
						onChange={(e) => setEmail(e.target.value)}
						name='emailInput'
						type="email"
						className="form-control"
						id="inputEmail4"
						required />
				</div>
				<div className="col-md-8">
					<label for="firstName" className="form-label">First Name</label>
					<input
						value={firstName}
						onChange={(e) => setFirstName(e.target.value)}
						name='firstName'
						type="text"
						className="form-control"
						id="firstName"
						required />
				</div>
				<div className="col-md-8">
					<label for="lastName" className="form-label">Last Name</label>
					<input
						value={lastName}
						onChange={(e) => setLastName(e.target.value)}
						name='lastName'
						type="text"
						className="form-control"
						id="lastName"
						required />
				</div>
				<div className="col-md-8">
					<label for="inputPassword4" className="form-label">Password</label>
					<input
						value={password}
						onChange={(e) => setPassword(e.target.value)}
						type="password"
						name='passwordInput'
						className="form-control"
						id="inputPassword4"
						required />
				</div>
				<div className="col-md-8">
					<label for="inputConfirmPassword4" className="form-label">Confirm Password</label>
					<input
						value={confirmPassword}
						onChange={(e) => setConfirmPassword(e.target.value)}
						type="password"
						name='confirmPasswordInput'
						className="form-control"
						id="confirmPassword4"
						required />
				</div>
				<p className="submit-btn d-flex">
					<button href="/"
						class="btn btn-outline-light"
						role="button"
					>Submit</button>
				</p>

			</form>
		</div>
	);
};

SignUp.propTypes = {
	match: PropTypes.object
}