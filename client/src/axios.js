import axios from 'axios';

const instance = axios.create({
  // baseURL: 'http://172.17.2.41',
  
  baseURL: 'https://4678-173-212-69-216.ngrok-free.app',

});

export default instance;
