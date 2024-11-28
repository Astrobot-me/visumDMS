from deepface import DeepFace
import asyncio
from typing import Dict, Any, Optional

class FaceExpression:

    def __init__(self, enforce_detection: bool = False, detector_backend: str = "mediapipe", align: bool = False):
        self.enforce_detection = enforce_detection
        self.detector_backend = detector_backend
        self.detector_backend_list = ['opencv', 'dlib', 'mediapipe']
        self.align = align

        if self.detector_backend not in self.detector_backend_list:
            raise ValueError(f"Invalid detector_backend. Must be one of {self.detector_backend_list}")

    def getFaceExpression(self, rgb_img: Any) -> Dict[str, Any]:
        """
        Analyzes the facial expression from the given image.

        Args:
            rgb_img (Any): Image in RGB format.

        Returns:
            Dict[str, Any]: Dictionary with emotion analysis or "UNREL_DATA" in case of errors.
        """
        try:
            if rgb_img is None:
                raise ValueError("Input image (rgb_img) cannot be None.")

            # Perform emotion analysis using DeepFace
            analysis_result = DeepFace.analyze(
                rgb_img,
                actions=['emotion'],
                enforce_detection=self.enforce_detection,
                detector_backend=self.detector_backend,
                align=self.align
            )

            emotion_dict = analysis_result[0].get("emotion", {})
            dominant_emotion = analysis_result[0].get("dominant_emotion", None)

            # Construct the result dictionary
            analysis_dict = {
                "emotiondict": emotion_dict,
                "dominantemotion": dominant_emotion,
            }

            return analysis_dict

        except ValueError as ve:
            print(f"ValueError: {ve}")
        except KeyError as ke:
            print(f"KeyError: Missing expected key in the analysis result: {ke}")
        except Exception as e:
            print(f"Unexpected error in face expression analysis: {e}")

        # Return dictionary with "UNREL_DATA" in case of error
        return {"UNREL_DATA": "Unable to process the image or analyze emotions."}

    async def getExpressionRunner(self, rgb_img: Any) -> Dict[str, Any]:
        """
        Asynchronous wrapper for analyzing facial expressions.

        Args:
            rgb_img (Any): Image in RGB format.

        Returns:
            Dict[str, Any]: Dictionary with emotion analysis or "UNREL_DATA" in case of errors.
        """
        try:
            task = asyncio.to_thread(self.getFaceExpression, rgb_img)
            emo_dict = await task
            return emo_dict
        except Exception as e:
            print(f"Error in asynchronous face expression analysis: {e}")
            return {"UNREL_DATA": "Error occurred during asynchronous processing."}

    async def getExpressionRunner(self, rgb_img) -> Dict[str, Any]:
        task = asyncio.to_thread(self.getFaceExpression, rgb_img)
        emo_dict = await task
        return emo_dict
