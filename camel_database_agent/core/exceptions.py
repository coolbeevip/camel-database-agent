class DataGenerationError(Exception):
    """数据生成过程中的异常基类"""

    pass


class QueryParsingError(DataGenerationError):
    """查询解析错误"""

    pass


class KnowledgeException(Exception):
    """统一的数据库知识异常类"""

    pass
