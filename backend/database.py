import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables from .env file
load_dotenv()

# Real Supabase Configuration
SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://your-supabase-url.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "your-supabase-anon-key")

def get_supabase_client() -> Client:
    """
    Initializes and returns the real Supabase client for database operations.
    Falls back to a MockClient if configuration is invalid.
    """
    try:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print(f"Supabase Connection Failed: {e}. Falling back to MockClient.")
        class MockClient:
            def table(self, name):
                class MockTable:
                    def select(self, *args, **kwargs): return self
                    def insert(self, *args, **kwargs): return self
                    def update(self, *args, **kwargs): return self
                    def eq(self, *args, **kwargs): return self
                    def order(self, *args, **kwargs): return self
                    def limit(self, *args, **kwargs): return self
                    def single(self, *args, **kwargs): return self
                    def execute(self): 
                        # Return empty but valid data structure
                        return type('obj', (object,), {'data': [], 'error': None})()
                return MockTable()
        return MockClient()

db = get_supabase_client()
