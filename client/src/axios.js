import axios from 'axios';

const instance = axios.create({
  baseURL: 'https://1f82-47-54-78-159.ngrok.io',

});

export default instance;
