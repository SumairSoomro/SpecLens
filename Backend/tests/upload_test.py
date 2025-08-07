import json
import asyncio
from app.routes.upload_spec import handle_uploaded_spec


# Mock class to simulate FastAPI's UploadFile
class MockUploadFile:
    def __init__(self, content: str, filename: str):
        self.content = content
        self.filename = filename

    async def read(self):
        return self.content.encode('utf-8')  # Mimic async file.read()

def main():
    print("Testing handle_uploaded_spec...")

    # Step 1: Define a simple OpenAPI spec as a Python dict
    spec_content = {
        "openapi": "3.0.0",
        "info": {
            "title": "Test API",
            "version": "1.0.0"
        },
        "paths": {
            "/users": {
                "get": {
                    "summary": "Get all users",
                    "responses": {
                        "200": {
                            "description": "Success"
                        }
                    }
                }
            }
        }
    }

    # Step 2: Create the mock file object
    mock_file = MockUploadFile(
        content=json.dumps(spec_content, indent=2),
        filename="test-api.json"
    )

    # Step 3: Run the async function inside an event loop
    try:
        result = asyncio.run(handle_uploaded_spec(
            user_id="test-user-123",
            spec_id="test-spec-456",
            file=mock_file
        ))

        print(f"✅ Success! Processed {result} chunks")
        print("Check your Pinecone index for:")
        print(f"  - User ID: test-user-123")
        print(f"  - Spec ID: test-spec-456")
        print("  - Should contain content about /users endpoint")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
