from datetime import datetime, timedelta, timezone
from aws_xray_sdk.core import xray_recorder


class UserActivities:
    def run(user_handle):
        try:
            model = {
                'errors': None,
                'data': None
            }

            now = datetime.now(timezone.utc).astimezone()

            if user_handle == None or len(user_handle) < 1:
                model['errors'] = ['blank_user_handle']
            else:
                now = datetime.now()
                results = [{
                    'uuid': '248959df-3079-4947-b847-9e0892d1bab4',
                    'handle':  'Andrew Brown',
                    'message': 'Cloud is fun!',
                    'created_at': (now - timedelta(days=1)).isoformat(),
                    'expires_at': (now + timedelta(days=31)).isoformat()
                }]
                model['data'] = results
            # Start a subsegment --- xray ---
            subsegment = xray_recorder.begin_subsegment('mock-data')
            # Create dictionary for segment --- xray ---
            dict = {
                "now": now.isoformat(),
                "results-size": len(model['data'])
            }
            # Add metadata to subsegment --- xray ---
            # Close the segment & sub-segment
            xray_recorder.end_subsegment()
        finally:
            xray_recorder.end_subsegment()
            # The main issue was closing a segment that was not defined ...
            # xray_recorder.end_segment()
        return model