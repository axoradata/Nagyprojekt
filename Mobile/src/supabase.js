import { createClient } from '@supabase/supabase-js'

// ⚠️ FONTOS: Vite alatt az env változókat így éred el:
const supabaseUrl = 'https://fenodzovtuspdqtbensq.supabase.co'
const supabaseKey = import.meta.env.VITE_SUPABASE_KEY

const supabase = createClient(supabaseUrl, supabaseKey)

export default supabase
