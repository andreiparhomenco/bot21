#!/usr/bin/env python3
"""
Helper script to prepare Google credentials for Railway deployment
Converts credentials file to a single-line JSON string suitable for Railway env vars
"""
import json
import sys
from pathlib import Path


def prepare_credentials(input_file="credentials/google_credentials.json"):
    """Read and format credentials file for Railway"""
    
    try:
        # Read the credentials file
        creds_path = Path(input_file)
        
        if not creds_path.exists():
            print(f"❌ Error: File not found: {input_file}")
            print(f"   Make sure you have the Google credentials file at this location")
            return None
        
        # Load and validate JSON
        with open(creds_path, 'r', encoding='utf-8') as f:
            credentials = json.load(f)
        
        # Validate required fields
        required_fields = ['type', 'project_id', 'private_key', 'client_email']
        missing_fields = [field for field in required_fields if field not in credentials]
        
        if missing_fields:
            print(f"❌ Error: Missing required fields: {', '.join(missing_fields)}")
            return None
        
        # Convert to compact JSON string (single line, no extra spaces)
        compact_json = json.dumps(credentials, separators=(',', ':'), ensure_ascii=False)
        
        print("✅ Successfully prepared credentials!")
        print("\n" + "="*80)
        print("📋 Copy this ENTIRE string and paste as GOOGLE_CREDENTIALS in Railway:")
        print("="*80)
        print()
        print(compact_json)
        print()
        print("="*80)
        print(f"📊 Stats:")
        print(f"   Length: {len(compact_json)} characters")
        print(f"   Type: {credentials.get('type')}")
        print(f"   Project: {credentials.get('project_id')}")
        print(f"   Client: {credentials.get('client_email')}")
        print("="*80)
        print()
        print("📝 Instructions:")
        print("   1. Select and copy the JSON string above (between the === lines)")
        print("   2. Go to Railway Dashboard → Your Project → Variables")
        print("   3. Add new variable:")
        print("      Name: GOOGLE_CREDENTIALS")
        print("      Value: <paste the JSON>")
        print("   4. Save and redeploy")
        print()
        
        return compact_json
        
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in credentials file: {e}")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


if __name__ == "__main__":
    # Allow custom file path as argument
    input_file = sys.argv[1] if len(sys.argv) > 1 else "credentials/google_credentials.json"
    
    prepare_credentials(input_file)


