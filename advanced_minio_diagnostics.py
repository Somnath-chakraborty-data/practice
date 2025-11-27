# Advanced MinIO Diagnostics
# This script performs deeper investigation into the MinIO connection issue

import socket
import subprocess
import sys

def check_what_is_on_port(port):
    """Check what process is using a specific port"""
    print(f"\n[Checking what's running on port {port}]")
    try:
        result = subprocess.run(
            ["powershell", "-Command", f"Get-NetTCPConnection -LocalPort {port} -ErrorAction SilentlyContinue | Select-Object LocalAddress, LocalPort, State, OwningProcess"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.stdout.strip():
            print(result.stdout)
            
            # Get process details
            lines = result.stdout.strip().split('\n')
            if len(lines) > 1:
                # Extract PID from the output
                for line in lines[1:]:
                    parts = line.split()
                    if parts:
                        pid = parts[-1]
                        proc_result = subprocess.run(
                            ["powershell", "-Command", f"Get-Process -Id {pid} -ErrorAction SilentlyContinue | Select-Object ProcessName, Id, Path"],
                            capture_output=True,
                            text=True,
                            timeout=5
                        )
                        print(f"\nProcess Details:")
                        print(proc_result.stdout)
        else:
            print(f"    No process found listening on port {port}")
    except Exception as e:
        print(f"    Error: {str(e)}")

def test_raw_connection():
    """Test raw TCP connection to MinIO"""
    print("\n[Testing raw TCP connection to 127.0.0.1:9000]")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect(("127.0.0.1", 9000))
        
        # Send a simple HTTP request
        request = b"GET / HTTP/1.1\r\nHost: 127.0.0.1:9000\r\n\r\n"
        sock.send(request)
        
        # Receive response
        response = sock.recv(4096)
        sock.close()
        
        print("    [OK] Connection successful!")
        print(f"\n    Raw response (first 500 chars):")
        print(f"    {response[:500]}")
        
        # Check if response looks like HTTP
        if response.startswith(b"HTTP/"):
            print("\n    [OK] Response looks like valid HTTP")
        else:
            print("\n    [WARNING] Response does NOT look like valid HTTP!")
            print(f"    Response starts with: {response[:50]}")
            
    except socket.timeout:
        print("    [ERROR] Connection timeout")
    except ConnectionRefusedError:
        print("    [ERROR] Connection refused")
    except Exception as e:
        print(f"    [ERROR] {str(e)}")

def check_proxy_settings():
    """Check system proxy settings"""
    print("\n[Checking system proxy settings]")
    try:
        result = subprocess.run(
            ["powershell", "-Command", "Get-ItemProperty -Path 'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings' | Select-Object ProxyEnable, ProxyServer"],
            capture_output=True,
            text=True,
            timeout=5
        )
        print(result.stdout)
        
        # Also check environment variables
        result2 = subprocess.run(
            ["powershell", "-Command", "Get-ChildItem Env: | Where-Object {$_.Name -like '*PROXY*'} | Format-Table Name, Value"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result2.stdout.strip():
            print("\nEnvironment proxy variables:")
            print(result2.stdout)
        else:
            print("\nNo proxy environment variables found")
            
    except Exception as e:
        print(f"    Error: {str(e)}")

def check_mc_version_and_config():
    """Check mc client version and configuration"""
    print("\n[Checking MinIO Client (mc) configuration]")
    try:
        # Check mc version
        result = subprocess.run(
            ["mc", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        print(f"mc version:\n{result.stdout}")
        
        # Check existing aliases
        result2 = subprocess.run(
            ["mc", "alias", "list"],
            capture_output=True,
            text=True,
            timeout=5
        )
        print(f"\nExisting aliases:\n{result2.stdout}")
        
    except Exception as e:
        print(f"    Error: {str(e)}")

def suggest_workarounds():
    """Suggest alternative approaches"""
    print("\n" + "="*60)
    print("ALTERNATIVE SOLUTIONS")
    print("="*60)
    print("\n1. Try using localhost instead of 127.0.0.1:")
    print("   mc alias set myminio http://localhost:9000 minioadmin minioadmin")
    print("\n2. Try using the machine's actual IP address")
    print("\n3. Use MinIO Web Console instead:")
    print("   Open: http://127.0.0.1:9001")
    print("   Login: minioadmin / minioadmin")
    print("\n4. Configure PySpark to connect directly (bypass mc):")
    print('   spark.config("spark.hadoop.fs.s3a.endpoint", "http://127.0.0.1:9000")')
    print('   spark.config("spark.hadoop.fs.s3a.access.key", "minioadmin")')
    print('   spark.config("spark.hadoop.fs.s3a.secret.key", "minioadmin")')
    print("\n5. Try using AWS CLI instead of mc:")
    print("   aws --endpoint-url http://127.0.0.1:9000 s3 ls")
    print("="*60)

if __name__ == "__main__":
    print("="*60)
    print("Advanced MinIO Connection Diagnostics")
    print("="*60)
    
    check_what_is_on_port(9000)
    test_raw_connection()
    check_proxy_settings()
    check_mc_version_and_config()
    suggest_workarounds()
