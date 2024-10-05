const getState = ({ getStore, getActions, setStore }) => {
	return {
		store: {
			token: null,
			user: null
		},
		actions: {
			signup: async (email, password) => {
				try {
					const response = await fetch(process.env.BACKEND_URL + '/api/sign-up', {
						method: 'POST',
						headers: { 'Content-Type': 'application/json' },
						body: JSON.stringify({
							email: email.toLowerCase(),
							password: password
						})
					})
					const data = await response.json();
					console.log(data);
					return data;
				} catch (error) {
					console.log('There was an error at sign-up.', error);
					throw error
				}
			},
			login: async (email, password) => {
				try {
					const response = await fetch(process.env.BACKEND_URL + '/api/log-in', {
						method: 'POST',
						headers: { 'Content-Type': 'application.json' },
						body: JSON.stringify({
							email: email.toLowerCase(),
							password: password
						})
					})
					const data = await response.json();

					if (response.status === 200) {
						localStorage.setItem('token', data.token);
						return true;
					} else if (response.status === 401) {
						alert(data.msg)
						return false;
					} else {
						console.log('Unexpected error occured at login.', response.status);
						return false;
					}
				} catch (error) {
					console.log('There was an error at log-in', error);
					throw error;
				};
			},

			logout: () => {
				setStore({ token: null, user: null });
			},
		},
	};
}

export default getState