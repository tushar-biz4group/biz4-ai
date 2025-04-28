"""
Script to run the FastAPI backend with ngrok tunnel.
"""
import os
import subprocess
import time
from pyngrok import ngrok, conf

# Set ngrok config
conf.get_default().region = "us"

def run_backend_with_ngrok():
    # Start the backend server in a separate process
    backend_process = subprocess.Popen(
        ["python", "main.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    
    # Wait for the server to start
    time.sleep(5)
    
    try:
        # Start ngrok tunnel
        http_tunnel = ngrok.connect(8000)
        public_url = http_tunnel.public_url
        
        print(f"\n✅ Backend server running locally at: http://localhost:8000")
        print(f"✅ Ngrok tunnel established at: {public_url}\n")
        
        # Keep the script running
        print("Press Ctrl+C to stop the server and tunnel...")
        while True:
            # Print some server output
            output = backend_process.stdout.readline()
            if output:
                print(output.strip())
            
            # Check if process is still running
            if backend_process.poll() is not None:
                print("Backend server stopped unexpectedly.")
                break
                
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\nShutting down server and ngrok tunnel...")
    finally:
        # Clean up
        ngrok.kill()
        if backend_process.poll() is None:
            backend_process.terminate()
            backend_process.wait()
        print("Server and tunnel stopped.")

if __name__ == "__main__":
    run_backend_with_ngrok()
