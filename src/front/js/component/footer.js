import React, { Component } from "react";
import "../../styles/footer.css"

export const Footer = () => (
	<footer className="footer py-3 text-center">
		<p style={{color:'whitesmoke'}}>
			Made for{" "}
			<a href="http://www.towanyc.com">TOWANYC</a>
		</p>
		<p className="towa-info pt-3" style={{color:'whitesmoke'}}>
			Dinner
			<br></br>
			Sun - Thu | 5:30 pm - 9:30 pm
			<br></br>
			Fri & Sat | 5:15 pm - 10:00 pm
			<br></br>
			<br></br>
			Brunch
			<br></br>
			Sat & Sun | 12:00 pm - 2:30 pm
			<br></br>
			______________________
			<br></br>
			<br></br>
			36 W 26th St. New York, NY 10010
			<br></br>
			(646) 351-6258
			
		</p>
	</footer>
);
