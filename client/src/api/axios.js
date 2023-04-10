import axios from 'axios';

const instance = axios.create({
  // baseURL: 'http://172.17.2.41',
  
  baseURL: 'https://a107-173-212-69-216.ngrok-free.app',
  headers: { "Content-Type": "application/json" }

});

export default instance;
