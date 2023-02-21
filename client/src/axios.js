import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://172.17.2.41',

});

export default instance;
