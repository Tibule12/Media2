import { createClient } from '@supabase/supabase-js'

const supabaseUrl = 'https://mszactexqxdjnyarbesw.supabase.co'
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1zemFjdGV4cXhkam55YXJiZXN3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDY2ODUxMTQsImV4cCI6MjA2MjI2MTExNH0.QwZ7Vb-04O8hfVZJs9y-gbujWR5qPFR2M2xSgCHjdDE'

const supabase = createClient(supabaseUrl, supabaseKey)

export default supabase
