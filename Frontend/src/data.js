// data.js – teljes mock adatbázis frontendhez

// Felhasználók
export const users = [
  {
    id: 1,
    username: 'Admin',
    email: 'admin@example.com',
    password: '1234',
    role: 'admin',
    card_id: 1000,
    created_at: "2025. 11. 10. 09:00:00"
  },
  {
    id: 2,
    username: 'Csoportvezető',
    email: 'leader@example.com',
    password: '1234',
    role: 'leader',
    card_id: 2000,
    created_at: "2025. 11. 10. 09:05:00"
  },
  {
    id: 3,
    username: 'Dolgozó',
    email: 'worker@example.com',
    password: '1234',
    role: 'worker',
    card_id: 3000,
    created_at: "2025. 11. 10. 09:10:00"
  }
]

// Belépési / kilépési logok
export const logins = [
  {
    id: 1,
    card_id: 1000,
    time: "2025. 11. 10. 08:00:00",
    log_IN: true
  },
  {
    id: 2,
    card_id: 2000,
    time: "2025. 11. 10. 08:15:00",
    log_IN: true
  },
  {
    id: 3,
    card_id: 3000,
    time: "2025. 11. 10. 08:30:00",
    log_IN: true
  },
  {
    id: 4,
    card_id: 1000,
    time: "2025. 11. 10. 16:30:00",
    log_IN: false
  }
]

// Csoportok
export const groups = [
  {
    id: 1,
    name: "Fejlesztők",
    leader_id: 2,
    members: [2, 3]  // user id-k
  },
  {
    id: 2,
    name: "Adminok",
    leader_id: 1,
    members: [1]
  }
]
