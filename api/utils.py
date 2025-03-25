def get_query_filters(request):
    _filters = {}
    try:
        filters = request.query_params


        for i in filters:
            if i is not None and filters.get(i) is not None:
                _filters[i]  = filters.get(i)

        return _filters
    
    except:
        raise Exception("some error in query parameters")