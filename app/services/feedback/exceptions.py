class FeedbackError(Exception):
    pass


class TraceNotFoundError(FeedbackError):
    pass


class TraceOwnershipError(FeedbackError):
    pass


class FeedbackNotFoundError(FeedbackError):
    pass
