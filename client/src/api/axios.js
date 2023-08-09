import axios from 'axios';

const instance = axios.create({
  // baseURL: 'http://172.17.2.41',
  
  baseURL: 'http://172.17.2.41:8000',
  headers: { "Content-Type": "application/json" }

});

export default instance;
