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
    
    // --- 2025. NOV. 21. (Péntek) ---
    // Admin (1000) - 7.5 óra
    { id: 1, card_id: 1000, time: "2025. 11. 21. 09:30:00", log_IN: true }, 
    { id: 2, card_id: 1000, time: "2025. 11. 21. 17:00:00", log_IN: false }, 
    // Leader (2000) - 8 óra
    { id: 3, card_id: 2000, time: "2025. 11. 21. 08:00:00", log_IN: true },
    { id: 4, card_id: 2000, time: "2025. 11. 21. 16:00:00", log_IN: false },
    // Worker (3000) - 8 óra 15 perc
    { id: 5, card_id: 3000, time: "2025. 11. 21. 08:30:00", log_IN: true }, 
    { id: 6, card_id: 3000, time: "2025. 11. 21. 16:45:00", log_IN: false }, 


    // --- 2025. NOV. 20. (Csütörtök) ---
    // Admin (1000) - 9 óra
    { id: 7, card_id: 1000, time: "2025. 11. 20. 08:00:00", log_IN: true }, 
    { id: 8, card_id: 1000, time: "2025. 11. 20. 17:00:00", log_IN: false }, 
    // Leader (2000) - 7 óra
    { id: 9, card_id: 2000, time: "2025. 11. 20. 09:00:00", log_IN: true },
    { id: 10, card_id: 2000, time: "2025. 11. 20. 16:00:00", log_IN: false },
    // Worker (3000) - 8 óra
    { id: 11, card_id: 3000, time: "2025. 11. 20. 07:30:00", log_IN: true }, 
    { id: 12, card_id: 3000, time: "2025. 11. 20. 15:30:00", log_IN: false }, 


    // --- 2025. NOV. 19. (Szerda) ---
    // Admin (1000) - 8 óra
    { id: 13, card_id: 1000, time: "2025. 11. 19. 08:45:00", log_IN: true }, 
    { id: 14, card_id: 1000, time: "2025. 11. 19. 16:45:00", log_IN: false }, 
    // Leader (2000) - 8.5 óra
    { id: 15, card_id: 2000, time: "2025. 11. 19. 07:45:00", log_IN: true },
    { id: 16, card_id: 2000, time: "2025. 11. 19. 16:15:00", log_IN: false },
    // Worker (3000) - 7 óra
    { id: 17, card_id: 3000, time: "2025. 11. 19. 09:15:00", log_IN: true }, 
    { id: 18, card_id: 3000, time: "2025. 11. 19. 16:15:00", log_IN: false }, 


    // --- 2025. NOV. 18. (Kedd) ---
    // Admin (1000) - 8 óra
    { id: 19, card_id: 1000, time: "2025. 11. 18. 08:30:00", log_IN: true }, 
    { id: 20, card_id: 1000, time: "2025. 11. 18. 16:30:00", log_IN: false }, 
    // Leader (2000) - 9 óra
    { id: 21, card_id: 2000, time: "2025. 11. 18. 07:00:00", log_IN: true },
    { id: 22, card_id: 2000, time: "2025. 11. 18. 16:00:00", log_IN: false },
    // Worker (3000) - 8.5 óra
    { id: 23, card_id: 3000, time: "2025. 11. 18. 08:00:00", log_IN: true }, 
    { id: 24, card_id: 3000, time: "2025. 11. 18. 16:30:00", log_IN: false }, 
    
    
    // --- 2025. NOV. 17. (Hétfő) ---
    // Admin (1000) - 7 óra
    { id: 25, card_id: 1000, time: "2025. 11. 17. 09:00:00", log_IN: true }, 
    { id: 26, card_id: 1000, time: "2025. 11. 17. 16:00:00", log_IN: false }, 
    // Leader (2000) - 8 óra
    { id: 27, card_id: 2000, time: "2025. 11. 17. 08:30:00", log_IN: true },
    { id: 28, card_id: 2000, time: "2025. 11. 17. 16:30:00", log_IN: false },
    // Worker (3000) - 8 óra
    { id: 29, card_id: 3000, time: "2025. 11. 17. 09:00:00", log_IN: true }, 
    { id: 30, card_id: 3000, time: "2025. 11. 17. 17:00:00", log_IN: false }, 

    // data.js frissítése a decemberi adatokkal
    
    // --- 2025. DEC. 19. (Péntek - MA) ---
    { id: 1, card_id: 1000, time: "2025. 12. 19. 08:00:00", log_IN: true }, 
    { id: 2, card_id: 1000, time: "2025. 12. 19. 15:30:00", log_IN: false }, 
    { id: 3, card_id: 2000, time: "2025. 12. 19. 08:30:00", log_IN: true },
    { id: 4, card_id: 2000, time: "2025. 12. 19. 16:30:00", log_IN: false },
    { id: 5, card_id: 3000, time: "2025. 12. 19. 09:00:00", log_IN: true }, 
    { id: 6, card_id: 3000, time: "2025. 12. 19. 17:15:00", log_IN: false }, 

    // --- 2025. DEC. 18. (Csütörtök) ---
    { id: 7, card_id: 1000, time: "2025. 12. 18. 08:15:00", log_IN: true }, 
    { id: 8, card_id: 1000, time: "2025. 12. 18. 17:15:00", log_IN: false }, 
    { id: 9, card_id: 2000, time: "2025. 12. 18. 07:45:00", log_IN: true },
    { id: 10, card_id: 2000, time: "2025. 12. 18. 16:00:00", log_IN: false },
    { id: 11, card_id: 3000, time: "2025. 12. 18. 08:00:00", log_IN: true }, 
    { id: 12, card_id: 3000, time: "2025. 12. 18. 16:30:00", log_IN: false }, 

    // --- 2025. DEC. 17. (Szerda) ---
    { id: 13, card_id: 1000, time: "2025. 12. 17. 08:45:00", log_IN: true }, 
    { id: 14, card_id: 1000, time: "2025. 12. 17. 16:45:00", log_IN: false }, 
    { id: 15, card_id: 2000, time: "2025. 12. 17. 07:30:00", log_IN: true },
    { id: 16, card_id: 2000, time: "2025. 12. 17. 17:00:00", log_IN: false },
    { id: 17, card_id: 3000, time: "2025. 12. 17. 09:30:00", log_IN: true }, 
    { id: 18, card_id: 3000, time: "2025. 12. 17. 17:30:00", log_IN: false }, 

    // --- 2025. DEC. 16. (Kedd) ---
    { id: 19, card_id: 1000, time: "2025. 12. 16. 08:00:00", log_IN: true }, 
    { id: 20, card_id: 1000, time: "2025. 12. 16. 17:00:00", log_IN: false }, 
    { id: 21, card_id: 2000, time: "2025. 12. 16. 08:30:00", log_IN: true },
    { id: 22, card_id: 2000, time: "2025. 12. 16. 16:30:00", log_IN: false },
    { id: 23, card_id: 3000, time: "2025. 12. 16. 07:15:00", log_IN: true }, 
    { id: 24, card_id: 3000, time: "2025. 12. 16. 16:45:00", log_IN: false }, 

    // --- 2025. DEC. 15. (Hétfő) ---
    { id: 25, card_id: 1000, time: "2025. 12. 15. 09:00:00", log_IN: true }, 
    { id: 26, card_id: 1000, time: "2025. 12. 15. 16:00:00", log_IN: false }, 
    { id: 27, card_id: 2000, time: "2025. 12. 15. 08:00:00", log_IN: true },
    { id: 28, card_id: 2000, time: "2025. 12. 15. 17:00:00", log_IN: false },
    { id: 29, card_id: 3000, time: "2025. 12. 15. 08:30:00", log_IN: true }, 
    { id: 30, card_id: 3000, time: "2025. 12. 15. 16:30:00", log_IN: false }, 

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
