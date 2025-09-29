import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if SUPABASE_URL and SUPABASE_KEY and SUPABASE_URL != "sua_url_do_supabase_aqui":
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ Conexão com Supabase estabelecida com sucesso!")
    except Exception as e:
        supabase = None
        print(f"❌ Erro ao conectar com Supabase: {e}")
else:
    supabase = None
    print("⚠️  AVISO: Variáveis SUPABASE_URL e SUPABASE_KEY não configuradas")
    print("📝 Configure o arquivo .env com suas credenciais do Supabase:")
    print("   SUPABASE_URL=sua_url_do_supabase")
    print("   SUPABASE_KEY=sua_chave_do_supabase")
    print("   SECRET_KEY=sua_chave_secreta_flask")
    print("🚀 Aplicação rodando em modo de desenvolvimento (sem banco de dados)")
