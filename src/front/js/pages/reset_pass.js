import React, { useContext, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "../../styles/reset_pass.css";
import { Context } from "../store/appContext";

export const ResetPassword = () => {
    const { actions } = useContext(Context);
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');

    const navigate = useNavigate();

    const handleSubmit = async (event) => {
        event.preventDefault();

        if (!email || !password || !confirmPassword) {
            alert ('Please fill out all fields.');
            return;
        }

        if (password !== confirmPassword) {
            alert('Passwords do not match. Please try again.');
            return;
        }

        const response = await actions.resetPassword(email, password);

        if (response) {
            alert('Password has been reset');
            navigate('/login');
        } else {
            alert ("We were not able to reset your password at this time. Please try again later.");
        }
    };

    return (
        <div className="container d-flex flex-wrap mt-5 ">
			<h1 className="text-center py-3">Reset your Password</h1>
			<form onSubmit={handleSubmit} className="reset-password w-100 row g-4">
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
					<button href="/login"
						class="btn btn-outline-light"
						role="button"
						>Submit</button>
				</p>

			</form>
		</div>
	);
};
