from pydantic import BaseModel, Field


class Photo(BaseModel):
    fullSizeUri: str | None = None
    minSizeUri: str | None = None


class UserDetail(BaseModel):
    name: str | None = None
    country: str | None = None
    hasPhoto: bool | None = None


class Answer(BaseModel):
    state: str | None = None
    lastUpdate: str | None = None
    createDate: str | None = None
    text: str | None = None
    supplierId: int | None = None
    employeeId: int | None = None
    editable: bool | None = None
    metadata: dict | None = None


class Feedback(BaseModel):
    id: str | None = None
    globalUserId: str | None = None
    wbUserId: int | None = None
    wbUserDetails: UserDetail | None = None
    nmId: int | None = None
    text: str | None = None
    pros: str | None = None
    cons: str | None = None
    matchingSize: str | None = None
    matchingPhoto: str | None = None
    matchingDescription: str | None = None
    productValuation: int | None = None
    color: str | None = None
    size: str | None = None
    createdDate: str | None = None
    updatedDate: str | None = None
    answer: Answer | None = None
    metadata: dict | None = None
    feedbackHelpfulness: list | None = None
    photos: list[Photo] | None = None
    video: str | None = None
    votes: dict | None = None
    rank: float | None = None


class ValuationDistribution(BaseModel):
    one: int = Field(alias='1')
    two: int = Field(alias='2')
    three: int = Field(alias='3')
    four: int = Field(alias='4')
    five: int = Field(alias='5')


class ItemReview(BaseModel):
    photosUris: list[list[str]] | None = None
    photo: list[int] | None = None
    valuation: str | None = None
    valuationSum: int | None = None
    valuationDistribution: ValuationDistribution | None = None
    valuationDistributionPercent: ValuationDistribution | None = None
    matchingSizePercentages: dict | None = None
    feedbackCount: int | None = None
    feedbackCountWithPhoto: int | None = None
    feedbackCountWithText: int | None = None
    feedbackCountWithVideo: int | None = None
    feedbacks: list[Feedback] | None = None
