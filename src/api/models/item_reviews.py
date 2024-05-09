from pydantic import BaseModel, Field


class Photo(BaseModel):
    fullSizeUri: str
    minSizeUri: str


class UserDetail(BaseModel):
    name: str
    country: str
    hasPhoto: bool


class Answer(BaseModel):
    state: str
    lastUpdate: str
    createDate: str
    text: str
    supplierId: int
    employeeId: int
    editable: bool
    metadata: dict | None = None


class Feedback(BaseModel):
    id: str
    globalUserId: str | None = None
    wbUserId: int
    wbUserDetails: UserDetail
    nmId: int
    text: str
    pros: str | None = None
    cons: str | None = None
    matchingSize: str | None = None
    matchingPhoto: str | None = None
    matchingDescription: str | None = None
    productValuation: int
    color: str
    size: str
    createdDate: str
    updatedDate: str
    answer: Answer
    metadata: dict | None = None
    feedbackHelpfulness: dict | None = None
    photos: list[Photo]
    video: str | None = None
    votes: dict | None = None
    rank: float


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
