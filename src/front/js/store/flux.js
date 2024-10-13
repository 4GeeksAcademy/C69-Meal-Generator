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
						headers: { 'Content-Type': 'application/json' },
						body: JSON.stringify({
							email: email.toLowerCase(),
							password: password
						})
					})
					const data = await response.json();
					localStorage.setItem('jwt-token', data.token);

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
					throw error;
				}
			},

			userProfile: async () => {
				try {
					const token = localStorage.getItem('jwt-token');

					const resp = await fetch(process.env.BACKEND_URL + '/api/private', {
						method: 'GET',
						headers: {
							"Content-Type": 'application/json',
							'Authorization': 'Bearer' + token
						}
					});

					if (!resp.ok) {
						throw Error('There was a problem at login')
					} else if (resp.status === 403) {
						throw Error('Missing or invalid token');
					} else {
						throw Error('Unknown error');
					}
				} catch (error) {
					console.log('There was an error fining your account', error)
				}

				const data = await resp.json();
				console.log('This is the data you requested', data);
				return data
			},
			logout: () => {
				setStore({ token: null, user: null });
			},
		},
	};
}

export default getState