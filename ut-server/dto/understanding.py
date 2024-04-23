from typing import List

from pydantic import BaseModel

__all__ = [
    'DiscussPostClassifyRequest',
    'DiscussPostClassifyResponse',
    'QualityClassifyRequest',
    'QualityClassifyResponse',
    'FaceIdentifyRequest',
    'FaceIdentifyResponse',
    "FacePoseDetectRequest",
    "FacePoseDetectResponse",
    "ScreenPopDetectRequest",
    "ScreenPopDetectResponse",
    'CompanyRecognitionRequest',
    'CompanyRecognitionResponse',
    'IntentDetectionRequest',
    'IntentDetectionResponse',
    'CompanyNormalizationRequest',
    'CompanyNormalizationResponse',
    'TagDocumentRequest',
    'TagDocumentResponse',
    'UgcBinaryClassificationRequest',
    'UgcBinaryClassificationResponse',
    'ArticleBinaryClassificationRequest',
    'ArticleBinaryClassificationResponse',
    'GenerateQuestionRequest',
    'GenerateQuestionResponse',
    'CommentAutoTagRequest',
    'CommentAutoTagResponse',
    'SegmentRequest',
    'SegmentResponse',
    'TextEntityIdRequest',
    'TxFmResponse',
    'MomentClassifierRequest',
    'MomentClassifierResponse',
    'PostCareerResponse',
    'PostCareerRequest',
    'ResumeBertRequest',
    'ResumeBertResponse',
    'EntityBertRequest',
    'EntityBertResponse',
    'LangChainQaRequest',
    'LangChainQaResponse',
    'RetrieveRelatedTextRequest',
    'RetrieveRelatedTextResponse',
    'RetrieveRelatedQuestionRequest',
    'RetrieveRelatedQuestionResponse',
    'RelatedText',
    'RelatedQuestion',
    'ChatGptRequest',
    'ChatGptResponse',
    'SentenceSplitRequest',
    'SentenceSplitResponse',
    'JdJobClassifierRequest',
    'JdJobClassifierResponse',
    'JdJobClassifierV2Request',
    'JdJobClassifierV2Response',
    'CompanyRecognitionV2Request',
    'CompanyRecognitionV2Response',
    'Text2VectorRequest',
    'Text2VectorResponse']


class Text2VectorRequest(BaseModel):
    text: str


class Text2VectorResponse(BaseModel):
    result: List[float]


class DiscussPostClassifyRequest(BaseModel):
    title: str = ''
    content: str = ''


class DiscussPostClassifyResponse(BaseModel):
    label1: int
    prob1: float
    label2: int
    prob2: float


class QualityClassifyRequest(BaseModel):
    title: str = ''
    content: str = ''


class QualityClassifyResponse(BaseModel):
    label: int
    prob: float


class JdJobClassifierRequest(BaseModel):
    jobDescription: str


class JdJobClassifierResponse(BaseModel):
    careerJobId: int


class JdJobClassifierV2Request(BaseModel):
    jobName: str
    jobDescription: str


class JdJobClassifierV2Response(BaseModel):
    careerJobId: int


class CompanyRecognitionV2Request(BaseModel):
    companyList: List[str]
    document: str


class CompanyRecognitionV2Response(BaseModel):
    labels: List[int]


class TextEntityIdRequest(BaseModel):
    entityId: int


class TxFmResponse(BaseModel):
    form: int
    formProb: float
    taxonomy1: int
    taxonomy1Prob: float


class MomentClassifierRequest(BaseModel):
    content: str


class MomentClassifierResponse(BaseModel):
    form: int
    formProb: float
    taxonomy1: int
    taxonomy1Prob: float


class SentenceSplitRequest(BaseModel):
    texts: str


class SentenceSplitResponse(BaseModel):
    params: List[str]


class PostCareerRequest(BaseModel):
    content: str


class PostCareerResponse(BaseModel):
    career: int
    careerProb: float


class LangChainQaRequest(BaseModel):
    query: str


class LangChainQaResponse(BaseModel):
    results: str


class RetrieveRelatedTextRequest(BaseModel):
    query: str
    companyId: int
    topK: int = 5


class RelatedText(BaseModel):
    text: str
    score: float
    companyId: int
    docId: int


class RetrieveRelatedTextResponse(BaseModel):
    results: List[RelatedText]


class RetrieveRelatedQuestionRequest(BaseModel):
    query: str
    skills: str
    companyId: int
    topK: int = 5


class RelatedQuestion(BaseModel):
    text: str
    score: float
    category: str
    companyId: int
    skills: str
    analysis: str
    docId: int


class RetrieveRelatedQuestionResponse(BaseModel):
    results: List[RelatedQuestion]


class ResumeBertRequest(BaseModel):
    resumeId: int
    content: str


class ResumeBertResponse(BaseModel):
    resumeId: int


class EntityBertRequest(BaseModel):
    entityId: int
    title: str
    content: str


class EntityBertResponse(BaseModel):
    entityId: int


# 人脸相似度判定
class FaceIdentifyRequest(BaseModel):
    targetUrl: str
    sourceUrl: str


class FaceIdentifyResponse(BaseModel):
    invalid: int
    differentPeople: int


# 人脸姿态判定
class FacePoseDetectRequest(BaseModel):
    url: str


class FacePoseDetectResponse(BaseModel):
    turnLeftOrRight: int
    incompleteFace: int
    imageQuality: int


class ScreensInfo(BaseModel):
    x: int
    y: int
    w: int
    h: int


class Config(BaseModel):
    version: str


class ScreenPopDetectRequest(BaseModel):
    imageUrl: str
    imgWidth: int
    imgHeight: int
    screens: List[ScreensInfo]
    config: Config


class ClsInfo(BaseModel):
    screenCls: int
    score: float


class ScreenData(BaseModel):
    version: str
    isPop: str
    screenImg: List[ClsInfo]


class ScreenPopDetectResponse(BaseModel):
    message: str
    code: int
    data: ScreenData


class Company(BaseModel):
    company: str
    confidence: float


class Intent(BaseModel):
    intent: str
    confidence: float


class CompanyRecognitionRequest(BaseModel):
    query: List[str]
    words: List[str]


class CompanyRecognitionResponse(BaseModel):
    results: List[Company]


class SegmentRequest(BaseModel):
    query: str


class SegmentResponse(BaseModel):
    result: List[str]


class IntentDetectionRequest(BaseModel):
    query: str


class IntentDetectionResponse(BaseModel):
    results: List[Intent]


class QueryWithRole(BaseModel):
    role: int
    query: str


class ChatGptRequest(BaseModel):
    query: str = None
    queries: List[QueryWithRole] = None
    callback: str = None


class ChatGptResponse(BaseModel):
    results: str
    total_tokens: int


class CompanyNormalizationRequest(BaseModel):
    query: str


class CompanyNormalizationResponse(BaseModel):
    com_id: str
    com_registered_name: str
    com_alias: List
    com_relative_com: List


class TagDocumentRequest(BaseModel):
    text: str
    words: List[str]


class TagDocumentResponse(BaseModel):
    results: List[Company]


class Comment(BaseModel):
    label: int
    confidence: float


class CommentAutoTagRequest(BaseModel):
    texts: str


class CommentAutoTagResponse(BaseModel):
    isInternalRecommendation: int
    confidence: float


class Ugc(BaseModel):
    label: int
    confidence: float


class UgcBinaryClassificationRequest(BaseModel):
    texts: List[str]


class UgcBinaryClassificationResponse(BaseModel):
    results: List[Ugc]


class ArticleBinaryClassificationRequest(BaseModel):
    text: str


class SentenceLabel(BaseModel):
    label: int
    confidence: float
    sentence: str


class ArticleBinaryClassificationResponse(BaseModel):
    results: List[SentenceLabel]


class GenerateQuestionRequest(BaseModel):
    queLength: int = None
    university: str = None
    work: str = None
    award: str = None


class GenerateQuestionResponse(BaseModel):
    code: int
    data: List[str]
