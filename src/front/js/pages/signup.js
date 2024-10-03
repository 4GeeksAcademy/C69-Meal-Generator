import React, { useContext } from "react";
import PropTypes from "prop-types";
import { Link, useNavigate } from "react-router-dom";
import { Context } from "../store/appContext";
import "../../styles/signup.css";


export const SignUp = () => {
	const { actions } = useContext(Context);
	const navigate = useNavigate()

	const handleSubmit = async (event) => {
		event.preventDefault();

		let email = event.target.emailInput.value;
		let password = event.target.passwordInput.value;
		let confirmPassword = event.target.confirmPasswordInput.value;

		if (password !== confirmPassword) {
			alert('Password does not match. Please try again.');
			return;
		}

		const response = await actions.signUp(email, password);
		if (response) {
			alert('Account has been created');
			navigate('/login')
		} else {
			alert(" We weren't able to sign you up at this time. Please try again later.");
		}
	}

	return (
		<div className="container d-flex flex-wrap mt-5 ">
			<h1 className="text-center">Create an Account</h1>
			<form onSubmit={handleSubmit} className="signInForm w-100 row g-4">
				<div className="col-md-8">
					<label for="inputEmail4" className="form-label">Email</label>
					<input name='emailInput' type="email" className="form-control" id="inputEmail4" required />
				</div>
				<div className="col-md-8">
					<label for="inputPassword4" className="form-label">Password</label>
					<input type="password" name='passwordInput' className="form-control" id="inputPassword4" required />
				</div>
				<div className="col-md-8">
					<label for="inputConfirmPassword4" className="form-label">Confirm Password</label>
					<input type="password" name='confirmPasswordInput' className="form-control" id="confirmPassword4" required />
				</div>
				<p className="submit-btn d-flex">
					<a href="/"
						class="btn btn-outline-light"
						role="button"
						id="brunchButton"
						onclick="toggleFill()">Submit</a>
				</p>

			</form>
		</div>
	);
};

SignUp.propTypes = {
	match: PropTypes.object
}