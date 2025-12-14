import socket
import requests
import subprocess

def check_port(host, port):
    """Check if a port is open"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    try:
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception as e:
        return False

def check_minio_health():
    """Check MinIO server health"""
    print("="*60)
    print("MinIO Connection Diagnostics")
    print("="*60)
    
    # Check if port 9000 is open
    print("\n[1] Checking if port 9000 is open...")
    if check_port("127.0.0.1", 9000):
        print("    [OK] Port 9000 is OPEN")
    else:
        print("    [X] Port 9000 is CLOSED or not responding")
        print("    -> MinIO server might not be running!")
        return False
    
    # Check if port 9001 (console) is open
    print("\n[2] Checking if port 9001 (MinIO Console) is open...")
    if check_port("127.0.0.1", 9001):
        print("    [OK] Port 9001 is OPEN")
    else:
        print("    [X] Port 9001 is CLOSED")
        print("    -> MinIO console might not be configured")
    
    # Try to access MinIO health endpoint
    print("\n[3] Checking MinIO health endpoint...")
    try:
        response = requests.get("http://127.0.0.1:9000/minio/health/live", timeout=5)
        if response.status_code == 200:
            print("    [OK] MinIO is responding and healthy")
            return True
        else:
            print(f"    [X] MinIO responded with status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("    [X] Connection refused - MinIO is not responding")
        print("    -> The port is open but MinIO is not running properly")
        return False
    except requests.exceptions.Timeout:
        print("    [X] Connection timeout")
        return False
    except Exception as e:
        print(f"    [X] Error: {str(e)}")
        return False

def check_minio_process():
    """Check if MinIO process is running"""
    print("\n[4] Checking for MinIO process...")
    try:
        result = subprocess.run(
            ["powershell", "-Command", "Get-Process | Where-Object {$_.ProcessName -like '*minio*'} | Select-Object ProcessName, Id, CPU"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.stdout.strip():
            print("    [OK] MinIO process found:")
            print(result.stdout)
            return True
        else:
            print("    [X] No MinIO process found")
            return False
    except Exception as e:
        print(f"    [X] Error checking process: {str(e)}")
        return False

def provide_solutions():
    """Provide solutions based on diagnostics"""
    print("\n" + "="*60)
    print("SOLUTIONS")
    print("="*60)
    print("\n1. Start MinIO Server:")
    print("   Run this command in a separate PowerShell window:")
    print("   minio server C:\\minio-data --console-address :9001")
    print()
    print("2. Or if you have a specific data directory:")
    print("   minio server <your-data-path> --console-address :9001")
    print()
    print("3. Check if MinIO is installed:")
    print("   minio --version")
    print()
    print("4. After starting MinIO, try the mc alias command again:")
    print("   mc alias set myminio http://127.0.0.1:9000 minioadmin minioadmin")
    print()
    print("5. Access MinIO Console in browser:")
    print("   http://127.0.0.1:9001")
    print("   Username: minioadmin")
    print("   Password: minioadmin")
    print("="*60)

if __name__ == "__main__":
    try:
        is_healthy = check_minio_health()
        is_process_running = check_minio_process()
        
        if is_healthy:
            print("\n[SUCCESS] MinIO is running properly!")
            print("\nYou can now run:")
            print("mc alias set myminio http://127.0.0.1:9000 minioadmin minioadmin")
        else:
            provide_solutions()
            
    except Exception as e:
        print(f"\nError during diagnostics: {str(e)}")
        provide_solutions()
