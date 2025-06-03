from ..queries.paginations import ConversationPaginationQuery, FilterParamModel
from domain.aggregates.Pagination import PaginationParams, FilterParam, FilterCondition, OperationType, OrderByClause
from ..responses.conversation_response import *
from ..responses.conversation_response import ConversationPaginationResponse
from domain.aggregates.Pagination import PaginationDataCollection
import datetime
class ConversationMapper:
    @staticmethod
    def map_to_entity_response(domain_obj: Conversation | None) -> ConversationEntityResponse:

        response = ConversationEntityResponse(response_created_time=datetime.datetime.now(),
                                              status= ResponseStatus.Success if not domain_obj else ResponseStatus.Error,
                                              entity= domain_obj,
                                              entity_id= domain_obj.id if domain_obj else None)


        return response

    @staticmethod
    def pagination_out_to_in(pagination_query: ConversationPaginationQuery) -> PaginationParams[Conversation]:
        
        def map_filter_params() -> List[FilterParam]:
            filter_params = []
            if not pagination_query.title_search_word:
                filter_params.append(FilterParam[str](field_name="title",
                             filter_conditions=[FilterCondition(operator=pagination_query.title_search_word.operator,
                                                                value=pagination_query.title_search_word.value)]))
                
            created_date_cond: FilterParam[date] | None = None
            if not pagination_query.created_from_date_cond or not pagination_query.created_to_date_cond:
                created_date_cond = FilterParam[date](field_name="created_date")
                filter_params.append(created_date_cond)
            if not pagination_query.created_from_date_cond:
                created_date_cond.filter_conditions.append(FilterCondition[date](operator=OperationType.GreaterThanOrEqual,
                                                                                 value=pagination_query.created_from_date_cond))
            if not pagination_query.created_to_date_cond:
                created_date_cond.filter_conditions.append(FilterCondition[date](operator=OperationType.LessThanOrEqual,
                                                                                 value=pagination_query.created_to_date_cond))
                
            return filter_params
        
        result = PaginationParams[Conversation]()
        
        result.page_size = pagination_query.page_size
        result.page_num = pagination_query.page_num
        
        result.filter_params = map_filter_params()
        result.order_by_clauses = OrderByClause(order_type= pagination_query.order_by_clause.order_type,
                                                order_fields= set(pagination_query.order_by_clause.order_by_fields)) if pagination_query.order_by_clause else None
        result.distinct_by = set(pagination_query.distinct_by)
        
        return result 
    
    @staticmethod
    def pagination_in_to_out(pagination_data: PaginationDataCollection[Conversation]) -> ConversationPaginationResponse:
        return ConversationPaginationResponse(response_created_time = datetime.datetime.now(),
                                              description="Query Successful",
                                              current_page= pagination_data.page_num,
                                              total_page= pagination_data.total_page,
                                              total_record= pagination_data.total_record,
                                              page_size= pagination_data.page_size,
                                              data= pagination_data.data)




