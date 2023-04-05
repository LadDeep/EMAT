import axios from 'axios';

const instance = axios.create({
  // baseURL: 'http://172.17.2.41',
  
  baseURL: 'https://f7f6-142-68-131-32.ngrok.io',

});

export default instance;
