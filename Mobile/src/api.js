import axios from 'axios'

const api = axios.create({
  baseURL: 'https://localhost:7003/api', // ← ezt módosítsd a saját backend URL-edre
})

export default api
