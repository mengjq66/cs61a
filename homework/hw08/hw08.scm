; Macros

(define-macro (list-of map-expr for var in lst if filter-expr)
	(list 'map `(lambda (,var) ,map-expr) `(filter (lambda (,var) ,filter-expr) ,lst)))