from django.core.management.base import BaseCommand
from common.RTAFUser.models import Affiliation

import requests

class Command(BaseCommand):
    help = "Fetch and save affiliation data from API"

    def handle(self, *args, **kwargs):
        # API URL
        url = "https://telephone.rtaf.mi.th/api/v1/unit/DGyaEgw-VZyAzprXgMxYqzWfPs5dRwrtivRZbqNMvf0/struc/all"
        
        try:
            # Send GET request to API
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for 4XX/5XX errors

            # Parse JSON response
            data = response.json()

            # Process each item in 'data' array
            for item in data.get('data', []):
                # Fetch required fields
                hris_code = item.get("ORG_TUNIT_PK", "")
                short_name = item.get("ORG_ABBR_NAME", "")
                full_name = item.get("ORG_ABBR_NAME", "")  # Use the short name for both fields as an example

                # You can further map 'children' to set up affiliations (recursive if needed)

                # Save affiliation
                Affiliation.objects.update_or_create(
                    hris_code=hris_code,
                    defaults={
                        'short_name': short_name,
                        'full_name': full_name,
                        'is_rtaf_directed': True,  # Assuming all are RTAF directed
                        'super_affiliation': None  # Assuming no parent structure for now
                    }
                )

            self.stdout.write(self.style.SUCCESS('Data successfully saved.'))

        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f"API request failed: {e}"))

