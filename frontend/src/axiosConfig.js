import axios from 'axios';

axios.defaults.baseURL = 'http://localhost:8000';

const token = localStorage.getItem('authToken');
if (token) {
  axios.defaults.headers.common['Authorization'] = `Token ${token}`;
}

export default axios;
