import axios from 'axios';
import qs from 'qs';

const API = import.meta.env.VITE_REMOTE_API;

export default {
  login(user) {
    return axios.post(`${API}/login`, qs.stringify({
      username: user.username,
      password: user.password,
    }), {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      }
    });
  },

  register(user) {
    return axios.post(`${API}/register`, user);
  }
};