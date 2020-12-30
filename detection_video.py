from google.cloud import videointelligence
def detect_labels(video_uri, mode, segments=None):
    video_client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.Feature.LABEL_DETECTION]
    print(f'Processing video "{video_uri}"...')
    operation = video_client.annotate_video(
        input_uri=video_uri,
        features=features,
    )
    return operation.result()
def sort_by_first_segment_confidence(labels):
    labels.sort(key=lambda label: label.segments[0].confidence, reverse=True)
def category_entities_to_str(category_entities):
    if not category_entities:
        return ""
    entities = ", ".join([e.description for e in category_entities])
    return f" ({entities})"

def obtener_etiquetas(response):
        labels = response.annotation_results[0].segment_label_annotations
        sort_by_first_segment_confidence(labels)
        for label in labels:
                categories = category_entities_to_str(label.category_entities)
                for segment in label.segments:
                        confidence = segment.confidence
                        print(
                                f"{confidence:4.0%}",
                                f"{label.entity.description}{categories}",
                                sep=" | ",
                                )
video_uri = "gs://videoproyecto-cde/archivo.mp4"#gs://videoproyecto-cde/cup.mp4"
mode=videointelligence.LabelDetectionMode.SHOT_MODE
response = detect_labels(video_uri, mode)
obtener_etiquetas(response)
