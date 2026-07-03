import asyncio

from services.websub_service import WebSubService


async def main():
    service = WebSubService(
        "https://example.com/webhook"
    )

    result = await service.subscribe(
        "UCX6OQ3DkcsbYNE6H8uQQuVA"
    )

    print(result)


if __name__ == "__main__":
    asyncio.run(main())