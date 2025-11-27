# MinIO Connection Issue - RESOLVED ✅

## Problem Summary

**Error Message:**
```
mc.exe: <ERROR> Unable to initialize new alias from the provided credentials. 
Get "http://127.0.0.1:9000/...": net/http: HTTP/1.x transport connection broken: 
malformed HTTP status code "127.0.0.1:9000".
```

## Root Cause Identified

A **Python process** (PID 21448) was **also listening on port 9000**, creating a port conflict with MinIO. When the MinIO client (`mc`) tried to connect, it received binary data from the Python process instead of proper HTTP responses from MinIO.

### Diagnostic Evidence:
- Port 9000 had TWO processes:
  - MinIO (PID 13276) - `C:\minio\minio.exe` ✅
  - Python (PID 21448) - `C:\Program Files\Python311\python.exe` ❌
- Raw TCP test showed non-HTTP binary response: `b'\xff\x00\x00\x00...'`
- This caused the "malformed HTTP status code" error

## Solution Applied

1. **Stopped the interfering Python process**
2. **Verified only MinIO is on port 9000**
3. **Successfully set mc alias**

## Verification - All Working! ✅

```powershell
# Alias is set
mc alias list
# Shows: myminio -> http://127.0.0.1:9000

# MinIO server info
mc admin info myminio
# Shows: Server running, 476 GiB storage, 41.4% used

# List buckets
mc ls myminio
# Working (currently no buckets)
```

## How to Prevent This in the Future

### Issue: PySpark/Python Scripts Binding to Port 9000

If you're running PySpark scripts that might bind to port 9000, make sure to:

1. **Always stop PySpark sessions properly:**
   ```python
   spark.stop()
   ```

2. **Check for lingering Python processes before starting MinIO:**
   ```powershell
   Get-Process python | Where-Object {$_.Id -in (Get-NetTCPConnection -LocalPort 9000).OwningProcess}
   ```

3. **Use the diagnostic script:**
   ```powershell
   python advanced_minio_diagnostics.py
   ```

## Quick Reference Commands

### Check MinIO Status
```powershell
mc admin info myminio
```

### List Buckets
```powershell
mc ls myminio
```

### Create a Bucket
```powershell
mc mb myminio/mybucket
```

### Upload a File
```powershell
mc cp myfile.txt myminio/mybucket/
```

### List Files in Bucket
```powershell
mc ls myminio/mybucket
```

### Access MinIO Console
Open in browser: http://127.0.0.1:9001
- Username: `minioadmin`
- Password: `minioadmin`

## For Your PySpark Notebook

Your PySpark configuration is already correct:

```python
spark = SparkSession.builder \
    .config("spark.hadoop.fs.s3a.endpoint", "http://127.0.0.1:9000") \
    .config("spark.hadoop.fs.s3a.access.key", "minioadmin") \
    .config("spark.hadoop.fs.s3a.secret.key", "minioadmin") \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .getOrCreate()

# Read from MinIO
df = spark.read.format("binaryFile").load("s3a://bronze/")
```

## Files Created for Troubleshooting

1. **check_minio_connection.py** - Basic MinIO diagnostics
2. **advanced_minio_diagnostics.py** - Deep diagnostic analysis (found the issue!)
3. **restart_minio.ps1** - Restart MinIO properly
4. **fix_minio_port_conflict.ps1** - Fix port conflicts (solved the problem!)
5. **MINIO_TROUBLESHOOTING.md** - General troubleshooting guide

---

**Status: RESOLVED ✅**

Your MinIO is now properly configured and working with the `mc` client!
