
from src.database import update_enquiry_status, get_all_enquiries

request_id = 27

update_enquiry_status(request_id, "in_progress")

enquiries = get_all_enquiries()
enquiry = next(
    item for item in enquiries
    if item["request_id"] == request_id
)

print("Request ID:", enquiry["request_id"])
print("Status:", enquiry["status"])
print("Reviewed at:", enquiry["reviewed_at"])
