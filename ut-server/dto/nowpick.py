from typing import List

from pydantic import BaseModel

__all__ = [
    'NowpickInviteUserRequest',
    'NowpickInviteUserResponse',
    'ResumeRecommendRequest',
    'ResumeRecommendResponse']


class NowpickInviteUserRequest(BaseModel):
    rid: str


class Resume(BaseModel):
    resumeId: int
    confidence: float


class NowpickInviteUserResponse(BaseModel):
    resumes: List[Resume]


class ResumeRecommendResponse(BaseModel):
    resumes: List[Resume]


class InviteAction(BaseModel):
    sex_var: str = ''
    data: str = ''
    pt: str = ''
    session: str = ''
    type: str = ''
    uid: str = ''
    highesteducation_var: str = ''
    schoolstatus_var: str = ''
    city_var: str = ''
    id: int = 0
    resumeid_var: str = ''
    event: str = ''
    age_var: int = 0
    position_var: str = ''
    ext: str = ''
    cuid: str = ''
    positionlevel1_var: str = ''
    positionlevel2_var: str = ''
    positionlevel3_var: str = ''
    tags: str = ''
    graduationtime_var: int = 0
    resumeid: int = 0
    pit_var: str = ''
    logid_var: str = ''
    event_time: str = ''


class ResumeRecommendRequest(BaseModel):
    histories: List[InviteAction]
