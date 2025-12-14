# MinIO Troubleshooting Guide

## Problem Identified

Your MinIO server is running (process ID 25200) but it's not responding with proper HTTP protocol.

Error: `malformed HTTP status code` and `protocol violation`

## Root Cause

This usually happens when:
1. MinIO is still initializing/starting up
2. There's a proxy or network configuration interfering
3. MinIO was started incorrectly or with wrong parameters
4. Port conflict with another service

## Solutions (Try in Order)

### Solution 1: Restart MinIO Properly

1. **Stop the current MinIO process:**
   ```powershell
   # Find and kill the MinIO process
   Stop-Process -Name "minio" -Force
   ```

2. **Wait a few seconds, then start MinIO with proper configuration:**
   ```powershell
   # Create data directory if it doesn't exist
   New-Item -ItemType Directory -Force -Path C:\minio-data
   
   # Start MinIO server
   minio server C:\minio-data --console-address :9001
   ```

3. **Try the mc alias command again:**
   ```powershell
   mc alias set myminio http://127.0.0.1:9000 minioadmin minioadmin
   ```

### Solution 2: Check for Proxy Issues

MinIO client (mc) might be using a proxy. Disable it temporarily:

```powershell
# Disable proxy for this session
$env:HTTP_PROXY=""
$env:HTTPS_PROXY=""
$env:NO_PROXY="localhost,127.0.0.1"

# Then try again
mc alias set myminio http://127.0.0.1:9000 minioadmin minioadmin
```

### Solution 3: Use Different Credentials

Sometimes the default credentials don't work. Try setting custom ones:

1. **Stop MinIO**
2. **Set environment variables:**
   ```powershell
   $env:MINIO_ROOT_USER="admin"
   $env:MINIO_ROOT_PASSWORD="password123"
   ```

3. **Start MinIO:**
   ```powershell
   minio server C:\minio-data --console-address :9001
   ```

4. **Set alias with new credentials:**
   ```powershell
   mc alias set myminio http://127.0.0.1:9000 admin password123
   ```

### Solution 4: Check MinIO Logs

Look at the MinIO console output where you started it. Check for:
- Initialization errors
- Port binding issues
- Permission errors

### Solution 5: Verify MinIO Installation

```powershell
# Check MinIO version
minio --version

# Check mc version
mc --version
```

### Solution 6: Use MinIO Console Instead

If mc continues to have issues, you can use the web console:

1. Open browser: http://127.0.0.1:9001
2. Login with: minioadmin / minioadmin
3. Create buckets and manage files through the UI

## Quick Test Commands

After restarting MinIO, test with these commands:

```powershell
# Test 1: List aliases
mc alias list

# Test 2: Check MinIO server info
mc admin info myminio

# Test 3: List buckets
mc ls myminio
```

## For Your PySpark Code

If you need to use MinIO with PySpark and mc isn't working, you can still configure PySpark directly:

```python
spark = SparkSession.builder \
    .config("spark.hadoop.fs.s3a.endpoint", "http://127.0.0.1:9000") \
    .config("spark.hadoop.fs.s3a.access.key", "minioadmin") \
    .config("spark.hadoop.fs.s3a.secret.key", "minioadmin") \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .getOrCreate()
```

This bypasses the need for mc alias configuration.
