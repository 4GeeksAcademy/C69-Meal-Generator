import React, { useContext, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "../../styles/forgot_pass.css";
import { Context } from "../store/appContext";

export const ForgotPassword = () => {
    const { actions } = useContext(Context);
    const [email, setEmail] = useState('');

    const navigate = useNavigate()

    const handleSubmit = async (event) => {
        event.preventDefault();

        if (!email) {
            alert('Email cannot be empty');
            return;
        }

        const response = await actions.ForgotPassword(email);

        if (response) {
            navigate('/');
            alert("Please check your email for your reset password link.")
        } else {
            alert("We were not able to send you a reset email at this time. Please try again later.")
        }

    }
    return (
        <form className="forgot-pass-container d-flex row justify-content-center p-5" onSubmit={handleSubmit}>
            <h1 className="forgot-pass-header text-center">Forgot Password</h1>
            <div className="mb-3 col-7 py-5">
                <label for="exampleInputEmail1" className="form-label">Email Address</label>
                <input
                    onChange={(e) => setEmail(e.target.value)}
                    value={email}
                    type="email"
                    name='emailInput'
                    className="form-control"
                    id="exampleInputEmail1"
                    aria-describedby="emailHelp"
                    required />
                <div className="submit-btn py-4 d-flex">
					<button
						type="submit"
						className="btn btn-outline-light"
					>
						Submit
					</button>
				</div>
            </div>
        </form>
    )
}

