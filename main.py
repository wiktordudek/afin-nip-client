import json

from afin_nip_client.client import AfinClient
from afin_nip_client.models import CompanyInfo


def main():
    with AfinClient() as client:
        info: CompanyInfo = client.get("525-26-74-798")  # Allegro

    pretty: str = json.dumps(
        info.to_dict(),
        indent=4,
        ensure_ascii=False,
    )
    print(pretty)


if __name__ == "__main__":
    main()
