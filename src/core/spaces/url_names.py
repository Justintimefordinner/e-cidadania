class SpaceURLs:
    ADD = 'create-space'
    EDIT = 'edit-space'
    DELETE = 'delete-space'
    INDEX = 'space-index'
    FEED = 'space-feed'
    LIST = 'list-spaces'
    GOTO = 'goto-space'
    EDIT_ROLES = 'edit-roles'
    SEARCH_USER = 'search-user'

class NewsURLs:
    SPACE_NEWS = 'list-space-news'  # for backwards compatibility
    ARCHIVE = 'post-archive'
    MONTH = 'post-archive-month'
    YEAR = 'post-archive-year'

class DocumentURLs:
    ADD = 'add-document'
    EDIT = 'edit-document'
    DELETE = 'delete-document'
    LIST = 'list-documents'

class EventURLs:
    ADD = 'add-event'
    EDIT = 'edit-event'
    DELETE = 'delete-event'
    LIST = 'list-events'
    VIEW = 'view-event'

class IntentURLs:
    ADD = 'add-intent'
    VALIDATE = 'validate-intent'