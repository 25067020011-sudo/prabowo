#!/usr/bin/env python3
"""
Brand24 MCP (Model Context Protocol) Client & Integration Module
Menghubungkan agen riset dengan server MCP resmi Brand24 (https://mcp.brand24.com/v1/mcp).
Mendukung penarikan mentions publik, volume sentimen, dan metrik emosi real-time.
"""

import os
import sys
import json
import urllib.request
import urllib.error

BRAND24_MCP_ENDPOINT = "https://mcp.brand24.com/v1/mcp"

def get_brand24_token():
    """Mengambil token Brand24 dari environment variable atau file .env"""
    token = os.environ.get("BRAND24_API_KEY") or os.environ.get("BRAND24_BEARER_TOKEN")
    if not token and os.path.exists(".env"):
        with open(".env", "r") as f:
            for line in f:
                if line.startswith("BRAND24_API_KEY=") or line.startswith("BRAND24_BEARER_TOKEN="):
                    token = line.strip().split("=", 1)[1].strip("\"'")
                    break
    return token

def call_brand24_mcp(method, params=None, token=None):
    """Mengirim request JSON-RPC 2.0 ke server Brand24 MCP"""
    if not token:
        token = get_brand24_token()
    
    if not token:
        return {
            "success": False,
            "error": "BRAND24_API_KEY / Bearer token belum disetel. Dapatkan token dari https://app.brand24.com/"
        }
    
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params or {}
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
        "User-Agent": "Antigravity-ResearchAgent/1.0"
    }
    
    req = urllib.request.Request(
        BRAND24_MCP_ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return {"success": True, "data": data}
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8", errors="ignore")
        return {"success": False, "http_code": e.code, "error": err_msg}
    except Exception as e:
        return {"success": False, "error": str(e)}

def list_mcp_tools(token=None):
    """Mendaftar tool yang tersedia di server MCP Brand24"""
    # 1. Initialize
    init_res = call_brand24_mcp(
        "initialize",
        params={
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "Antigravity-Research", "version": "1.0"}
        },
        token=token
    )
    if not init_res["success"]:
        return init_res
    
    # 2. List tools
    tools_res = call_brand24_mcp("tools/list", params={}, token=token)
    return tools_res

if __name__ == "__main__":
    token = get_brand24_token()
    if len(sys.argv) > 1:
        token = sys.argv[1]
    
    print("=" * 60)
    print("Brand24 MCP Server Diagnostic & Client")
    print("Endpoint:", BRAND24_MCP_ENDPOINT)
    print("=" * 60)
    
    if not token:
        print("[INFO] Bearer token belum disetel.")
        print("Untuk menghubungkan live Brand24 MCP:")
        print("1. Buka dashboard akun Anda di https://app.brand24.com/")
        print("2. Dapatkan API Key / Bearer Token dari menu Settings / Integrations.")
        print("3. Jalankan: python3 src/collector/brand24_mcp_client.py <TOKEN_ANDA>")
        print("   Atau tambahkan BRAND24_API_KEY=<TOKEN> di berkas .env")
    else:
        print(f"[INFO] Menguji koneksi dengan token: {token[:6]}...{token[-4:]}")
        res = list_mcp_tools(token=token)
        print("Response:", json.dumps(res, indent=2))
