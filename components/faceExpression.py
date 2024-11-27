from deepface import DeepFace
import asyncio
from typing import Dict, Any

class FaceExpression:

    def __init__(self, enforce_detection: bool = False, detector_backend: str = "mediapipe", align: bool = False):
        self.enforce_detection = enforce_detection
        self.detector_backend = detector_backend
        self.detector_backend_list = ['opencv', 'dlib', 'mediapipe']
        self.align = align

        if self.detector_backend not in self.detector_backend_list:
            raise ValueError(f"Invalid detector_backend. Must be one of {self.detector_backend_list}")

    def getFaceExpression(self, rgb_img) -> Dict[str, Any]:
        try:
            analysisResult = DeepFace.analyze(rgb_img,
                                              actions=['emotion'],
                                            #   actions=['emotion', 'age', 'gender'],
                                              enforce_detection=self.enforce_detection,
                                              detector_backend=self.detector_backend,
                                              align=self.align
                                              )

            print("Analysis Result",analysisResult)
            emotiondict = analysisResult[0]["emotion"]
            dominantemotion = analysisResult[0]["dominant_emotion"]
            # face_confidence = analysisResult[0]['face_confidence']
            # age = analysisResult[0]['age']
            # dominant_gender = analysisResult[0]['dominant_gender']
            # left_eye_region = analysisResult[0]['region']['left_eye']
            # right_eye_region = analysisResult[0]['region']['right_eye']

            analysisDict = {
                "emotiondict": emotiondict,
                "dominantemotion": dominantemotion,
                # "face_confidence": face_confidence,
                # "age": age,
                # "dominant_gender": dominant_gender,
                # "leye_region": left_eye_region,
                # "reye_region": right_eye_region
            }

            return analysisDict

        except Exception as e:
            print(f"Error in face expression analysis: {e}")
            return {}

    async def getExpressionRunner(self, rgb_img) -> Dict[str, Any]:
        task = asyncio.to_thread(self.getFaceExpression, rgb_img)
        emo_dict = await task
        return emo_dict
