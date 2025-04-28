"""
Script to create an ngrok tunnel to the backend server.
"""
from pyngrok import ngrok, conf
import time

# Configure ngrok
conf.get_default().auth_token = ""  # Add your auth token here if you have one

def create_tunnel():
    try:
        # Create an HTTP tunnel on port 8000
        http_tunnel = ngrok.connect(8000, "http")
        public_url = http_tunnel.public_url
        
        print(f"\n✅ Ngrok tunnel established!")
        print(f"✅ Public URL: {public_url}")
        print(f"✅ Forwarding to: http://localhost:8000")
        print("\nPress Ctrl+C to stop the tunnel...")
        
        # Keep the tunnel open
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nShutting down ngrok tunnel...")
    finally:
        ngrok.kill()
        print("Tunnel stopped.")

if __name__ == "__main__":
    create_tunnel()
