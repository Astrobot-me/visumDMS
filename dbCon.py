import firebase_admin
from firebase_admin import credentials, firestore 

class FirestoreDB:
    def __init__(self, key_path: str, collection_name: str):
        # Initialize Firebase Admin SDK
        cred = credentials.Certificate(key_path)
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()
        self.collection_name = collection_name

    def insert_into_db(self, head_state:str,img_frame:str,eye_state:str,hazard_status: str, yawn_phase_state: str, yawn_phase_count:str,reported_ear: float,sos_state : bool,current_vehicle_status:str,alcohol_quantity:str,driver_reported_image:str,lat:float,long:float,
                        location_text: str,
                       maps_link: str):
        data = {
            "head_state":head_state, 
            "eye_state":eye_state, 
            "hazard_status": hazard_status,
            "reported_ear": reported_ear,
            "yawn_phase_state":yawn_phase_state, 
            "yawn_phase_count":yawn_phase_count, 
            "sos_state":sos_state, 
            "current_vehicle_status":current_vehicle_status, 
            "vehicle_cords":{"lat":lat, "long":long},
            "alcohol_quantity":alcohol_quantity, 
            "driver_reported_image":driver_reported_image,
            "location_text": location_text,
            "maps_link": maps_link,
            "img_frame":img_frame,
            "timestamp": firestore.SERVER_TIMESTAMP
        }
        try:
            doc_ref = self.db.collection(self.collection_name).add(data)
            print(f"Document inserted with ID: {doc_ref[1].id}")
        except Exception as e: 
            print(f"[ERROR/DBCON]: Exception Occured in Db Connection :: {e}")

# # Example usage:
# if __name__ == "__main__":
#     firestore_instance = FirestoreDB("serviceAccountKey.json", "dashboard_data")
#     firestore_instance.insert_into_db(
#         hazard_status="NOT SAFE",
#         connection_status="connected",
#         reported_ear=3.21,
#         city="Patna",
#         region="Bihar",
#         coordinates="Patna",
#         location_text="25.5941,85.1356",
#         maps_link="https://maps.app.goo.gl/nkmmm5aEjFkprL1H7?g_st=ac"
#     )


firestore_instance = FirestoreDB("serviceAccountKey.json", "locations")

   