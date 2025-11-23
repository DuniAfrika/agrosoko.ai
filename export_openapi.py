#!/usr/bin/env python3
"""
Export OpenAPI specification for watsonx Orchestrate integration.
"""

import json
from app.main import app

def export_openapi():
    """Export OpenAPI spec to openapi.json file."""
    
    # Get OpenAPI schema
    openapi_schema = app.openapi()
    
    # Save to file
    output_file = "openapi.json"
    with open(output_file, "w") as f:
        json.dump(openapi_schema, f, indent=2)
    
    print(f"✅ OpenAPI specification exported to: {output_file}")
    print(f"📄 File size: {len(json.dumps(openapi_schema))} bytes")
    print(f"📊 Endpoints: {len(openapi_schema.get('paths', {}))}")
    print(f"\n🚀 Ready for watsonx Orchestrate!")
    print(f"\nTo use:")
    print(f"  1. Import {output_file} into watsonx Orchestrate")
    print(f"  2. Configure the server URL in orchestrate")
    print(f"  3. Start using the APIs!")

if __name__ == "__main__":
    export_openapi()

