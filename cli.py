import httpx
import asyncio
import json

async def analyze_ticket_cli(ticket_content: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post("http://localhost:8000/analyze_ticket", content=ticket_content)
            response.raise_for_status()  # Raise an exception for bad status codes
            analysis = response.json()
            print(json.dumps(analysis, indent=2))
        except httpx.HTTPStatusError as e:
            print(f"Error: {e.response.status_code} - {e.response.text}")
        except httpx.RequestError as e:
            print(f"An error occurred while requesting {e.request.url!r}: {e}")

async def main():
    print("Enter your support ticket (press Ctrl+D or Ctrl+Z and then Enter to finish input):")
    ticket_lines = []
    while True:
        try:
            line = input()
            ticket_lines.append(line)
        except EOFError:
            break
    ticket_content = "\n".join(ticket_lines)
    if ticket_content.strip():
        await analyze_ticket_cli(ticket_content)
    else:
        print("No ticket content provided.")

if __name__ == "__main__":
    asyncio.run(main())

